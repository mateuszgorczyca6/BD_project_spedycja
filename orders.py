import pandas as pd

###########################
###       product       ###
###########################

products = pd.read_csv('data/products.csv', index_col = 0)
products.fillna('', inplace = True)
prod_list = products.index.values.tolist()
print(products)

###########################
###      distance       ###
###########################

distances = pd.read_csv('data/cities_dist.csv', index_col = 0)

def get_distance(city1, city2):
    '''Return distance between cities'''
    return distances.loc[city1][city2]

cities = list(distances.columns)



def make_order(comp, act_date):
    '''
    'Product', 'Origin', 'Destination', 'Distance', 'Special Treatment', 'Price', 'Mass', 'Date'
    '''