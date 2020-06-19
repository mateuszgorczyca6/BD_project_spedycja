import pandas as pd
from random import random as rand
from numpy.random import choice as rand_list
from datetime import timedelta, date
from math import floor, ceil
from scipy.stats import expon
from cars import *

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
    ''' Create Name'''
    if rand() < 0.5 or pos == 'physic worker':    # male
        name = rand_list(Ffnames).capitalize() + " " + rand_list(Flnames).capitalize()
        gender = 'male'
    else:                                                    # female
        name = rand_list(Mfnames).capitalize() + " " + rand_list(Mlnames).capitalize()
        gender = 'female'
    return name, gender

###########################
###      birth date     ###
###########################

def get_birth_date(actual_date):
    ''' Create Birth Date'''
    birth_date = actual_date - timedelta(days=8400+15000*rand()) 
    return birth_date

###########################
###        salary       ###
###########################

def get_salary(pos, act_date, employment_date, l_drivers, l_logistics):
    '''Return Salary'''
    work_time = act_date.year - employment_date.year
    if pos == 'boss':
        return 100 * floor(50 + l_drivers ** 1/2 * 10)
    elif pos == 'accountant':
        return 100 * floor (35 + l_drivers ** 1/2 * 7)
    elif pos == 'driver':
        return 3000 + 200 * work_time
    elif pos == 'logistic':
        return 100 * floor((35 + l_drivers ** 1/2 * 7) / (l_logistics + 1) ** 1/5)
    else:
        return 100 * (25 + l_logistics * 2)

def change_salary(comp, act_date):
    '''Change employees salary'''
    for i in range(len(comp.employees)):
        comp.employees.at[i, 'Last Salary'] = get_salary(comp.employees.loc[i]['Position'], act_date,
        comp.employees.loc[i]['Employment Date'], comp.l_drivers, comp.l_logistics)

###########################
###    making person    ###
###########################

def make_employee(pos, act_date = date(2000,1,1), l_drivers=1, l_logistics=1):
    ''' Generate random person data'''
    name, gender = get_name(pos)
    birth_date = get_birth_date(act_date)
    salary = get_salary(pos, act_date, act_date, l_drivers, l_logistics)
    phone_number = floor(500000000 + 300000000 * rand())
    employment_date = act_date
    if pos == 'boss':
        release_date = None
    else:
        release_date = employment_date + timedelta(days = 10 + 30 * expon.rvs(scale = 70))
        pension_date = birth_date + timedelta(days = 365 * 65)
        if release_date > pension_date:
            release_date = pension_date
        if release_date > date.today():
            release_date = None
    return [name, pos, birth_date, salary, phone_number, employment_date, release_date]

###########################
###      job offer      ###
###########################

class Job_offer():
    ''' Job offer that will hire new person in few days'''
    def __init__(self, pos, act_date, company):
        self.pos = pos
        self.expire = act_date + timedelta(days = 3 * 10 ** rand())
        self.company = company
    
    def update(self, act_date):
        if act_date >= self.expire:
            self.company.employees.loc[len(self.company.employees)]=pd.Series(make_employee(self.pos, act_date, self.company.l_drivers, self.company.l_logistics)).values
            self.company.job_offers.remove(self)
            if self.pos == 'accountant':
                self.company.l_accountants += 1
                self.company.o_accountants -= 1
            elif self.pos == 'driver':
                self.company.l_drivers += 1
                self.company.o_drivers -= 1
            elif self.pos == 'logistic':
                self.company.l_logistics += 1
                self.company.o_logistics -= 1
            elif self.pos == 'phisic_worker':
                self.company.l_phisic_workers += 1
                self.company.o_phisic_workers -= 1

###########################
###     offer making    ###
###########################

def make_offers_if_needed(comp, act_date):
    ''' Make job offer f needed'''
    if comp.plan_accountants > comp.l_accountants + comp.o_accountants:
        comp.job_offers.append(Job_offer('accountant', act_date, comp))
        comp.o_accountants += 1
    if comp.plan_drivers > comp.l_drivers + comp.o_drivers:
        comp.job_offers.append(Job_offer('driver', act_date, comp))
        comp.o_drivers += 1
    if comp.plan_logistics > comp.l_logistics + comp.o_logistics:
        comp.job_offers.append(Job_offer('logistic', act_date, comp))
        comp.o_logistics += 1
    if comp.plan_phisic_workers > comp.l_phisic_workers + comp.o_phisic_workers:
        comp.job_offers.append(Job_offer('physic worker', act_date, comp))
        comp.o_phisic_workers += 1

###########################
###   employee release  ###
###########################

def delete_employee_when_released(comp, act_date):
    ''' Delete employee when released'''
    for i in range(len(comp.employees)):
        release_date = comp.employees.loc[i]['Release Date']
        if not release_date is None and release_date == act_date:
            position = comp.employees.loc[i]['Position']
            if position == 'accountant':
                comp.l_accountants -= 1
            elif position == 'driver':
                comp.l_drivers -= 1
            elif position == 'logistic':
                comp.l_logistics -= 1
            else:
                comp.l_phisic_workers -= 1

###########################
###    employee plan    ###
###########################

def add_driver(comp, act_date):
    '''Add driver and other things when needed'''
    comp.plan_drivers += 1
    if comp.plan_drivers > comp.plan_phisic_workers * 3:
        comp.plan_phisic_workers += 1
    if comp.plan_drivers > comp.plan_logistics * 7:
        comp.plan_logistics += 1
    if comp.plan_drivers > comp.plan_accountants * 15:
        comp.plan_accountants += 1
    make_car(comp, act_date)