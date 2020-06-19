import sqlite3 as sql


def connect(path):
    conn = sql.connect(path)
    cur = conn.cursor()
    return conn, cur