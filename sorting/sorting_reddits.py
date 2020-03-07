import json

list_reddit = {'nsfw': [], 'normal': [], 'usa': [], 'europe': []}
nsfw = []
num = 1

for line in open('nsfw.txt', 'r'):
    line = line.split()
    line = [x.replace('r/', '') for x in line]
    nsfw += line

for line in open('subredditi.txt', 'r'):
    line = line.split()
    if num == 1:
        num = 0
    elif line[1].strip('/r/') in nsfw:
        list_reddit['nsfw'] += [[line[1].strip('/r/'), int(line[0].replace(',','')), int(line[2].replace(',',''))]]
    else:
        list_reddit['normal'] += [[line[1].strip('/r/'), int(line[0].replace(',','')), int(line[2].replace(',',''))]]

with open('reddit_dict1.json', 'w') as fp:
    json.dump(list_reddit, fp, indent = 4)
