import praw
import json
import datetime

# Initializing the API
reddit = praw.Reddit(client_id='***************',
                     client_secret='******************',
                     user_agent='****************')
print(reddit.read_only) # Test if working(prints True)


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

    def fetching_data(self):
        curent_time = 0
        ''' METHOD: retrieves data from 24h(-32h to -8h) and saves the data to the self.variables'''
        for submission in reddit.subreddit(self.name).top(time_filter='hour'):
            print(datetime.datetime.fromtimestamp(int(submission.created_utc)).strftime('%Y-%m-%d %H:%M:%S'))
            # Testing to print the date time ot the top posts from past 1 hour which is converted from Unix time

data = DailySubredditData('aww')
data.fetching_data()
