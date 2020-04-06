import praw
import prawcore
import json
import os
from reading_daily_data import SubredditData

# Initializing the API
reddit = praw.Reddit(client_id='g5oHfBMlowm7oQ',
                     client_secret='MX-BmHukfZxZY4jf1-ZFA8IcdA4',
                     user_agent='RedditAnalysis by u/Adarkcid')

print(reddit.user.me())
print(reddit.read_only) # Test if working(prints True)

# We use the SubreddiData class to read, preview, and save all data
def main(list_of_subs):
    counter = 1
    did_not_read = list()
    # Path below is for Adarkcid's pc
    new_path = r'C:\Users\laptop\Desktop\RedditAnalysis\RedditAnalysis\TopAllTime'
    if not os.path.exists(new_path):
        os.makedirs(new_path)

    for key, value in list_of_subs.items():
        for sub in value:

            subreddit = sub[0]
            try:
                test = reddit.subreddit(subreddit)  # Tests if the sub name is valid
            except prawcore.exceptions.ServerError as e:
                did_not_read.append(sub)
                continue

            data = SubredditData(subreddit, 'all')  # Creates instance for the subreddit
            data.fetching_data()
            data.data_preview_txt(counter, new_path)  # Creates a prevew .txt file
            data.saving_data_to_json(counter, new_path)  # Saves the data to a .jsom file

            # Test: Prints all data of the instance
            '''temp = vars(data)
            for item in temp:
                print(item , ' : ' , temp[item])
            '''
            del data
            counter += 1

            print('did_not_read: ' + str(did_not_read))

if __name__ == '__main__':
    '''list_of_subs = {'normal': [['natureismetal', 100, 100000]]}
    main(list_of_subs)
    time.sleep(2)'''
    f = open('subreddit_dict_fin.json')
    list_of_subs = json.load(f)
    main(list_of_subs)
    f.close()
