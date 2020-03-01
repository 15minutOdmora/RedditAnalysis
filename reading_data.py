import praw
import json
import datetime
import time
import math

# Initializing the API
reddit = praw.Reddit(client_id='',
                     client_secret='',
                     user_agent='')
print(reddit.read_only) # Test if working(prints True)

def unix_to_utc(unix_time):
    """ FUNCTION:
    Input = unix time, returns a touple = ([day, month, year], seconds_in_a_day),
    range from 0 - 86399, 86400s in one day"""
    normal_time = [int(i) for i in datetime.datetime.fromtimestamp(int(unix_time)).strftime('%d %m %Y %H %M %S').split(' ')]
    return (normal_time[:3], normal_time[3] * 3600 + normal_time[4] * 60 + normal_time[5])

class DailySubredditData:
    def __init__(self, name, period):
        self.name = name
        self.period = period          # String of the time range we want to analyse
        # Following lists contain below mentioned data from each post
        # where the first added post is on the 0 index
        self.upvotes = []             # number of upvotes
        self.ud_ratio = []            # percentage of upvotes out of (upvotes + downvotes)
        self.comments = []            # number of comments
        self.awards = [[], [], []]    # on index(number of): 0 = silver, 1 = gold, 2 = platinum
        self.u_top10_comments = []    # list will contain lists of lenght 10 where each i- th number is
                                      # the number of upvotes the i-th top level comment got,
                                      # 0 index is the number of top level comments
        self.uc_ratio = []            # upvote/comment ratio
        self.title_length = [[], []]   # the length of the title number of words [num. of words, length(str)]
        self.time = []                # time at which the post was submitted
        self.username = []            # all the usernames of the posts posted in sub.
        self.oc = []                  # list of true,false weather the submission was marked original content
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
        """ METHOD: 
        retrieves data from 24h(-32h to -8h) and saves the data to the self.variables,
        Idea: We can change the search time to 'day', 'week', 'month'. changing the variable self.period """
        counter = 0
        for submission in reddit.subreddit(self.name).top(time_filter=self.period):
            if self.is_in_time_range(int(submission.created_utc)):
                num_upvotes, num_comments = submission.score, submission.num_comments
                self.upvotes.append(num_upvotes)
                self.comments.append(num_comments)
                self.ud_ratio.append(submission.upvote_ratio)
                self.time.append(int(submission.created_utc))
                self.oc.append(submission.is_original_content)

                try:
                    self.username.append(submission.author.name)
                except:
                    self.username.append(None)

                try:
                    self.uc_ratio.append(round(num_upvotes/num_comments))
                except:
                    self.uc_ratio.append(None)

                # Top-level comments, curr. top 10
                self.u_top10_comments.append([len(submission.comments)])
                if len(submission.comments) > 0:
                    print(len(submission.comments), '*****', num_comments)
                    for i in range(len(submission.comments) - 1):
                        if i >= 10: break
                        print(submission.comments[i].score, '+')
                        self.u_top10_comments[counter -1].append(submission.comments[i].score) #todo nedela

                # Awards
                if len(submission.gildings) > 0:
                    for award, index in {'gid_1': 0, 'gid_2': 1 , 'gid_3': 2}.items(): # silver, gold, plat respectively
                        try: self.awards[index].append(submission.gildings[award])
                        except: self.awards[index].append(0)
                else:
                    for i in range(3): self.awards[i].append(0)

                # Title lengths
                title_str = submission.title
                self.title_length[0].append(len(title_str.split(' ')))
                self.title_length[1].append(len(title_str))


            counter += 1
            if counter > 5: break  # Testing purpose
        print('Finished scraping: ', self.name)

    def data_preview_txt(self):
        """todo METHOD: Saves the daily average data in a .txt file"""
        datetime = [unix_to_utc(self.current_time - 115200), unix_to_utc(self.current_time - 28800)]
        avg_upvotes = round(sum(self.upvotes)/len(self.upvotes), 2)
        avg_comments = round(sum(self.comments)/len(self.comments), 2)
        avg_ud_ratio = round(sum(self.ud_ratio)/len(self.ud_ratio), 2)
        avg_uc_ratio_1 = round(sum(self.upvotes)/sum(self.comments), 2)
        avg_uc_ratio_2 = round(sum(self.uc_ratio)/len(self.uc_ratio), 2)
        num_of_oc_content = sum(self.oc)

        #avg_u_top10_comments,      avg. of the top 3 top comm.
        avg_per_post = [round(sum(sorted([a[b] for b in range(1, len(a))])[:2])/3, 2) for a in self.u_top10_comments]
        print(avg_per_post)

    def saving_data_to_json(self):
        """todo METHOD: Saves the daily data to a .json file"""

class DailyRedditorData:
    def __init__(self, username):
        self.username = username
    #todo Class to read daily redditor data


list_of_subs = ['natureismetal']

def main():
    for sub in list_of_subs:
        data = DailySubredditData(sub,'day')
        data.fetching_data()

        # Test: Prints all data of the instance
        temp = vars(data)
        for item in temp:
            print(item , ' : ' , temp[item])

        del data
main()
