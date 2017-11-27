import sqlite3

from PyQt5.Qt import *


class DBManager(QObject):
    sqlExecuted = pyqtSignal()

    def __init__(self, dbPath):
        super().__init__()
        self.db = sqlite3.connect(dbPath)
        self.cursor = self.db.cursor()

        self.error = ""
        self.isTable = False

        # yes, I'm aware of how much of a bad practice this is..
        self.dbStrucute = None
        self.dataBrowser = None
        self.loader = None

    def setdbStrucuteReference(self, dbStructue):
        if self.dbStrucute is None:
            self.dbStrucute = dbStructue

    def setDataBrowserReference(self, dataBrowser):
        if self.dataBrowser is None:
            self.dataBrowser = dataBrowser

    def setLoaderReference(self, loader):
        if self.loader is None:
            self.loader = loader

    def executor(self, sql):
        try:
            self.cursor.execute(sql)
            if self.cursor.description is not None:
                self.isTable = True
            else:
                self.isTable = False
            self.sqlExecuted.emit()
            print("executed: "+sql)
            self.setStatusBarMessage("executed: " + sql)
            return True
        except Exception as e:
            self.error = e
            print(e)
            self.setStatusBarMessage("Error: " + str(e))
            return False

    def setStatusBarMessage(self, msg):
        self.loader.mainWindow.statusBar().showMessage(msg)

    def getColumnNames(self, tableName):
        try:
            sql = "select * from {}".format(tableName)
            self.cursor.execute(sql)
            return [column[0] for column in self.cursor.description]
        except Exception as e:
            self.error = e
            return []

    def getAllData(self, tableName):
        try:
            sql = "select * from {}".format(tableName)
            return self.cursor.execute(sql).fetchall()
        except Exception as e:
            self.error = e
            return None

    def getError(self):
        if self.error is not "":
            return self.error
            return None

    def getListofTables(self):
        try:
            self.cursor.execute("select tbl_name from sqlite_master where type='table'")
            return [t[0] for t in self.cursor.fetchall()]
        except Exception as e:
            self.error = e
            return None

    def getColumnTypes(self, tableName):
        try:
            sql = "pragma table_info({})".format(tableName)
            self.cursor.execute(sql)
            return [(i[1], i[2]) for i in self.cursor.fetchall()]
        except Exception as e:
            self.error = e
            return None

    def getColumnCount(self, tableName):
        data = self.getColumnNames(tableName)
        if data is not None:
            return len(data)
        return 0

    def deleteRow(self, table, columnName, identifier):
        try:
            sql = "delete from {} where {}={}".format(table, columnName, identifier)
            self.cursor.execute(sql)
        except Exception as e:
            self.error = e

    def updateQueryConstructor(self, tableName, identifierList, identifierDataList, updatingColumn, updatingValue):
        sql = "update " + tableName + " set " + updatingColumn + "='" + updatingValue + "' where "
        for i, column in enumerate(identifierList):
            sql += " {}='{}' {}".format(column, identifierDataList[i], "and" if i != len(identifierList)-1 else ';')
        self.executor(sql)

    def hasAutoIncColumn(self, tableName):
        sql = "select 1 from sqlite_master where tbl_name='{}' and sql like '%AUTOINCREMENT%';".format(tableName)
        resp = self.executor(sql)
        if resp is False:
            return None
        else:
            data = self.cursor.fetchall()
            if len(data) > 0:
                return data[0][0]
            return 0

    def getAutoIncColumnNames(self, tableName):
        resp = self.hasAutoIncColumn(tableName)
        if resp == 0 or resp is None:
            return []

        names = []
        sql = "select sql from sqlite_master where tbl_name='{}'".format(tableName)
        resp = self.executor(sql)
        if resp is False:
            return []

        colNames = self.getColumnNames(tableName)
        schema = self.cursor.fetchall()
        if len(schema) > 0:
            schema = schema[0][0].split(',')
        candidates = []
        for col in schema:
            if 'autoincrement' in col.lower():
                candidates.append(col)
        # too tired to hack-up a generator
        # TODO: use generator?
        if len(candidates) > 0:
            for d in candidates:
                for col in colNames:
                    if col in d:
                        names.append(col)

        return names

    def getNotNullColNames(self, tableName):
        names = []
        sql = "pragma table_info({})".format(tableName)
        res = self.executor(sql)
        if res is False:
            return []
        data = self.cursor.fetchall()
        if len(data) > 0:
            for dataSet in data:
                if str(dataSet[3]) == "1":
                    names.append(dataSet[1])
        return names

    def addNewRow(self, tableName, colNames, values):
        sql = "insert into "+ tableName + " " + str(tuple(colNames)) + " values ("
        for i, data in enumerate(values):
            sql += " {} {} ".format(data, ' ' if i < len(values)-1 else ')' )
        print(sql)

    def addEmptyRow(self, tableName):
        notNull = self.getNotNullColNames(tableName)
        if len(notNull) == 0:
            colNames = self.getColumnNames(tableName)
            notNull = list(set(colNames) - set(self.getAutoIncColumnNames(tableName)))
            if len(notNull) == 0:
                notNull = colNames
        sql = "insert into " + tableName + " " + str(tuple(notNull)) + "values" + \
              str(tuple(["insertValue" for i in range(0, len(notNull))])) + ";"
        res = self.executor(sql)
        if res == False:
            print("Error addint empty row: " + str(self.error))


    def commitToDB(self):
        self.db.commit()