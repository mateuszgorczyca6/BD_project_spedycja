import pandas as pd
from random import random as rand
from math import floor
from scipy.stats import expon

def make_car(comp, act_date): # we want   2 van : 3 struck : 4 btruck
    '''Create procedural car'''
    val = rand()
    if val < 0.6:
        add = ''
    elif val < 0.85:
        add = 'fluid'
    elif val < 0.95:
        add = 'fridge'
    else:
        add = 'fluid, fridge'
    price = 1000 * floor({'': 45 + 10 * rand(),
        'fluid': 60 + 10 * rand(),
        'fridge': 50 + 10 * rand(),
        'fluid, fridge': 75 + 10 * rand()}[add])
    if 3 * comp.l_van < 2 * comp.l_struck:
        ctype = 'Van'
        cap = floor(10 * (0.8 + 0.2 * rand())) / 10
        comb = floor(10 * (9 + 2 * rand())) / 10
        comp.l_van += 1
    elif 4 * comp.l_struck < 3 * comp.l_btruck:
        ctype = 'Small Truck'
        cap = floor(10 * (8 + 2 * rand())) / 10
        comb = floor(10 * (18 + 4 * rand())) / 10
        comp.l_struck += 1
        price += 20000
    else:
        ctype = 'Big Truck'
        cap = floor(10 * (20 + 8 * rand())) / 10
        comb = floor(10 * (25 + 6 * rand())) / 10
        comp.l_btruck += 1
        price += 50000
    print(price)
    comp.cars.loc[len(comp.cars)] = pd.Series([ctype, act_date, cap, comb, add, price]).values
    comp.transactions.loc[len(comp.transactions)] = pd.Series([act_date, price, 'Buy car {}'.format(len(comp.cars)), -price, None]).values
    comp.saldo -= price

def destroy_car(comp, act_date):
    '''Check if car is damaged and make transaction for it'''
    for i in range(len(comp.cars)):
        if rand() <= 1/250:
            price = 1000 * expon.rvs(1)
            if price > comp.cars.loc[i]['Price']:
                title = f'Buy car {i}'
                price = comp.cars.loc[i]['Price']
                comp.cars.loc[i]['Overview Date'] = act_date
            else:
                title = f'Repair of {i}'
            comp.transactions.loc[len(comp.transactions)] = pd.Series([act_date, price, title, -price, None]).values
            comp.saldo -= price