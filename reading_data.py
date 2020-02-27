import praw
import json
import datetime
import time

# Initializing the API
reddit = praw.Reddit(client_id='',
                     client_secret='',
                     user_agent='')
print(reddit.read_only) # Test if working(prints True)

def unix_to_utc(unix_time):
    ''' FUNCTION:
    Input = unix time, returns a touple = ([day, month, year]], seconds_in_a_day),
    range from 0 - 86399, 86400s in one day'''
    normal_time = [int(i) for i in datetime.datetime.fromtimestamp(int(unix_time)).strftime('%d %m %Y %H %M %S').split(' ')]
    return (normal_time[:3], normal_time[3] * 3600 + normal_time[4] * 60 + normal_time[5])

class DailySubredditData:
    def __init__(self, name):
        self.name = name
        # Following lists contain below mentioned data from each post
        # where the first added post is on the 0 index
        self.upvotes = []           # number of upvotes
        self.ud_ratio = []          # percentage of upvotes out of (upvotes + downvotes)
        self.comments = []          # number of comments
        self.awards = [[], [], []]  # on index(number of): 0 = silver, 1 = gold, 2 = platinum
        self.u_top10_comments = []  # list will contain lists of lenght 10 where each i- th number is
                                    # the number of upvotes the i-th top level comment got
        self.uc_ratio = []          # upvote/comment ratio
        self.title_length = []      # the length of the title number of words [num. of words, length(str)]
        self.time = []              # time at wich the post was submitted
        self.username = []          # username(lol)
        self.current_time = int(time.time())

    def is_in_time_range(self, unix_time):
        """ FUNCTION:
        Checks if the time is in the in the time range (self.current_time - 32h , self.current_time - 8)"""
        if self.current_time - 115200 <= unix_time < self.current_time - 28800:
            return True
        else:
            return False

    def fetching_data(self):
        curent_time = 0
        ''' METHOD: retrieves data from 24h(-32h to -8h) and saves the data to the self.variables'''
        for submission in reddit.subreddit(self.name).top(time_filter='week'):
            if self.is_in_time_range(int(submission.created_utc)):
                print(submission.score, submission.num_comments) # Test
                # todo saving to the variables , fetching data...
            else:
                pass
            # print(datetime.datetime.fromtimestamp(int(submission.created_utc)).strftime('%d-%m-%Y %H:%M:%S'))
            # Testing to print the date time out the top posts from past 1 hour which is converted from Unix time

data = DailySubredditData('learnpython')
data.fetching_data()
