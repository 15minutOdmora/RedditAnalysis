import praw
import prawcore
import json
import datetime
import time
import os

# Initializing the API
reddit = praw.Reddit(client_id='g5oHfBMlowm7oQ',
                     client_secret='MX-BmHukfZxZY4jf1-ZFA8IcdA4',
                     user_agent='RedditAnalysis by u/Adarkcid')
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
        Checks if the time is oldar then -4h"""
        if unix_time < self.current_time - 14400:
            return True
        else:
            return False

    def fetching_data(self):
        """ METHOD: 
        retrieves data from 24h(-32h to -8h) and saves the data to the self.variables,
        Idea: We can change the search time to 'day', 'week', 'month'. changing the variable self.period """
        counter = 0
        print(str(self.name) + ' scraping data ... ', end='')
        for submission in reddit.subreddit(self.name).top(time_filter=self.period):
            counter += 1
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

            if counter > 1500: break  # Testing purpose
        print(' {} submissions read - Finished.'.format(self.number_of_submissions))

    def data_preview_txt(self, counter, path):
        """ METHOD: Saves the daily average data in a .txt file
            just for preview"""
        preview_dict = dict()
        preview_dict['num_of_posts'] = self.number_of_submissions
        preview_dict['datetime'] = [unix_to_utc(self.current_time - 374400), unix_to_utc(self.current_time - 28800)]
        preview_dict['avg_upvotes'] = round(sum(self.upvotes)/len(self.upvotes), 2)
        preview_dict['avg_comments'] = round(sum(self.comments)/len(self.comments), 2)
        preview_dict['avg_ud_ratio'] = round(sum(self.ud_ratio)/len(self.ud_ratio), 2)
        preview_dict['avg_uc_ratio_1'] = round(sum(self.upvotes)/sum(self.comments), 2)
        try:
            preview_dict['avg_uc_ratio_2'] = round(sum(self.uc_ratio)/len(self.uc_ratio), 2)
        except:
            preview_dict['avg_uc_ratio_2'] = 'ned'
        preview_dict['num_of_oc_content'] = sum(self.oc)
        preview_dict['avg_awards'] = [round(sum(a) / len(a), 4) for a in self.awards]
        preview_dict['avg_title_length'] = [round(sum(a) / len(a), 2) for a in self.title_length]
        # avg. of the top 3 top comm.
        per_post_avg_top3c = [round(sum(sorted([b for b in a[1:]])[::-1][:3])/3, 2) for a in self.u_top10_comments]
        # Average in all posts
        preview_dict['avg_u_top10_comments'] = round(sum(per_post_avg_top3c)/len(per_post_avg_top3c), 2)

        # Saving the averages to a .txt file,
        curr_date_time = unix_to_datetime(self.current_time)    # 'dd_mm_yyyy_hh'
        with open(path + '\{}.txt'.format(curr_date_time), 'a') as file:
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

    def saving_data_to_json(self, counter, path):
        """ Saves the daily data to a .json file"""
        sub_dict = dict()
        sub_dict['datetime'] = [self.current_time - 374400, self.current_time - 28800]
        sub_dict['number_of_submissions'] = self.number_of_submissions
        sub_dict['upvotes'] = self.upvotes
        sub_dict['ud_ratio'] = self.ud_ratio
        sub_dict['comments'] = self.comments
        sub_dict['u_top10_comments'] = self.u_top10_comments
        sub_dict['awards'] = self.awards
        sub_dict['uc_ratio'] = self.uc_ratio
        sub_dict['title_length'] = self.title_length
        sub_dict['time'] = self.time
        sub_dict['username'] = self.username
        sub_dict['oc'] = self.oc
        # Save the data to a new json file
        with open(path + '\{}.json'.format(self.name), 'w') as file:
            json.dump(sub_dict, file)
        print(self.name, ' saved to file. ...... {}'.format(counter))

def main(list_of_subs):
    counter = 0
    # Creates a new directory, named as the date and hour the program ran
    curr_time = unix_to_datetime(int(time.time()))   # Path below is for liams pc
    new_path = r'C:\Users\laptop\Desktop\RedditAnalysis\RedditAnalysis\data\{}'.format(curr_time)
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    for key, value in list_of_subs.items():
        if key == 'nsfw':   #todo Some nsfw subs dont exist anymore, fix the list
            pass
        else:
            for sub in value:
                counter += 1
                #if counter < 56: continue
                subreddit = sub[0]
                data = DailySubredditData(subreddit, 'day')  # Creates instance for the subreddit
                data.fetching_data()
                data.data_preview_txt(counter, new_path)    # Creates a prevew .txt file
                data.saving_data_to_json(counter, new_path)   # Saves the data to a .jsom file
                '''
                # Test: Prints all data of the instance
                temp = vars(data)
                for item in temp:
                    print(item , ' : ' , temp[item])
                '''
                del data
                if counter > 500:
                    break

if __name__ == '__main__':
    '''f = open('subreddit_dict2.json')
    list_of_subs = json.load(f)
    main(list_of_subs)
    f.close()'''
    list_of_subs = {'usa': [['kjsbndflhbasd'], ['aww']]}
    main(list_of_subs)



