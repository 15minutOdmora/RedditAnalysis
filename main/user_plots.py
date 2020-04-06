import os, json, math
import matplotlib.pyplot as plt
import numpy as np

def general_commons(graph_list):
    ''' Plots selected histogram of connections between specific subreddits '''

    titles = {'advice_bros1': 'AdviceAnimals vs AnimalsBeingBros',
              'cats_memes1': 'cats vs dankmemes',
              'gw_atheism1': 'gonewild vs atheism',
              'swhores_art1': 'StarWars vs Art',
              'syd_germoney1': 'Sydney vs Germany',
              'tt_iphone1': 'TittyDrop vs iphone'}

    some_dict = graph_list[1]
    x_names = list(some_dict.keys())
    y_num = list(some_dict.values())

    plt.figure(figsize=(21,6))
    plt.bar(x_names, y_num)
    plt.ylabel('Number of connections')
    plt.xlabel('Subreddits most in common')
    plt.title(titles[graph_list[0]])
    plt.show()

def top_14_plot(key):
    '''Plots top 14 visited subreddits from users of a specific subreddit'''

    data = json.load(open('top_14', 'r'))
    plot = data[key] # dictionary of top 14 visited subreddits

    plt.figure(figsize=(21,6))
    y_pos = np.arange(14)
    plt.bar(y_pos, list(plot.values()))
    plt.ylabel('Number of visits')
    plt.title(key)
    plt.xticks(y_pos, list(plot.keys()))
    plt.show()

def histogram(mod_plots, prem_plots, both):
    '''This function creates a histogram for premium and mod, percentwise'''
    percent = 100/len(data['is_premium'])
    histo = [prem_plots*percent, mod_plots*percent, (len(data['is_premium']) - prem_plots - mod_plots - both
                                                                   )*percent, both*percent, ]
    # list of data to be displayed in histogram

    plt.figure(figsize=(15,7))
    plt.bar(['Users with premium', 'Users that are mods', 'Normal users', 'Users that are mods and have premium'], histo)
    # premium, mod, both and normal add up to represent 100% of the users looked at
    plt.ylabel('Percent of users')
    plt.title('Ratio of users that are mods, have premium, are both and those without any')
    plt.show()

def all_users(data):
    '''Return number of all users looked at'''
    print('\n', len(data['is_premium']))

with open('non_relational', 'r') as fp:
    data = json.load(fp)

# histogram data
mod_plots, prem_plots, both = 0, 0, 0
for item1, item2 in zip(data['is_mod'], data['is_premium']):
    # checks if users have premium or are mods, or both
    # adds it to variables used in plotting
    if item1 == True and item1 == item2:
        both += 1
    elif item1 == True:
        mod_plots += 1
    elif item2 == True:
        prem_plots += 1
    else:
        pass
