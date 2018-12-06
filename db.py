import sqlite3


def connect():
    conn = sqlite3.connect('./test.db')
    print("Opened database successfully")

connect()

