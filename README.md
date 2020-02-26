# RedditAnalysis
## Description of project: Analyzing different data from reddit
to do

## Git hub commands
[Basic writing and formatting in Github](https://help.github.com/en/github/writing-on-github/basic-writing-and-formatting-syntax)

In cmd: set the current directory(cd) to the working file connected to this repo.
```
git status                             # tells the status of the folder in the repo.
git add 'filename'                     # adds the file 'filename' to the repo
git commit -m 'change description'     # locks the changes of the file 'filename' 
git push                               # pushes the changes to the github repo.
git pull                               # pulls the changes from github into the cd
```

## Json format 101
On this project most data will be saved using dictionaries and lists saved as a .json file.
```
import json                            # comes with the python package

data = {'sub_name' : [1, 1, 1, 0]}     # dict(), list() are allowed

with open('mydata.json', 'w') as f:    # Saving data
    json.dump(data, f)
    
f = open('mydata.json')                # Reading data
team = json.load(f)
```

## Praw: the python reddit API 
To use praw with your program you have to: 
Go to [Reddit preferences/apps](https://www.reddit.com/prefs/apps) while logged in with a reddit account.
Click on the create app and fill out the form:
- name: RedditAnalysis
- App type: Choose the script option
- description: You can leave this blank
- about url: You can leave this blank
- redirect url: http://localhost:8080 

That gives you your app's client ID and apps client secret number which are used when you create a reddit instance, as showed in the below example:

```
import praw

reddit = praw.Reddit(client_id='my client id',
                     client_secret='my client secret',
                     user_agent='my user agent')

```


