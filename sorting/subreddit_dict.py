import praw
import json

'''This program sorts looked at subreddits to their respective continents, for the final version of the dictionary
    used in DailyData extraction.'''

reddit = praw.Reddit(client_id='g5oHfBMlowm7oQ',
                     client_secret='MX-BmHukfZxZY4jf1-ZFA8IcdA4',
                     user_agent='RedditAnalysis by u/Adarkcid')

usa = ['NYC', 'Seattle','Chicago', 'Toronto', 'LosAngeles', 'Portland', 'Boston', 'Austin', 'London','SanFrancisco',
       'Vancouver','WashingtonDC','Houston','Atlanta','Philadelphia','Denver','Melbourne', 'SanDiego','Dallas',
       'Montreal', 'Sydney', 'Pittsburgh', 'Calgary','Baltimore','StLouis']

europe = ['Europe', 'Austria', 'Albania', 'Belgium', 'slovenia', 'Bosnia', 'Croatia', 'France', 'Germany', 'Ireland',
          'Italy', 'thenetherlands', 'Serbia', 'unitedkingdom', 'Switzerland', 'Slovakia', 'Russia']


new_usa = [[sub, None, reddit.subreddit(sub).subscribers] for sub in usa]
new_europe = [[sub, None, reddit.subreddit(sub).subscribers] for sub in europe]

f = open(r'C:\Users\laptop\Desktop\RedditAnalysis\RedditAnalysis\sorting\reddit_dict1.json')
dic = json.load(f)

dic["usa"] = new_usa
dic["europe"] = new_europe
f.close()

with open(r'C:\Users\laptop\Desktop\RedditAnalysis\RedditAnalysis\subreddit_dict2.json', 'w') as fi:
    json.dump(dic, fi)

