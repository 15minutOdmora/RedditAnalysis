import praw
import json
import datetime
import time
import math
import os

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

def unix_to_datetime(unix_time):
    """ FUNCTION:
    Input = unix time, returns a date and hhmmss string, used for daily file names"""
    normal_time = datetime.datetime.fromtimestamp(int(unix_time)).strftime('%d_%m_%Y_%H')
    return normal_time

class DailySubredditData:
    def __init__(self, name, period):
        self.name = name
        self.number_of_submissions = 0  # The number of subissions read
        self.period = period            # String of the time range we want to analyse
        # Following lists contain below mentioned data from each post
        # where the first added post is on the 0 index
        self.upvotes = []               # number of upvotes
        self.ud_ratio = []              # percentage of upvotes out of (upvotes + downvotes)
        self.comments = []              # number of comments
        self.awards = [[], [], []]      # on index(number of): 0 = silver, 1 = gold, 2 = platinum
        self.u_top10_comments = []      # list will contain lists of lenght 10 where each i- th number is
                                        # the number of upvotes the i-th top level comment got,
                                        # 0 index is the number of top level comments
        self.uc_ratio = []              # upvote/comment ratio
        self.title_length = [[], []]    # the length of the title number of words [num. of words, length(str)]
        self.time = []                  # time at which the post was submitted
        self.username = []              # all the usernames of the posts posted in sub.
        self.oc = []                    # list of true,false weather the submission was marked original content
        self.current_time = int(time.time())

    def is_in_time_range(self, unix_time):
        """ FUNCTION:
        Checks if the time is in the in the time range (self.current_time - 32h , self.current_time - 8)"""
        if self.current_time - 115200 <= unix_time < self.current_time - 28800:
            return True
        else:
            return False

    def fetching_data(self):
        """ METHOD: 
        retrieves data from 24h(-32h to -8h) and saves the data to the self.variables,
        Idea: We can change the search time to 'day', 'week', 'month'. changing the variable self.period """
        counter = 0
        print('Scraping data from: ' + self.name , end='')
        for submission in reddit.subreddit(self.name).top(time_filter=self.period):

            if self.is_in_time_range(int(submission.created_utc)):
                print('|', end='')
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

                if num_comments > 0:
                    self.uc_ratio.append(round(num_upvotes/num_comments))
                else:
                    self.uc_ratio.append(None)

                # Top-level comments, curr. top 10
                self.u_top10_comments.append([len(submission.comments)])
                if len(submission.comments) > 0:
                    for i in range(len(submission.comments)):
                        if i >= 10: break
                        self.u_top10_comments[self.number_of_submissions].append(submission.comments[i].score)
                else:
                    self.u_top10_comments[self.number_of_submissions].append(0)

                # Awards
                if len(submission.gildings) > 0:
                    for award, index in {'gid_1': 0, 'gid_2': 1, 'gid_3': 2}.items(): # silver, gold, plat respectively
                        try: self.awards[index].append(submission.gildings[award])
                        except: self.awards[index].append(0)
                else:
                    for i in range(3): self.awards[i].append(0)
                # Title lengths
                title_str = submission.title
                self.title_length[0].append(len(title_str.split(' ')))
                self.title_length[1].append(len(title_str))
                self.number_of_submissions += 1

            counter += 1
            if counter > 5: break  # Testing purpose
        print('  Finished')

    def data_preview_txt(self, counter):
        """ METHOD: Saves the daily average data in a .txt file
            just for preview"""
        preview_dict = dict()
        preview_dict['num_of_posts'] = self.number_of_submissions
        preview_dict['datetime'] = [unix_to_utc(self.current_time - 115200), unix_to_utc(self.current_time - 28800)]
        preview_dict['avg_upvotes'] = round(sum(self.upvotes)/len(self.upvotes), 2)
        preview_dict['avg_comments'] = round(sum(self.comments)/len(self.comments), 2)
        preview_dict['avg_ud_ratio'] = round(sum(self.ud_ratio)/len(self.ud_ratio), 2)
        preview_dict['avg_uc_ratio_1'] = round(sum(self.upvotes)/sum(self.comments), 2)
        preview_dict['avg_uc_ratio_2'] = round(sum(self.uc_ratio)/len(self.uc_ratio), 2)
        preview_dict['num_of_oc_content'] = sum(self.oc)
        preview_dict['avg_awards'] = [round(sum(a) / len(a), 2) for a in self.awards]
        preview_dict['avg_title_length'] = [round(sum(a) / len(a), 2) for a in self.title_length]
        # avg. of the top 3 top comm.
        per_post_avg_top3c = [round(sum(sorted([b for b in a[1:]])[::-1][:3])/3, 2) for a in self.u_top10_comments]
        # Average in all posts
        preview_dict['avg_u_top10_comments'] = round(sum(per_post_avg_top3c)/len(per_post_avg_top3c), 2)

        # Saving the averages to a .txt file,
        curr_date_time = unix_to_datetime(self.current_time)    # 'dd_mm_yyyy_hh'
        with open(curr_date_time + '.txt', 'a') as file:
            if counter == 1:             # If its the first sub we are saving, create the first and second line
                titles = curr_date_time + (15 - len(curr_date_time)) * ' ' + '   '
                for key, value in preview_dict.items():
                    if key in ['datetime', 'avg_awards']:
                        titles += (len(str(value)) - len(key)) * ' ' + key + '   '
                    else:
                        titles += key + '   '

                file.write(titles + '\n')

            dat_str = self.name + (15 - len(self.name)) * ' ' + '   '
            for key, value in preview_dict.items():
                if key in ['datetime', 'avg_awards']:
                    dat_str += str(value) + '   '
                else:
                    dat_str += (len(key) - len(str(value))) * ' ' + str(value) + '   '

            file.write(dat_str + '\n')

    def saving_data_to_json(self):
        """todo METHOD: Saves the daily data to a .json file"""

class DailyRedditorData:
    def __init__(self, username):
        self.username = username
    #todo Class to read daily redditor data

list_of_subs = ['natureismetal', 'TIHI', 'askreddit']

def main():
    counter = 1
    for sub in list_of_subs:
        data = DailySubredditData(sub,'day')
        data.fetching_data()              # Reads data from reddit
        # data.data_preview_txt(counter)    # Creates a prevew .txt file
        '''
        # Test: Prints all data of the instance
        temp = vars(data)
        for item in temp:
            print(item , ' : ' , temp[item])
        '''
        del data
        counter += 1
main()
