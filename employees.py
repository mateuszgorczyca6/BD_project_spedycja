import pandas as pd
from random import random as rand
from numpy.random import choice as rand_list
from datetime import timedelta, date
from math import floor, ceil

###########################
###        names        ###
###########################
## data from https://dane.gov.pl
Mfnames = pd.read_csv("data/M_fnames.csv")  # male first names
Ffnames = pd.read_csv("data/F_fnames.csv")  # female first names
Mlnames = pd.read_csv("data/M_lnames.csv")  # male last names
Flnames = pd.read_csv("data/F_lnames.csv")  # female last names
Mfnames = list(Mfnames['IMIĘ_PIERWSZE'])[:100]
Ffnames = list(Ffnames['IMIĘ_PIERWSZE'])[:100]
Mlnames = list(Mlnames['Nazwisko aktualne'])[:1000]
Flnames = list(Flnames['Nazwisko aktualne'])[:1000]

def get_name(pos):
    if rand() < 0.5 or pos == 'warehouse worker':    # male
        name = rand_list(Ffnames).capitalize() + " " + rand_list(Flnames).capitalize()
    else:                                                    # female
        name = rand_list(Mfnames).capitalize() + " " + rand_list(Mlnames).capitalize()
    return name


def get_birth_date(actual_date):
    birth_date = actual_date - timedelta(days=8400+15000*rand()) 
    return birth_date

###########################
###        salary       ###
###########################

def get_salary(pos, act_date, employment_date, l_drivers, l_logistics):
    work_time = act_date.year - employment_date.year
    if pos == 'boss':
        return 100 * floor(50 + l_drivers ** 1/2 * 10)
    elif pos == 'accountant':
        return 100 * floor (35 + l_drivers ** 1/2 * 7)
    elif pos == 'driver':
        return 3000 + 200 * work_time
    elif pos == 'logistic':
        return 100 * floor((35 + l_drivers ** 1/2 * 7) ** 1/(l_logistics + 1))
    else:
        return 100 * (25 + l_logistics * 2)

###########################
###        making       ###
###########################

def make_employee(pos, act_date = date(2000,1,1), l_drivers=1, l_logistics=1):
    ''' Generate random person data'''
    name = get_name(pos)
    birth_date = get_birth_date(act_date)
    salary = get_salary(pos, act_date, act_date, l_drivers, l_logistics)
    phone_number = 500000000 + 300000000 * rand()
    employment_date = act_date
    release_date = None
    return [name, pos, birth_date, salary, phone_number, employment_date, release_date]

###########################
###      job offer      ###
###########################

