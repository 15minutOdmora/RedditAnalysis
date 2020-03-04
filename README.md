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

## HDF5
The big dictionaries of data will be saved in a HDF5 format.



## Praw: the python reddit API 
### Initializing the API
[Getting started](https://praw.readthedocs.io/en/latest/getting_started/quick_start.html)
To use praw with your program you have to: 
Go to [Reddit preferences/apps](https://www.reddit.com/prefs/apps) while logged in with a reddit account.
Click on the create app and fill out the form:
- name: RedditAnalysis
- App type: Choose the script option
- description: You can leave this blank
- about url: You can leave this blank
- redirect url: http://localhost:8080 

That gives you your app's client ID and apps client secret number which are used when you create a reddit instance, as shown in the example below:

```
import praw

reddit = praw.Reddit(client_id='my client id',
                     client_secret='my client secret',
                     user_agent='my user agent')

```

Or if you want to do whatever your Reddit account is authorized to do:

```
import praw

reddit = praw.Reddit(client_id='my client id',
                     client_secret='my client secret',
                     user_agent='my user agent',
                     username='my username',
                     password='my password')
```

### Reading data 
#### Obtaining a subreddit instance [Subreddit instances](https://praw.readthedocs.io/en/latest/code_overview/models/subreddit.html#praw.models.Subreddit):
```
subreddit = reddit.subreddit('learnpython')      
```

#### Obtain submission instances from a created submission instance [Submission instances](https://praw.readthedocs.io/en/latest/code_overview/models/submission.html#praw.models.Submission):

Example:
```
# assume you have a Subreddit instance bound to variable `subreddit`
for submission in subreddit.hot(limit=10):
    print(submission.title)  # Output: the submission's title
    print(submission.score)  # Output: the submission's score
    print(submission.id)     # Output: the submission's ID
    print(submission.url)    # Output: the URL the submission points to
                             # or the submission's URL if it's a self post
```
Sorts you can iterate through:
- controversial
- gilded
- hot
- new
- rising
- top

#### Obtain redditor instances [Redditor Attributes](https://praw.readthedocs.io/en/latest/code_overview/models/redditor.html#praw.models.Redditor):

Two most common ones are:
- via the author attribute of a Submission or Comment instance
- via the redditor() method of Reddit

Example:
```
 # assume you have a Submission instance bound to variable `submission`
 redditor1 = submission.author
 print(redditor1.name)  # Output: name of the redditor

# assume you have a Reddit instance bound to variable `reddit`
 redditor2 = reddit.redditor('bboe')
 print(redditor2.link_karma)  # Output: u/bboe's karma
```

#### Obtain comment instances [Comment Attributes](https://praw.readthedocs.io/en/latest/code_overview/models/comment.html#praw.models.Comment):
Submissions have a comments attribute that is a CommentForest instance. That instance is iterable and represents the top-level comments of the submission by the default comment sort (best). If you instead want to iterate over all comments as a flattened list you can call the list() method on a CommentForest instance.

Example:
```
# assume you have a Reddit instance bound to variable `reddit`
top_level_comments = list(submission.comments)
all_comments = submission.comments.list()
```
