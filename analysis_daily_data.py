import json
import numpy as np
import math
import os
import datetime
from matplotlib import pyplot as plt

def unix_to_utc(unix_time):
    """ FUNCTION:
    Input = unix time, returns a touple = ([day, month, year], seconds_in_a_day),
    range from 0 - 86399, 86400s in one day"""
    normal_time = [int(i) for i in datetime.datetime.fromtimestamp(int(unix_time)).strftime('%d %m %Y %H %M %S').split(' ')]
    return (normal_time[:3], normal_time[3] * 3600 + normal_time[4] * 60 + normal_time[5])

def seconds_to_hours(sec):
    """ FUNCTION:
    Input= seconds in that particular day, returns the hour"""
    return (sec // 60) // 60

def seconds_to_20min(sec):
    """ FUNCTION:
        Input= seconds in that particular day, returns the 20minutes of the day"""
    return (sec // 60) // 20

class AllData:
    def __init__(self, filter=None):
        # Count (sum of all):
        self.number_of_submissions = 0
        self.comments = 0
        self.upvotes = 0
        self.ud_ratio = 0
        self.awards = np.array([0, 0, 0])
        self.oc = 0
        self.title_length = np.array([0, 0])
        # Time:                                     # Post freq
        self.time_freq_hour = np.zeros((1, 24))     # 24 intervals by 1hour (ex.: 00-01:00, 01:00-02:00, ...)
        self.time_freq_20min = np.zeros((1, 72))    # 72 intervals by 20minutes (ex.: 00-00:20, 00:20-00:40; ...)
        self.time_freq_hour_upv = np.zeros((1, 24))  # Sum of upvotes per interval
        self.time_freq_20min_upv = np.zeros((1, 72))  # -ll-
        # Title length: char intervals are by 5 (0-10, ... 290-300+), word intervals are by numbers of words (1,...,50+)
        self.title_length_char = np.zeros((2, 60))  # Number of posts in specific title length interval
        self.title_length_word = np.zeros((2, 65))  # 1. = num. of posts, 2. = num of upvotes
        # upvotes to ud_ratio: ud ratio is from (<=0.5,..,1)
        self.up_ud_ratio_corr = np.zeros((2, 50))  # 1. = num. of posts in interval, 2. = num of upvotes
        # upvotes to uc_ratio: intervals by 5 (0-5,..,295-300+):
        self.up_uc_ratio_corr = np.zeros((2, 60))  # 1. = num. of posts in interval, 2. = num of upvotes
        # awards to uc_ratio:
        self.awards_uc = np.zeros((1, 60))        # num of awards in interval, we use the above ones as the x axis

    def count_data(self, directory):
        """ METHOD:_
        Goes over all the .json files in the 'directory' """
        for file in os.listdir(os.fsencode(directory)):
            filename = os.fsdecode(file)
            print(filename)
            if filename.endswith(".json"):
                f = open(directory + '/' + filename)
                sub = json.load(f)

                self.number_of_submissions += sub['number_of_submissions']
                self.comments += sum(sub['comments'])
                self.upvotes += sum(sub['upvotes'])
                self.ud_ratio += sum(sub['ud_ratio'])
                self.awards[0] += sum(sub['awards'][0])
                self.awards[1] += sum(sub['awards'][1])
                self.awards[2] += sum(sub['awards'][2])
                self.oc += sum(sub['oc'])
                self.title_length[0] += sum(sub['title_length'][0])
                self.title_length[1] += sum(sub['title_length'][1])

                # Time freq. per hour, and per 20min, upvotes per 20min
                index = 0
                for submission_time in sub['time']:
                    hour = seconds_to_hours(unix_to_utc(submission_time)[1])
                    self.time_freq_hour[0, hour] += 1
                    self.time_freq_hour_upv[0, hour] += sub['upvotes'][index]
                    minute = seconds_to_20min(unix_to_utc(submission_time)[1])
                    self.time_freq_20min[0, minute] += 1
                    self.time_freq_20min_upv[0, minute] += sub['upvotes'][index]
                    index += 1

                # Title length correlation to upvotes
                index = 0
                for title_words in sub['title_length'][0]:
                    # we subtract one so its the right index in the np. array
                    if title_words >= 65:
                        tit = 64
                    else:
                        tit = title_words - 1
                    self.title_length_word[0, tit] += 1
                    self.title_length_word[1, tit] += int(sub['upvotes'][index])
                    index += 1
                index = 0
                for title_char in sub['title_length'][1]:
                    if title_char >= 300:
                        tit = 59
                    else:
                        tit = (title_char // 5) - 1
                    self.title_length_char[0, tit] += 1
                    self.title_length_char[1, tit] += int(sub['upvotes'][index])
                    index += 1

                # Num. of upvotes per ud_ratio:
                index = 0
                for ud in sub['ud_ratio']:
                    ud_r = int((ud * 100) - 50) - 1
                    if ud_r < 0:
                        ud_r = 0
                    self.up_ud_ratio_corr[0, ud_r] += 1
                    self.up_ud_ratio_corr[1, ud_r] += int(sub['upvotes'][index])
                    index += 1

                # Num. of upvotes per uc_ratio:
                index = 0
                for up in sub['upvotes']:
                    com = sub['comments'][index]
                    if up <= 0 or com == 0:
                        index += 1
                        continue
                    uc_ratio = (up/com)
                    if uc_ratio >= 300:
                        uc_ratio = 59
                    uc_ratio = int((uc_ratio // 5) - 1)
                    self.up_uc_ratio_corr[0, uc_ratio] += 1
                    self.up_uc_ratio_corr[1, uc_ratio] += sub['upvotes'][index]
                    index += 1

                # Num. of awards in correlation to uc_ratio:
                index = 0


a = AllData()
a.count_data(r'C:\Users\laptop\Desktop\RedditAnalysis\RedditAnalysis\data\08_03_2020_14')
a.count_data(r'C:\Users\laptop\Desktop\RedditAnalysis\RedditAnalysis\data\09_03_2020_19')
a.count_data(r'C:\Users\laptop\Desktop\RedditAnalysis\RedditAnalysis\data\10_03_2020_20')
a.count_data(r'C:\Users\laptop\Desktop\RedditAnalysis\RedditAnalysis\data\11_03_2020_17')
a.count_data(r'C:\Users\laptop\Desktop\RedditAnalysis\RedditAnalysis\data\12_03_2020_20')
'''averages20min = []
averageshour = []
for b in range(len(a.time_freq_20min[0])):
    averages20min.append(a.time_freq_20min_upv[0][b]/a.time_freq_20min[0][b])
for c in range(len(a.time_freq_hour[0])):
    averageshour.append(a.time_freq_hour_upv[0][c] / a.time_freq_hour[0][c])'''

'''
print(a.upvotes/a.number_of_submissions)
sez = [x * 3 for x in range(24)]
sez2 = [x for x in range(72)]'''
averages_tit = []
x_ = [x for x in range(len(a.up_uc_ratio_corr[0]))]
for b in range(len(a.up_uc_ratio_corr[0])):
    averages_tit.append(a.up_uc_ratio_corr[1,b]/a.up_uc_ratio_corr[0,b])
print(len(averages_tit), len(x_))
# test plots
plt.style.use('fivethirtyeight')
plt.plot(x_, averages_tit)
plt.show()


# Test: Prints all data of the instance
temp = vars(a)
for item in temp:
    print(item, ' : ', temp[item])

print(a.title_length_char[0, 4])


