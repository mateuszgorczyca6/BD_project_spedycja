import pandas as pd

def add_salary(comp, act_date):
    for i in range(len(comp.employees)):
        salary = comp.employees.loc[i]['Last Salary']
        comp.transactions.loc[len(comp.transactions)] = pd.Series([act_date, salary,
        f'Wypłata dla {i}', -1.3 * salary]).values
        comp.saldo -= 1.3 * salary