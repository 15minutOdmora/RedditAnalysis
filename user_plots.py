import os, json, math
import matplotlib.pyplot as plt
import numpy as np

def histogram(mod_plots, prem_plots, both):
    '''This function creates a histogram for premium and mod, percentwise'''
    percent = 100/len(data['is_premium'])
    histo = [prem_plots*percent, mod_plots*percent, both*percent, 100]
    plt.figure(figsize=(15,7))
    plt.bar(['Users with premium', 'Users that are mods', 'Users that are mods and have premium', 'All users'], histo)
    plt.show()

def all_users(data):
    '''Return number of all users looked at'''
    print('\n', len(data['is_premium']))

def graph(data):
    '''This function plots the graph of posts by month'''
    month_x, month_y = [x for x in range(1,13)], data['po_mont']
    plt.figure(figsize=(12,6))
    plt.plot(month_x, month_y)
    plt.ylabel('Number of posts')
    plt.xlabel('Months in year')
    plt.show()

def posts_month(data):
    '''Return posts by month in list'''
    print('\n', data['po_mont'])

with open('non_relational', 'r') as fp:
    data = json.load(fp)

# histogram data
mod_plots, prem_plots, both = 0, 0, 0
for item1, item2 in zip(data['is_mod'], data['is_premium']):
    if item1 == True and item1 == item2:
        both += 1
    elif item1 == True:
        mod_plots += 1
    elif item2 == True:
        prem_plots += 1
    else:
        pass
