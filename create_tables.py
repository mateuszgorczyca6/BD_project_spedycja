from connect import connect
from datetime import datetime, date, timedelta
from employees import *
from math import ceil

conn, cur = connect(r'D:\Programy\MySQL Server\data xyz\Data\mysql.db')

T = 3652
t = 0 # -> 3652
act_date = date.today() - timedelta(days = T)

class Company():
    def __init__(self):
        # lists
        self.employees = pd.DataFrame(columns = ['Name',
        'Position', 'Birth Date', 'Salary', 'Phone Number', 'Employment Date', 'Release Date'])

        # planned number of employees
        self.plan_accountants = 1
        self.plan_drivers = 3
        self.plan_logistics = 1
        self.plan_phisic_workers = 2
        # number of employees
        self.l_accountants = 0
        self.l_drivers = 0
        self.l_logistics = 0
        self.l_phisic_workers = 0
        # number of job offers
        self.o_accountants = 0
        self.o_drivers = 0
        self.o_logistics = 0
        self.o_phisic_workers = 0

        # make boss
        self.employees.loc[1]=pd.Series(make_employee('boss', act_date, self.l_drivers, self.l_logistics)).values

    def make_offers_if_needed(self):
        pass

    def update(self):
        self.make_offers_if_needed()

    def __str__(self):
        return(str(self.employees))

c = Company()
print(c)