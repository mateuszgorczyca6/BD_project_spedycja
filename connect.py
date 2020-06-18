import sqlite3 as sql

# dile is 'D:\Programy\MySQL Server\data xyz\Data\mysql.db'
def connect(path):
    conn = sql.connect(path)
    cur = conn.cursor()
    return conn, cur

