import pymysql
import os

class Database:
    def getConn(self):
        return pymysql.connect(host="10.10.9.120", user="root", password="root",
                               db='scanner', charset='utf8', cursorclass=pymysql.cursors.DictCursor)


    def closeConn(self, conn):
        return conn.close()

def init():
    db = Database()
    conn = Database().getConn()
    cr = conn.cursor()

    # 初始化
    sqlpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'init.sql')
    sqlf = open(sqlpath, 'r')
    data = sqlf.read()
    sqlf.read()
    cr.execute(data)

    cr.close()
    conn.close()

# init()
