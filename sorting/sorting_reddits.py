import json
import praw

list_reddit = {'nsfw': [], 'normal': [], 'usa': [], 'europe': []}
nsfw = []
num = 1
reddit = praw.Reddit(client_id='n1WIc796crv1mQ',
                     client_secret='l2ZeRpYtZLl8gOQp-xILlOXiGHM',
                     user_agent='RedditAnalysis2')

for line in open('nsfw.txt', 'r'):
    line = line.split()
    line = [x.replace('r/', '') for x in line]
    nsfw += line

for line in open('subredditi.txt', 'r'):
    line = line.split()
    name, rank, subs = line[1].replace('/r/',''), int(line[0].replace(',','')), int(line[2].replace(',',''))
    #print(name, rank, subs)
    sub = reddit.subreddit(name)
    #print(sub)
    if num == 1:
        num = 0
    else:
        try:
            if sub.title:
                if name in nsfw:
                    list_reddit['nsfw'] += [[name, rank, subs]]
                else:
                    list_reddit['normal'] += [[name, rank, subs]]
        except:
            pass

with open('reddit_dict88.json', 'w') as fp:
    json.dump(list_reddit, fp, indent = 4)
