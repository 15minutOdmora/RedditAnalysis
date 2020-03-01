import json

list = []
num = 1
for line in open('subredditi.txt', 'r'):
    line = line.split()
    if num == 1:
        num = 0
    else:
        list.append([line[1].strip('/r/'), line[0], line[2]])

list_reddit = {'nsfw': [], 'normal': [], 'usa': [], 'europe': []}

nsfw = []
for line in open('nsfw.txt', 'r'):
    line = line.split()
    line = [x.strip('r/') for x in line]
    nsfw += line

for ena in list:
    for dva in nsfw:
        if ena[0] == dva:
            list_reddit['nsfw'] += [ena]

for stvar in list_reddit['nsfw']:
    if stvar in list:
        list.remove(stvar)

for nekaj in list:
    list_reddit['normal'] += [nekaj]

with open('reddit_dict.json', 'w') as fp:
    json.dump(list_reddit, fp)
