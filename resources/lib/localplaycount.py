try:
    from sqlite3 import dbapi2 as database
except:
    from pysqlite2 import dbapi2 as database

import json

from resources.lib import control


def getPlaycount():
    try:
        dbcon = database.connect(control.playcountFile)
        dbcur = dbcon.cursor()
        dbcur.execute("SELECT * FROM playcount")
        items = dbcur.fetchall()
        items = [(i[0].encode('utf-8'), eval(i[1].encode('utf-8'))) for i in items]
    except:
        items = []

    return items


def addPlaycount(id):
    try:
        control.makeFile(control.dataPath)
        dbcon = database.connect(control.playcountFile)
        dbcur = dbcon.cursor()
        dbcur.execute("CREATE TABLE IF NOT EXISTS playcount (""id TEXT, ""items TEXT, ""UNIQUE(id)"");")
        dbcur.execute("DELETE FROM playcount WHERE id = '%s'" %  id.decode('utf-8'))
        dbcur.execute("INSERT INTO playcount Values (?, ?)", (id.decode('utf-8'), '0'))
        dbcon.commit()

        control.refresh()
    except:
        return


def deletePlaycount(id):
    try:
        try:
            dbcon = database.connect(control.playcountFile)
            dbcur = dbcon.cursor()
            dbcur.execute("DELETE FROM playcount WHERE id = '%s'" % id.decode('utf-8'))       
            dbcon.commit()
            control.refresh()
        except:
            pass

    except:
        return