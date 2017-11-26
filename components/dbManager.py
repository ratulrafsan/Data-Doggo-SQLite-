import sqlite3

class DBManager():
    def __init__(self, dbPath):
        self.db = sqlite3.connect(dbPath)
        self.cursor = self.db.cursor()

        self.error = ""
        self.isTable = False

    def executor(self, sql):
        try:
            self.cursor.execute(sql)
            if self.cursor.description is not None:
                self.isTable = True

            return True
        except Exception as e:
            self.error = e
            return False

    def getColumnNames(self, tableName):
        try:
            sql = "select * from {}".format(tableName)
            self.cursor.execute(sql)
            return [column[0] for column in self.cursor.description]
        except Exception as e:
            self.error = e
        return None

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