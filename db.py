import sqlite3
import classes


def connect():
    conn = sqlite3.connect('./test.db')
    print("Opened database successfully")

data = classes.Node()

connect()
