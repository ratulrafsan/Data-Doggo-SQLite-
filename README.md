# Data Doggo (SQLite)
An attempt to write a sqlite database management software in a day

# REQUIRES PYQT5

# Installation
- pull this repo/download it as zip and extract it wherever you want
- install PyQt5 via PIP3
```
sudo pip3 install PyQt5
```
- launch it by starting ```Main.py```
```
python3 Main.py
```

# Bugs
If you are creating a new database file using it, make sure you reload the file after you've created the table. Otherwise the changes won't be shown on the data browser section. (Table structure seems to work fine :/)

# Todo
1. Add proper error messages!
2. Add output section for the executor
3. Add a proper menu bar (specially for the the dock)
4. Add syntax highlighting and auto-complete features
5. Add graphical way of creating and altering existing table
6. Rollback system
7. IDK, you tell me.

# Screenshots (KDE Oxygen theme)
![Table strucute](https://i.imgur.com/mhlLGZe.png)
![Data browser](https://i.imgur.com/9JrdzRE.png)
