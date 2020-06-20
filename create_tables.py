from connect import connect
from datetime import datetime, date, timedelta
from employees import *
from transactions import *
from orders import *
from cars import *
from math import ceil
from callendar import *
from os import system


class Company():
    def __init__(self):
        # lists
        self.employees = pd.DataFrame(columns = [
            'Employee ID', 'Name', 'Position', 'Birth Date', 'Last Salary', 'Phone Number', 'Employment Date', 'Release Date'
        ])
        self.job_offers = []
        self.actual_drivers = []
        self.transactions = pd.DataFrame(columns = [
            'Transaction ID', 'Date', 'Sum', 'Type', 'Balance Change', 'Order ID'
            ])
        self.cars = pd.DataFrame(columns = [
            'Car ID', 'Type', 'Last Overview', 'Capacity', 'Combust', 'Additional Functionality', 'Price', 'Last Tanking (km)'
        ])
        self.orders = pd.DataFrame(columns = [
            'Order ID', 'Product', 'Origin', 'Destination', 'Distance', 'Special Treatment', 'Duration', 'Price', 'Mass', 'Date', 'Client ID', 'Employee ID', 'Car ID'
        ])
        self.clients = pd.DataFrame(columns = [
            'Client ID', 'Name', 'Birth Date', 'Phone Number', 'E-mail'
        ])

        # saldo
        self.saldo = 500000

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
        self.employees.loc[len(self.employees)]=pd.Series(
            [0, *make_employee('boss', act_date, self.l_drivers, self.l_logistics)]
        ).values

        # number of cars
        self.l_van = 0  # m = 0,9t, OC = 1500zł, comb = 10l/100km
        self.l_struck = 0 # m = 8t, OC = 2000zł, comb = 20l/100km
        self.l_btruck = 0  # m = 24t, OC = 2500zł, comb = 30l/100km
        for i in range(5):
            make_car(self, act_date)

    def update(self):
        if act_date.month == 5 and act_date.day == 4:
            change_salary(self, act_date)
        if act_date.day == 10: ## wypłata
            add_salary(self, act_date)
            system('cls')
            print(act_date)
        for i in self.job_offers:
            i.update(act_date)
        pay_OC(self, act_date)
        if self.saldo > 100000 * (self.plan_drivers - 1):
            add_driver(self, act_date) # add driver and other if needed
        if working_day(act_date):
            make_offers_if_needed(self, act_date)
            destroy_car(self, act_date)
            take_orders(self, act_date)
            tank_cars(self, act_date)
        delete_employee_when_released(self, act_date)

    def __str__(self):
        return(str(self.employees))



def get_tables():
    global act_date, t, T
    T = 1826
    t = 0 # -> 3652
    act_date = date.today() - timedelta(days = T)
    c = Company()
    while t <= T:
        c.update()
        act_date += timedelta(days = 1)
        t += 1
        if act_date.day == 11:
            print(c.l_drivers)
            print(c.saldo)
    return c.employees, c.transactions, c.cars, c.orders, c.clients

if __name__ == '__main__':
    a = get_tables()
