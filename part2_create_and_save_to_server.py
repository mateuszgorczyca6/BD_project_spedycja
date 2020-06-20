from create_tables import get_tables
import pandas as pd
import pymysql
# getting tables
employees, transactions, cars, orders, clients = get_tables()
# connectiong to server
con = pymysql.connect(host='localhost',
                      user='Matt',
                      password='578469')
cur = con.cursor()

# dropping db
cur.execute('''DROP DATABASE IF EXISTS project''')

# creating new db
cur.execute('''CREATE DATABASE project''')

# closeconnection to server and connect to db
con.close()
con = pymysql.connect(host='localhost',
                      user='Matt',
                      password='578469',
                      db='project')
cur = con.cursor()
### save to sql table
def save_to_SQL(data, cur, table_name):
    # creating column list for insertion
    cols = "`,`".join([str(i) for i in data.columns.tolist()])
    # Insert DataFrame recrds one by one.
    for _,row in data.iterrows():
        sql = "INSERT INTO " + table_name+" (`"  + cols + "`) VALUES (" + "%s,"*(len(row)-1) + "%s)"
        cur.execute(sql, tuple(row))
# creating new tables
cur.execute('''CREATE TABLE employees (
    `Employee ID` SMALLINT,
    Name TINYTEXT,
    Position TINYTEXT,
    `Birth Date` DATE,
    `Last Salary` SMALLINT,
    `Phone Number` INT,
    `Employment Date` DATE,
    `Release Date` DATE
)''')
cur.execute('''CREATE TABLE transactions (
    `Transaction ID` MEDIUMINT,
    Date DATE,
    Sum FLOAT,
    Type TINYTEXT,
    `Balance Change` FLOAT,
    `Order ID` SMALLINT
)''')
cur.execute('''CREATE TABLE cars (
    `Car ID` SMALLINT,
    Type TINYTEXT,
    `Last Overview` DATE,
    Capacity FLOAT,
    Combust FLOAT,
    `Additional Functionality` TINYTEXT,
    Price MEDIUMINT,
    `Last Tanking (km)` FLOAT
)''')
cur.execute('''CREATE TABLE orders (
    `Order ID` MEDIUMINT,
    Product TINYTEXT,
    Origin TINYTEXT,
    Destination TINYTEXT,
    Distance FLOAT,
    `Special Treatment` TINYTEXT,
    Duration FLOAT,
    Price FLOAT,
    Mass FLOAT,
    Date DATE,
    `Client ID` SMALLINT,
    `Employee ID` SMALLINT,
    `Car ID` SMALLINT
)''')
cur.execute('''CREATE TABLE clients (
    `Client ID` SMALLINT,
    Name TINYTEXT,
    `Birth Date` DATE,
    `Phone Number` INT,
    `E-mail` TINYTEXT
)''')
save_to_SQL(employees, cur, 'employees')
save_to_SQL(cars, cur, 'cars')
save_to_SQL(orders, cur, 'orders')
save_to_SQL(transactions, cur, 'transactions')
save_to_SQL(clients, cur, 'clients')
# closing connection
con.commit()
con.close()