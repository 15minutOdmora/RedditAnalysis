import os, json

def main():
    '''This function extracts the user data which DailyRedditor_data gathered from reddits API
    In its current form, the program extracts only booleans for mods and premium, and posts by month.
    If data from DailyRedditor_data.py was to be extracted in its full form, the generated files would include
    all of the data written in the code.
    Relational data was extracted from select subreddits over a span of 8 days.
    Some data was thrown away, as it was deemed useless.'''

    files = list()
    path = 'C:/Users/U2/Desktop/analysis fin/sorting data for plots'
    data_points = {
        'is_mod': [],
        'is_premium': [],
        'posts_1k': 0,
        'com_karm': 0,
        'pos_karm': 0,
        'po_hour': [0 for x in range(25)],
        'po_mont': [0 for x in range(13)],
        'users': []
    }
    relational_data = dict() # data to be used in plotting would be relational graphs
    names = [] # list of usernames used in loop for dictionary creation

    for file in os.listdir(path):
        if file.startswith('u_'): # loads pregenerated files and appends them for use
            names.append(file.split('_')[-1])
            with open(file, 'r') as f:
                data = json.load(f)
                files.append(data)

    for name in names: # creates a dictionary with usernames as its keys. Values are different karmas, facts if premium
        # or mod
        relational_data[name] = dict()
    i = 0 # counter for reading different dictionaries
    l = 0 # counter for creating user based dictionary

    for dictionary in files:
        for c_karma in dictionary['com_karm']: # append comment karma
            data_points['com_karm'] += c_karma
        for p_karma in dictionary['pos karma']: # append post karma
            data_points['pos_karm'] += p_karma
        for premium in dictionary['premium']: # append boolean if premium
            data_points['is_premium'].append(premium)
        for mod in dictionary['mod']: # append boolean if mod
            data_points['is_mod'].append(mod)
        for name in dictionary['users']: # append username
            data_points['users'].append(name)

        for item in dictionary['num posts']:
            data_points['com_karm'] += item[0][0] # adds up all comment karma
            data_points['pos_karm'] += item[0][1] # adds up all post karma
            for tuple in item[1]:
                data_points['po_mont'][tuple[0]] += 1 # adds occurence of post for month related post analysis
                # for example: tuple[0] is 12, the month of december
                data_points['po_hour'][tuple[1]] += 1
                # tuple[1] is 16, time of day when comment was posted
            data_points['posts_1k'] += item[2] # adds up all comments above 1000 karma
            relational_data[names[i]].update({data_points['users'][l]: item[3]})
            # adds data to be used in relational plotting
            # structure of saved data:
            # {name of subreddit: {username: [ [visited subreddits], [frequency of posting in subreddits]]}}
             # the indexes of subreddits and frequency of posting match
            l += 1
        i += 1

    with open('non_relational', 'w') as fp:
        json.dump(data_points, fp, indent=4)
    with open('relational', 'w') as fp:
        json.dump(relational_data, fp, indent=4)

#main()

