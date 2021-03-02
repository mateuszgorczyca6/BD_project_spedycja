import matplotlib.pyplot as plt
import pandas as pd
import pymysql


############################################
### connection
############################################
con = pymysql.connect(host='localhost',
                      user='Matt',
                      password='578469',
                      db='project')
cur = con.cursor()
############################################
### 1. Waiting orders
############################################

cur.execute('SET @csum := 0')
daily_orders = pd.read_sql('''
SELECT Date, @csum := @csum + IF(Ordered IS NOT NULL, Ordered, 0) - IF(Delivered IS NOT NULL, Delivered, 0) AS `Waiting Orders`
FROM (
	(SELECT ordered.Date AS Date, Ordered, Delivered
	FROM
		(SELECT `Order Date` AS Date, COUNT(*) AS Ordered
		FROM orders
		GROUP BY `Order Date`) AS ordered
	LEFT OUTER JOIN
		(SELECT `Delivery Date` AS Date, COUNT(*) AS Delivered
		FROM orders
		GROUP BY `Delivery Date`) AS delivered
	ON ordered.Date = delivered.Date)
UNION
	(SELECT ordered.Date AS Date, Ordered, Delivered
	FROM
		(SELECT `Order Date` AS Date, COUNT(*) AS Ordered
		FROM orders
		GROUP BY `Order Date`) AS ordered
	RIGHT OUTER JOIN
		(SELECT `Delivery Date` AS Date, COUNT(*) AS Delivered
		FROM orders
		GROUP BY `Delivery Date`) AS delivered
	ON ordered.Date = delivered.Date)
    ORDER BY Date) AS tab
WHERE Date IS NOT NULL
GROUP BY Date
''', con)

daily_orders = daily_orders.set_index('Date')
daily_orders.plot()
plt.savefig('images/p3_001.pdf')

############################################
### 2. Active workers
############################################

cur.execute('SET @csum := 0')
working_workers = pd.read_sql('''
SELECT Date, @csum := @csum + Employed - Released AS `Working Workers`
FROM
	(SELECT *
	FROM
		(
			(SELECT employment.Date AS Date, IFNULL(Employed,0) AS Employed, IFNULL(Released,0) AS Released
			FROM
				(SELECT `Employment Date` AS Date, COUNT(*) AS Employed
				FROM employees
				GROUP BY `Employment Date`) AS employment
			LEFT JOIN
				(SELECT `Release Date` AS Date, COUNT(*) AS Released
				FROM employees
				WHERE `Release Date` IS NOT NULL
				GROUP BY `Release Date`) AS released
			ON employment.Date = released.Date)
		UNION
			(SELECT released.Date AS Date, IFNULL(Employed,0) AS Employes, IFNULL(Released,0) AS Released
			FROM
				(SELECT `Employment Date` AS Date, COUNT(*) AS Employed
				FROM employees
				GROUP BY `Employment Date`) AS employment
			RIGHT JOIN
				(SELECT `Release Date` AS Date, COUNT(*) AS Released
				FROM employees
				WHERE `Release Date` IS NOT NULL
				GROUP BY `Release Date`) AS released
			ON employment.Date = released.Date)
		) AS emp_rel_unsorted
		ORDER BY Date
	) AS emp_rel_sorted
''', con)

working_workers = working_workers.set_index('Date')
working_workers.plot()
plt.savefig('images/p3_002.pdf')

############################################
### 3. Saldo.
############################################

cur.execute('SET @csum := 500000')
saldo = pd.read_sql('''
SELECT Date, @csum := @csum + c AS Saldo
FROM
	(SELECT Date, SUM(`Balance Change`) AS c
	FROM transactions
	GROUP BY Date) AS balance_changes
''', con)
saldo = saldo.set_index('Date')
saldo.plot()
plt.savefig('images/p3_003.pdf')

############################################
### 4. The biggest waiters
############################################

waiters = pd.read_sql('''
SELECT orders.`Client ID` AS `Client ID`, Name, SUM(DATEDIFF(`Delivery Date`, `Order Date`)) / COUNT(*) AS `Average Waiting Time`, COUNT(*) AS `Number of Orders`
FROM orders
LEFT JOIN clients
ON orders.`Client ID` = clients.`Client ID`
GROUP BY orders.`Client ID`
ORDER BY `Average Waiting Time` DESC
LIMIT 10
''', con)

############################################
### 5. Number of orders made by each car type
############################################

orders_per_car_type = pd.read_sql('''
SELECT Type, n AS `Nuber of orders`, COUNT(*) AS `Number of cars`
FROM cars
LEFT JOIN
	(SELECT `Car ID`, COUNT(*) AS n
    FROM orders
    GROUP BY `Car ID`) AS order_by_car
ON cars.`Car ID` = order_by_car.`Car ID`
GROUP BY Type
''', con)

############################################
### 6. Chance for driver to take two orders
############################################

two_orders_chance = pd.read_sql('''
SELECT SUM(aa) / (COUNT(*) - SUM(aa)) AS `Chance for driver to take two orders`
FROM
	(SELECT COUNT(*) - 1 AS aa
	FROM orders
	GROUP BY `Delivery Date`, `Employee ID`) AS a
''', con).loc[0]['Chance for driver to take two orders']

############################################
### 7. Average salary by position
############################################

avg_salary = pd.read_sql('''
SELECT
	Year,
	SUM(IF(Position = 'boss', `Average Salary`, 0))/
    COUNT(IF(Position = 'boss', `Average Salary`, Null)) AS `Boss`,
	SUM(IF(Position = 'logistic', `Average Salary`, 0))/
    COUNT(IF(Position = 'logistic', `Average Salary`, Null)) AS `Logistic`,
	SUM(IF(Position = 'driver', `Average Salary`, 0))/
    COUNT(IF(Position = 'driver', `Average Salary`, Null)) AS `Driver`,
	SUM(IF(Position = 'manual worker', `Average Salary`, 0))/
    COUNT(IF(Position = 'manual worker', `Average Salary`, Null)) AS `Manual Worker`,
	SUM(IF(Position = 'accountant', `Average Salary`, 0))/
    COUNT(IF(Position = 'accountant', `Average Salary`, Null)) AS `Accountant`
FROM
	(SELECT YEAR(Date) AS Year, AVG(Sum) AS `Average Salary`, SUBSTRING_INDEX(Type, ' ', -1) AS `Employee ID`
	FROM transactions
	WHERE Type LIKE 'Salary for %'
	GROUP BY Year, Type) AS avg_salary_per_year_and_position
LEFT JOIN
	employees
ON avg_salary_per_year_and_position.`Employee ID` = employees.`Employee ID`
GROUP BY Year
''', con)

avg_salary = avg_salary.set_index('Year')
avg_salary.plot()
plt.savefig('images/p3_007.pdf')

############################################
### 8. Number of transactions made each day
############################################

trans = pd.read_sql('''
SELECT `Delivery Date` AS Date, COUNT(*) AS `Number of transactions`
FROM orders
GROUP BY `Delivery Date`
''', con)
trans = trans.set_index('Date')
trans.plot()
plt.savefig('images/p3_008.pdf')


con.close()