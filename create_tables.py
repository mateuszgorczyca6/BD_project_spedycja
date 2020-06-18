from connect import connect
from datetime import datetime, date, timedelta
from employees import *
from transactions import *
from math import ceil

# file is 'D:\Programy\MySQL Server\data xyz\Data\mysql.db'
conn, cur = connect(r'D:\Programy\MySQL Server\data xyz\Data\mysql.db')

T = 3652
t = 0 # -> 3652
act_date = date.today() - timedelta(days = T)

class Company():
    def __init__(self):
        # lists
        self.employees = pd.DataFrame(columns = ['Name',
        'Position', 'Birth Date', 'Last Salary', 'Phone Number', 'Employment Date', 'Release Date'])
        self.job_offers = []
        self.transactions = pd.DataFrame(columns = ['Date', 'Sum', 'Type', 'Balance Change'])

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
        self.employees.loc[len(self.employees)]=pd.Series(make_employee('boss', act_date, self.l_drivers, self.l_logistics)).values

        # saldo
        self.saldo = 10000

    def update(self):
        make_offers_if_needed(self, act_date)
        for i in self.job_offers:
            i.update(act_date)
        delete_employee_when_released(self, act_date)
        if act_date.month == 5 and act_date.day == 4:
            change_salary(self, act_date)
        if self.saldo > 200000:
            add_driver(self) # add driver and other if needed
        if act_date.day == 10: ## wypłata
            add_salary(self, act_date)

    def __str__(self):
        return(str(self.employees))

c = Company()
while t <= T:
    c.update()
    act_date += timedelta(days = 1)
    t += 1
print(c.employees)
print(c.transactions)