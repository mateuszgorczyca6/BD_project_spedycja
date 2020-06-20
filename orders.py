import pandas as pd
from numpy.random import choice as rand_list
from employees import *

###########################
### product and special ###
###########################

products = pd.read_csv('data/products.csv', index_col = 0)
products.fillna('', inplace = True)
prod_list = products.index.values.tolist()

###########################
### distance and cities ###
###########################

distances = pd.read_csv('data/cities_dist.csv', index_col = 0)

def get_distance(city1, city2):
    '''Return distance between cities'''
    return distances.loc[city1][city2]

cities = list(distances.columns)

###########################
###        price        ###
###########################

def get_price(dist, mass, spec):
    '''Zwraca cenę za zamówienie'''
    bonus = {'': 1, 'fluid': 1.2, 'fridge': 1.3, 'fluid fridge': 1.2 * 1.3}[spec]
    return 35 * (mass * (dist / 100) ** (4/5)) * bonus

###########################
###       client        ###
###########################

def make_client(act_date):
    name, gender = get_name('')
    birth_date = get_birth_date(act_date)
    phone_number = floor(500000000 + 300000000 * rand())
    e_mail = name[:3].lower() + name.split(' ')[1][:3].lower() + str(birth_date.year)[:-2] + '@' + rand_list(['wp.pl', 'o2.pl', 'gmail.com', 'outlook.com', 'tlen.pl'])
    return [name, birth_date, phone_number, e_mail]

def get_client(comp, act_date):
    l_cust = len(comp.clients)
    if rand() < 0.02 or l_cust < 10:
        comp.clients.loc[l_cust] = pd.Series([
            len(comp.clients), *make_client(act_date)
        ]).values
    return rand_list(comp.clients.index.to_list())
    
###########################
###      make order     ###
###########################

def make_order(comp, act_date):
    product = rand_list(prod_list)
    origin = rand_list(cities)
    distance = 0
    while distance == 0:
        destination = rand_list(cities)
        distance = get_distance(origin, destination)
    special_treatment = products.loc[product]['Special treatment']
    mass = floor(50 + 2500 * rand()) / 100
    price = get_price(distance, mass, special_treatment)
    client = get_client(comp, act_date)
    duration = 0.5 + 2 * mass / 30 + 2 * distance / 90
    return [product, origin, destination, distance, special_treatment, duration, mass, price, client]

def take_orders(comp, act_date):
    '''Create orders for today'''
    today_orders = []
    for i in range(floor(1 + rand()) * comp.l_drivers):
        today_orders.append(make_order(comp, act_date))
    '''Get free drivers and cars'''
    free_drivers = comp.actual_drivers[:]
    free_cars = list(comp.cars.index.values)
    while len(today_orders) > 0 and len(free_drivers) > 0:
        prices = [x[7] for x in today_orders]
        price = min(prices)
        for o in today_orders:
            if o[7] == price:
                order = o
        product, origin, destination, distance, special_treatment, duration, mass, price, client = order
        '''selecting cars that are good for this order'''
        good_cars = []
        for car in free_cars:
            if special_treatment in comp.cars.loc[car]['Additional Functionality']:
                if mass <= comp.cars.loc[car]['Capacity']:
                    good_cars.append(car)
        if len(good_cars) == 0: # we can't make that order
            today_orders.remove(order)
        else:  # we are making that order
            good_cars_min_ability = [] # cars that are good and don't have unnecesery additional functionality
            for car in good_cars:
                if comp.cars.loc[car]['Additional Functionality'] == special_treatment:
                    good_cars_min_ability.append(car)
            if good_cars_min_ability == []:
                good_cars_min_ability = good_cars # if there are not that cars we take with unnecesery addi. func.
            '''selecting car with minimum capacity from good cars'''
            capacities = [comp.cars.loc[car]['Capacity'] for car in good_cars_min_ability]
            min_cap = min(capacities)
            # chosen car:
            car = good_cars_min_ability[capacities.index(min_cap)]
            driver = free_drivers[0] # first driver has the best experience
            free_drivers.remove(driver)
            free_cars.remove(car)
            # transactions
            comp.saldo += price
            comp.transactions.loc[len(comp.transactions)] = pd.Series([
                len(comp.transactions), act_date, price, 'Payment for order', price, len(comp.orders)
            ]).values
            # delete order from list and add to history
            comp.orders.loc[len(comp.orders)] = pd.Series([
                len(comp.orders), product, origin, destination, distance, special_treatment, duration, price, mass, act_date, client, driver, car
            ]).values
            today_orders.remove(order)
            # add km to cars
            comp.cars.at[car, 'Last Tanking (km)'] += distance
            if duration < 8: # selecting additional curs if car is good and driver has enought free time
                good_orders = []
                for o in today_orders:
                    if o[5] < 8 - duration and o[4] in comp.cars.loc[car]['Additional Functionality']:
                        if o[6] <= comp.cars.loc[car]['Capacity']:
                            good_orders.append(o)
                if len(good_orders) == 0: # we can't make another order today
                    pass
                else:
                    prices = [x[7] for x in good_orders]
                    price = min(prices)
                    for o in good_orders:
                        if price == o[7]:
                            order = o
                    product, origin, destination, distance, special_treatment, duration, mass, price, client = order
                    # transactions
                    comp.saldo += price
                    comp.transactions.loc[len(comp.transactions)] = pd.Series([
                        len(comp.transactions), act_date, price, 'Payment for order', price, len(comp.orders)
                    ]).values
                    # delete order from list and add to history
                    comp.orders.loc[len(comp.orders)] = pd.Series([
                        len(comp.orders), product, origin, destination, distance, special_treatment, duration, price, mass, act_date, client, driver, car
                    ]).values
                    today_orders.remove(order)
                    # add km to cars
                    comp.cars.at[car, 'Last Tanking (km)'] += distance



