import json, os

def incommon_subs_sort(dictionary, name):
    '''Sorts .json file to top 10 with most connections with other subreddit'''

    sorted_incommon = dict()
    some_list = [name]
    # [list(item[0].values()).index(num)]]
    # top_14[item[1]][list(item[0].keys())[list(item[0].values()).index(num)]] = num
    score = sorted(list(dictionary.values()))[::-1][:10]

    for item in score:
        sorted_incommon[list(dictionary.keys())[list(dictionary.values()).index(item)]] = item

    some_list.append(sorted_incommon)

    return some_list

def relation_subs(dictionary1, dictionary2):
    '''Creates a dictionary which contains users of the 1st dictionary as its key, of which value is another dictionary
    that contains users of the other dictionary and the subreddits they have in common.
    Data was discontinued.'''
    incommon = dict()

    for user, user_val in dictionary1.items():
         for user2, user_val2 in dictionary2.items():
            counter = 0
            for subreddit in user_val2[0]:
                if subreddit in user_val[0] and counter == 0: # check if the subreddit is in common and
                    # if this is the first ocurrence
                    incommon[user] = dict()
                    incommon[user][user2] = [subreddit]
                    counter = 1
                elif subreddit in user_val[0] and counter != 0:
                    incommon[user][user2].append(subreddit) # append subreddit in common

    return incommon

def incommon_subs(dictionary1, dictionary2):
    '''This function checks what users in general have in common between 2 subreddits. Dump for .json file for plotting'''
    unique_subs1 = []
    sub_relation = dict()

    for user, user_val in dictionary1.items(): # creates a list of subreddits and checks that they do not duplicate
        for item in user_val[0]:
            if item in unique_subs1:
                pass
            else:
                unique_subs1.append(item)

    for user, user_val in dictionary2.items(): # checks what the two subreddits have in common and the number of times
        # subreddits appear between them among different users
        for item in user_val[0]:
            if item in sub_relation.keys():
                sub_relation[item] += 1
            elif item in unique_subs1:
                sub_relation[item] = 1

    return sub_relation

def frequency(dictionary):
    '''This function creates a dictionary of subreddits and the times users visited them. It counts only the
    subreddits who are visited or rather, commented on >= 10 times. It then adds them up.'''

    subreddits = dict() # the first key of the dictionary is the name of the subreddit looked at

    for key, val in dictionary.items(): # keys are users
        # val = [[reddits], [frequencies]]
        for reddit, freq in zip(val[0], val[1]):
            if reddit in subreddits.keys(): # check if subreddit already in dictionary
                subreddits[reddit] += freq
            elif freq >= 10: # add subreddit which has >= 10 comments or 'visits'
                subreddits[reddit] = freq

    return subreddits

def top_15_sort(list_dict):
    '''Sorts data of select subreddits to top 14 most visited among users. Most visited is based on frequency of posting
    of users in different subreddits they subscribe to. Dumps into .json file.'''

    top_14 = dict()
    score = []

    for item in list_dict:
        score = sorted(list(item[0].values()))[::-1][:14]
        top_14[item[1]] = dict()
        for num in score:
            top_14[item[1]][list(item[0].keys())[list(item[0].values()).index(num)]] = num
            # elegant way of adding score to its subreddit

    with open('top_14', 'w') as f:
        json.dump(top_14, f, indent=4)

def main():
    '''This function takes extracted user data and graphs it in a relation graph.
    Represented data shows which interests users across different subreddits have in common.'''

    data = json.load(open('relational', 'r'))
    subs = list(data.keys())
    freq_list = list()

    for item in subs:
        freq_list.append([frequency(data[item]), item])

    with open('frequency', 'w') as f:
        json.dump(freq_list, f, indent=4)

    '''discontinued data'''
    # tt_iphone = relation_subs(data['TittyDrop'], data['iphone'])
    # gw_atheism = relation_subs(data['gonewild'], data['atheism'])
    # cats_memes = relation_subs(data['cats'], data['dankmemes'])
    # syd_germoney = relation_subs(data['Sydney'], data['Germany'])
    # swhores_art = relation_subs(data['StarWars'], data['Art'])
    # advice_bros = relation_subs(data['AdviceAnimals'], data['AnimalsBeingBros'])

    tt_iphone1 = incommon_subs(data['TittyDrop'], data['iphone'])
    gw_atheism1 = incommon_subs(data['gonewild'], data['atheism'])
    cats_memes1 = incommon_subs(data['cats'], data['dankmemes'])
    syd_germoney1 = incommon_subs(data['Sydney'], data['Germany'])
    swhores_art1 = incommon_subs(data['StarWars'], data['Art'])
    advice_bros1 = incommon_subs(data['AdviceAnimals'], data['AnimalsBeingBros'])

    '''discontinued data'''
    #dump_list = ['tt_iphone', 'gw_atheism', 'cats_memes', 'syd_germoney', 'swhores_art',
                 #'advice_bros']
    dump_list1 = ['tt_iphone1', 'gw_atheism1', 'cats_memes1', 'syd_germoney1', 'swhores_art1',
                 'advice_bros1']

    for item1 in dump_list1:
        with open(item1, 'w') as f:
            json.dump(eval(item1), f, indent=4)

    path = os.getcwd()
    some_list = list()
    for file in os.listdir(path):
        if file.endswith('1'):
            ext = os.path.splitext(file)[0]
            some_list.append(incommon_subs_sort(json.load(open(file, 'r')), ext))

    with open('incommon_sort', 'w') as f:
        json.dump(some_list, f, indent=4)

''' top 15 function dump'''
#data = json.load(open('frequency', 'r'))
#top_15_sort(data)

'''frequency of posting dump'''
#main()