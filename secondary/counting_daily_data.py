import json
import numpy as np
import os
import os.path
import datetime


def unix_to_utc(unix_time):
    """ FUNCTION:
    Input = unix time, returns a touple = ([day, month, year], seconds_in_a_day),
    range from 0 - 86399, 86400s in one day"""
    list_time = datetime.datetime.fromtimestamp(int(unix_time)).strftime('%d %m %Y %H %M %S').split(' ')
    normal_time = [int(i) for i in list_time]
    return normal_time[:3], normal_time[3] * 3600 + normal_time[4] * 60 + normal_time[5]


def seconds_to_hours(sec):
    """ FUNCTION:
    Input= seconds in that particular day, returns the hour"""
    return (sec // 60) // 60


def seconds_to_20min(sec):
    """ FUNCTION:
        Input= seconds in that particular day, returns the 20minutes of the day"""
    return (sec // 60) // 20


class CountingData:
    def __init__(self, subreddit_save_path, all_of_data_save_path):
        # Saving directories
        self.sub_save_path = subreddit_save_path
        self.all_of_data_save_path = all_of_data_save_path
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
        # Title length: char intervals are by 5 (0-5, ... 295-300+), word intervals are by numbers of words (1,...,50+)
        self.title_length_char = np.zeros((2, 60))  # Number of posts in specific title length interval
        self.title_length_word = np.zeros((2, 65))  # 1. = num. of posts, 2. = num of upvotes
        # upvotes to ud_ratio: ud ratio is from (<=0.5,..,1)
        self.up_ud_ratio_corr = np.zeros((2, 50))  # 1. = num. of posts in interval, 2. = num of upvotes
        # upvotes to uc_ratio: intervals by 5 (0-5,..,295-300+):
        self.up_uc_ratio_corr = np.zeros((2, 60))  # 1. = num. of posts in interval, 2. = num of upvotes
        # awards to uc_ratio:
        self.awards_uc = np.zeros((3, 60))        # num of awards in interval, we use the above ones as the x axis
        self.topcom_counter = 0                 # counts the posts that fit in the 100+ upv, 5+ comments category.
        self.topcomupv_to_upv = 0               # upv of post / upv of top comments (adds all of them up)
        self.topcomupv_to_2topcomupv = 0        # upv of top comm / upv of second top comm (adds all up)
        # Upvote freq., how many post are in what upv. interval
        self.upv_freq = np.zeros((1, 100))

    def count_data(self, directory):
        """ METHOD:
        Goes over all the .json files in the 'directory' and adds up the numbers, saves them in the sub.jsons"""
        for file in os.listdir(os.fsencode(directory)):
            filename = os.fsdecode(file)
            if filename.endswith(".json"):
                f = open(directory + '/' + filename)
                sub = json.load(f)

                # If file doesn't exist, open a new .json file for spec. sub and crate the keys, vlues
                if not os.path.exists(self.sub_save_path + r'\{}'.format(filename.lower())):
                    new_sub = dict()
                    new_sub['number_of_submissions'] = 0
                    new_sub['comments'] = 0
                    new_sub['upvotes'] = 0
                    new_sub['ud_ratio'] = 0
                    new_sub['awards'] = [0, 0, 0]
                    new_sub['oc'] = 0
                    new_sub['title_length'] = [0, 0]
                    new_sub['time_freq_hour'] = np.zeros((1, 24)).tolist()
                    new_sub['time_freq_20min'] = np.zeros((1, 72)).tolist()
                    new_sub['time_freq_hour_upv'] = np.zeros((1, 24)).tolist()
                    new_sub['time_freq_20min_upv'] = np.zeros((1, 72)).tolist()
                    new_sub['title_length_char'] = np.zeros((2, 60)).tolist()
                    new_sub['title_length_word'] = np.zeros((2, 65)).tolist()
                    new_sub['up_ud_ratio_corr'] = np.zeros((2, 50)).tolist()
                    new_sub['up_uc_ratio_corr'] = np.zeros((2, 60)).tolist()
                    new_sub['awards_uc'] = np.zeros((3, 60)).tolist()
                    new_sub['topcom_counter'] = 0
                    new_sub['topcomupv_to_upv'] = 0
                    new_sub['topcomupv_to_2topcomupv'] = 0
                    new_sub['upv_freq'] = np.zeros((1, 100)).tolist()
                    # save the sub to a .json
                    with open(self.sub_save_path + r'\{}'.format(filename.lower()), 'w') as fil:
                        json.dump(new_sub, fil)

                # Open the .json for the specific subreddit(as asub).json to add all the counted data
                f = open(self.sub_save_path + r'\{}'.format(filename.lower()))
                new_sub = json.load(f)

                # Add the BD together
                self.number_of_submissions += sub['number_of_submissions']
                new_sub['number_of_submissions'] += sub['number_of_submissions']
                self.comments += sum(sub['comments'])
                new_sub['comments'] += sum(sub['comments'])
                self.upvotes += sum(sub['upvotes'])
                new_sub['upvotes'] += sum(sub['upvotes'])
                self.ud_ratio += sum(sub['ud_ratio'])
                new_sub['ud_ratio'] += sum(sub['ud_ratio'])
                self.awards[0] += sum(sub['awards'][0])
                new_sub['awards'][0] += sum(sub['awards'][0])
                self.awards[1] += sum(sub['awards'][1])
                new_sub['awards'][1] += sum(sub['awards'][1])
                self.awards[2] += sum(sub['awards'][2])
                new_sub['awards'][2] += sum(sub['awards'][2])
                self.oc += sum(sub['oc'])
                new_sub['oc'] += sum(sub['oc'])
                self.title_length[0] += sum(sub['title_length'][0])
                new_sub['title_length'][0] += sum(sub['title_length'][0])
                self.title_length[1] += sum(sub['title_length'][1])
                new_sub['title_length'][1] += sum(sub['title_length'][1])

                # Time freq. per hour, and per 20min, upvotes per 20min
                index = 0
                for submission_time in sub['time']:
                    hour = seconds_to_hours(unix_to_utc(submission_time)[1])
                    self.time_freq_hour[0, hour] += 1
                    new_sub['time_freq_hour'][0][hour] += 1
                    self.time_freq_hour_upv[0, hour] += sub['upvotes'][index]
                    new_sub['time_freq_hour_upv'][0][hour] += sub['upvotes'][index]

                    minute = seconds_to_20min(unix_to_utc(submission_time)[1])
                    self.time_freq_20min[0, minute] += 1
                    new_sub['time_freq_20min'][0][minute] += 1
                    self.time_freq_20min_upv[0, minute] += sub['upvotes'][index]
                    new_sub['time_freq_20min_upv'][0][minute] += sub['upvotes'][index]
                    index += 1

                # Title length in words correlation to upvotes
                index = 0
                for title_words in sub['title_length'][0]:
                    # we subtract one so its the right index in the np. array
                    if title_words >= 65:
                        tit = 64
                    else:
                        tit = title_words - 1
                    self.title_length_word[0, tit] += 1
                    new_sub['title_length_word'][0][tit] += 1
                    self.title_length_word[1, tit] += int(sub['upvotes'][index])
                    new_sub['title_length_word'][1][tit] += int(sub['upvotes'][index])
                    index += 1
                # Title length in characters
                index = 0
                for title_char in sub['title_length'][1]:
                    if title_char >= 300:
                        tit = 59
                    else:
                        tit = (title_char // 5) - 1
                    self.title_length_char[0, tit] += 1
                    new_sub['title_length_char'][0][tit] += 1
                    self.title_length_char[1, tit] += int(sub['upvotes'][index])
                    new_sub['title_length_char'][1][tit] += int(sub['upvotes'][index])
                    index += 1

                # Num. of upvotes per ud_ratio:
                index = 0
                for ud in sub['ud_ratio']:
                    ud_r = int((ud * 100) - 50) - 1
                    if ud_r < 0:
                        ud_r = 0
                    self.up_ud_ratio_corr[0, ud_r] += 1
                    new_sub['up_ud_ratio_corr'][0][ud_r] += 1
                    self.up_ud_ratio_corr[1, ud_r] += int(sub['upvotes'][index])
                    new_sub['up_ud_ratio_corr'][1][0] += int(sub['upvotes'][index])
                    index += 1

                # Num. of upvotes per uc_ratio and number of awards per uc.ratio:
                index = 0
                for up in sub['upvotes']:
                    com = sub['comments'][index]
                    if up <= 0 or com == 0:
                        index += 1
                        continue
                    uc_ratio = (up / com)
                    if uc_ratio >= 300:
                        uc_ratio = 59
                    uc_ratio = int((uc_ratio // 5) - 1)
                    self.up_uc_ratio_corr[0, uc_ratio] += 1
                    new_sub['up_uc_ratio_corr'][0][uc_ratio] += 1
                    self.up_uc_ratio_corr[1, uc_ratio] += sub['upvotes'][index]
                    new_sub['up_uc_ratio_corr'][1][uc_ratio] += sub['upvotes'][index]

                    # Add the number of awards into each interval of the uc_ratio intervals
                    self.awards_uc[0, uc_ratio] += sub['awards'][0][index]
                    new_sub['awards_uc'][0][uc_ratio] += sub['awards'][0][index]
                    self.awards_uc[1, uc_ratio] += sub['awards'][1][index]
                    new_sub['awards_uc'][1][uc_ratio] += sub['awards'][1][index]
                    self.awards_uc[2, uc_ratio] += sub['awards'][2][index]
                    new_sub['awards_uc'][2][uc_ratio] += sub['awards'][2][index]

                    # Top voted comment upvotes divided by the posts upvotes, added up
                    if up >= 100 and len(sub['u_top10_comments'][index]) >= 5:
                        if not sorted(sub['u_top10_comments'][index])[::-1][1] > 0:
                            continue
                        maxcomentupv_div_upv = round(max(sub['u_top10_comments'][index]) / up, 5)
                        self.topcomupv_to_upv += maxcomentupv_div_upv
                        new_sub['topcomupv_to_upv'] += maxcomentupv_div_upv

                        # Top voted comm. / second top voted comm.
                        sorted_list = sorted(sub['u_top10_comments'][index])[::-1]
                        maxcomupv_to_2maxcomupv = round(sorted_list[0]/sorted_list[1], 5)
                        self.topcomupv_to_2topcomupv += maxcomupv_to_2maxcomupv
                        new_sub['topcomupv_to_2topcomupv'] += maxcomupv_to_2maxcomupv

                        self.topcom_counter += 1
                        new_sub['topcom_counter'] += 1

                    # Upv. frequency, how many posts fall in the upv. interval
                    if up <= 50:
                        self.upv_freq[0, 0] += 1
                        new_sub['upv_freq'][0][0] += 1
                    elif 50 < up <= 100:
                        self.upv_freq[0, 1] += 1
                        new_sub['upv_freq'][0][1] += 1
                    elif 100 < up <= 250:
                        self.upv_freq[0, 2] += 1
                        new_sub['upv_freq'][0][2] += 1
                    elif 250 < up <= 500:
                        self.upv_freq[0, 3] += 1
                        new_sub['upv_freq'][0][3] += 1
                    elif 500 < up <= 1000:
                        self.upv_freq[0, 4] += 1
                        new_sub['upv_freq'][0][4] += 1
                    elif up >= 95000:
                        self.upv_freq[0, 99] += 1
                        new_sub['upv_freq'][0][99] += 1
                    else:
                        interval = (up // 1000) + 4
                        self.upv_freq[0, interval] += 1
                        new_sub['upv_freq'][0][interval] += 1
                    index += 1
                # Save the data to the sub. dictionary
                with open(self.sub_save_path + r'\{}'.format(filename.lower()), 'w') as fil:
                    json.dump(new_sub, fil)

    def save_data_to_json(self):
        all_data = dict()
        all_data['number_of_submissions'] = self.number_of_submissions
        all_data['comments'] = self.comments
        all_data['upvotes'] = self.upvotes
        all_data['ud_ratio'] = self.ud_ratio
        all_data['awards'] = self.awards.tolist()
        all_data['oc'] = self.oc
        all_data['title_length'] = self.title_length.tolist()
        all_data['time_freq_hour'] = self.time_freq_hour.tolist()
        all_data['time_freq_20min'] = self.time_freq_20min.tolist()
        all_data['time_freq_hour_upv'] = self.time_freq_hour_upv.tolist()
        all_data['time_freq_20min_upv'] = self.time_freq_20min_upv.tolist()
        all_data['title_length_char'] = self.title_length_char.tolist()
        all_data['title_length_word'] = self.title_length_word.tolist()
        all_data['up_ud_ratio_corr'] = self.up_ud_ratio_corr.tolist()
        all_data['up_uc_ratio_corr'] = self.up_uc_ratio_corr.tolist()
        all_data['awards_uc'] = self.awards_uc.tolist()
        all_data['topcom_counter'] = self.topcom_counter
        all_data['topcomupv_to_upv'] = self.topcomupv_to_upv
        all_data['topcomupv_to_2topcomupv'] = self.topcomupv_to_2topcomupv
        all_data['upv_freq'] = self.upv_freq.tolist()
        # Save the data from instance to a .json
        with open(self.all_of_data_save_path + r'\all_sub_data.json', 'w') as file:
            json.dump(all_data, file)


def main(data_files, sub_save, all_save):
    """Method:
        Creates an instance and runs over the files"""
    a = CountingData(sub_save, all_save)
    for file in data_files:
        a.count_data(r'C:\Users\laptop\Desktop\RedditAnalysis\RedditAnalysis\data\{}'.format(file))
        print(file + ' Finished.')
    a.save_data_to_json()  # Save all the data to a .json

    # Print the data from the instance as preview
    temp = vars(a)
    for item in temp:
        print(item, ' : ', temp[item])

# Data files from which we read the subreddit data
date_files = ['08_03_2020_14', '09_03_2020_19', '10_03_2020_20', '11_03_2020_17', '12_03_2020_20', '13_03_2020_20',
              '14_03_2020_19', '15_03_2020_19', '16_03_2020_23', '17_03_2020_20', '18_03_2020_18']

# Path where we save the counted data
save_path = r'C:\Users\laptop\Desktop\RedditAnalysis\RedditAnalysis\counted_data'

if __name__ == '__main__':
    main(date_files, save_path, save_path)
