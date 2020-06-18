from connect import connect
from datetime import datetime, date, timedelta
from employees import *
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
        'Position', 'Birth Date', 'Salary', 'Phone Number', 'Employment Date', 'Release Date'])
        self.job_offers = []

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

    def make_offers_if_needed(self, act_date):
        if self.plan_accountants > self.l_accountants + self.o_accountants:
            self.job_offers.append(Job_offer('accountant', act_date, self))
            self.o_accountants += 1
        if self.plan_drivers > self.l_drivers + self.o_drivers:
            self.job_offers.append(Job_offer('driver', act_date, self))
            self.o_drivers += 1
        if self.plan_logistics > self.l_logistics + self.o_logistics:
            self.job_offers.append(Job_offer('logistic', act_date, self))
            self.o_logistics += 1
        if self.plan_phisic_workers > self.l_phisic_workers + self.o_phisic_workers:
            self.job_offers.append(Job_offer('physic worker', act_date, self))
            self.o_phisic_workers += 1

    def update(self):
        self.make_offers_if_needed(act_date)
        for i in self.job_offers:
            i.update(act_date)

    def __str__(self):
        return(str(self.employees))

c = Company()
print(act_date)
print(c)
while t <= 20:
    c.update()
    act_date += timedelta(days = 1)
    t += 1
print(act_date)
print(c)