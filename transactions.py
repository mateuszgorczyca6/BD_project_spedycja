import pandas as pd
from datetime import timedelta

def add_salary(comp, act_date):
    for i in range(len(comp.employees)):
        employment_date = comp.employees.loc[i]['Employment Date']
        release_date = comp.employees.loc[i]['Release Date']
        if release_date is None or (act_date + timedelta(days = 30) >= employment_date and act_date + timedelta(days = 30) <= release_date):
            salary = comp.employees.loc[i]['Last Salary']
            comp.transactions.loc[len(comp.transactions)] = pd.Series([act_date, salary,
                f'Wypłata dla {i}', -1.3 * salary]).values
            comp.saldo -= 1.3 * salary

def pay_OC(comp,act_date):
    for i in range(len(comp.cars)):
        last_overviev = comp.cars.loc[i]['Last Overview']
        if act_date >= last_overviev + timedelta(days = 365):
            comp.cars.loc[i]['Last Overview'] = act_date
            price = {'Dostawczak': 1500, 'Mała Ciężarówka': 2000, 'Duża Ciężarówka': 2500}[comp.cars.loc[i]['Type']]
            comp.transactions.loc[len(comp.transactions)] = pd.Series([act_date, price,
                f'Opłata OC dla {i}', -price]).values
            comp.saldo -= price