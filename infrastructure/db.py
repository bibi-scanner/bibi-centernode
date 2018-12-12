import sqlite3
import os

class Database:
    def getConn(self):
        dbpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test.db')
        return sqlite3.connect(dbpath)

    def closeConn(self, conn):
        return conn.close()

def init():
    db = Database()
    conn = Database().getConn()

    # 初始化
    sqlpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'init.sql')
    sqlf = open(sqlpath, 'r')
    data = sqlf.read()
    sqlf.read()
    conn.executescript(data)

    db.closeConn(conn)

init()
