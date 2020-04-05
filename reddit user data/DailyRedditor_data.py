import praw, time, datetime, json, os

reddit = praw.Reddit(client_id='n1WIc796crv1mQ',
                     client_secret='l2ZeRpYtZLl8gOQp-xILlOXiGHM',
                     user_agent='RedditAnalysis2')
# reddit api access 

def unix_to_datetime(unix_time):
    """ FUNCTION:
    Input = unix time, returns a date and hhmmss string, used for daily file names"""
    normal_time = datetime.datetime.fromtimestamp(int(unix_time)).strftime('%d_%m_%Y_%H')
    return normal_time

def what_month_time(time_str):
    '''This function returns a tuple with the month and hour of a submission or comment'''
    time_str = time_str.split('_')
    return int(time_str[1]), int(time_str[3])

class DailyRedditorData:
    '''A class for easier access of Redditor data.'''

    def __init__(self, username):
        self.username = username
        instance = reddit.redditor(username)
        self.ck = instance.comment_karma  # comment karma
        self.pk = instance.link_karma  # link or post karma
        self.pr = instance.is_gold  # boolean for if the user has premium
        self.mo = instance.is_mod  # boolean for if the user is a mod
        self.co = len(list(instance.comments.new(limit=None)))  # number of comments
        self.po = len(list(instance.submissions.new(limit=None)))  # number of posts
        self.comments = instance.comments # creates a comments instance

def main(user_list, sub_name):
    '''This function saves the sought after data of a user to a dictionary, where its key is the present day,
    and its value is another dictionary. This second dictionary contains the data we are fetching as its keys,
    and then their values are lists of data. Indexes of the lists are related to each other.
    Example: list_of_users[i] ~ list_of_comment_karma[i]; where '~' denotes a relation.'''

    time_today = str(unix_to_datetime(int(time.time())))[:10] # day of data extraction
    data_dict = { # structured dictionary for saving data
        'users':[],
        'com karma':[],
        'pos karma':[],
        'premium':[],
        'mod':[],
        'num posts':[]
    }
    n = 0 # positional counter

    for user in user_list:
        try:
            instance = DailyRedditorData(user)
            data_dict['users'].append(user) # append user
            data_dict['com karma'].append(instance.ck) # append comment karma
            data_dict['pos karma'].append(instance.pk) # append post karma
            data_dict['premium'].append(instance.pr) # append if premium
            data_dict['mod'].append(instance.mo) # append if mod
            data_dict['num posts'].append([(instance.co, instance.po),[], 0,[ [],[] ] ])
                # append a list; 1st element is a tuple

            instance_2 = instance.comments # creates a sublisting generator for comments from reddit user object
            comments = list(instance_2.new(limit=None)) # list of comment objects
            x = 0 # counter for comments above 1000 upvotes

            for item in comments:
                if item.score > 1000: x += 1 # adds 1 to comment counter

                subreddit = item.subreddit # create subreddit instance from comment object
                if subreddit.display_name in data_dict['num posts'][n][3][0]:
                    # check if name of subreddit is in dictionary
                    index = data_dict['num posts'][n][3][0].index(subreddit.display_name) # add the name to dictionary
                    data_dict['num posts'][n][3][1][index] += 1 # number of occurences of commenting in subreddit
                    # in other words: frequency of posting in subreddit
                else:
                    data_dict['num posts'][n][3][0].append(subreddit.display_name) # appends name of commented subreddit
                    data_dict['num posts'][n][3][1].append(0) # appends counter for frequency of posting in subreddit

                created = what_month_time(unix_to_datetime(item.created_utc)) # tuple with 1st element being month
                # 2nd element being hour posted
                data_dict['num posts'][n][1].append(created) # add time and hour posted to dictionary

            data_dict['num posts'][n][2] = x # add number of comments above 1000 upvotes to dictionary
            n += 1 # increase positional counter
        except:
            n += 1

    with open('u_' + time_today + sub_name, 'w') as fp: # dump collected data into .json file
        json.dump(data_dict, fp, indent=4)

path = '' # path where .py file is located
os.chdir(path)
for file in os.listdir(path):
    ext = os.path.splitext(file)[-1].lower()
    ext_n = os.path.splitext(file)[0]
    if ext == '.json' and counter == 1:
        file = json.load(open(file,'r'))
        main(file["username"], ext_n)

# tabulacija498%&/