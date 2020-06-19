# v 0.1 (18.06.2020r.)
   connect.py \[new\]
      + function connectiong to database
   create_tables.py \[new\]
      + number of workers
      + make boss
   employees.py \[new\]
      + generating names
      + birth date generating
      + salary generating
      + function that creates personal info of employee
      
# v 0.1.1 (18.06.2020r.)
   create_tables.py
      ~ change persons indexing to starting from 0 not 1
      + function making job offers
   employees.py
      ~ position name from 'worehouse worker' to 'phisic worker'
      + klasa Job_Offer
      
# v 0.1.2 (19.06.2020r.)
   create_tables.py
      ~ column name from 'Salary' to 'Last Salary'
      + transactions list
      + saldo (start = 10000)
      ~ mover function 'make_offers_if_needed' to employee.py
   employees.py
      + added gender in name generating function
      + function that change salary of workers at one day a year
      ~ added generation of employees release date
      + now employers are released when it's their time
      ~ job offer now change number of employees
      + function that makes job offers when needed
      + function that add employees when needed or whed saldo is big enought
   transactions.py
      + function to pay salaries to employees
      
# v 0.2 (19.06.2020r.)
   create_tables.py
      + cars list
      ~ saldo change from 10000 to 300000
      + number of cars of each type
   employees.py
      ~ change function of logistics salary
      ~ phone number is now int type
   cars.py \[new\]
      + function that add cars when number of drivers is increasing
      + function responsible for repairing cars
   transactions.py
      ~ fixed: now salary is paid only when employee is working (before he was payed after released)
      + function that pay OC

# v 0.2.1 (19.06.2020r.)
   create_tables.py
      ~ added 'Order ID' column to transaction list
      ~ added 'Price' column to cars list
   cars.py
      ~ repaired error in destroy_car function
