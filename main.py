import json
import os

from analysis import Analysis

# Get the current directory and initialize the analysis class as an.
dir_path = os.path.dirname(os.path.realpath(__file__))
an = Analysis(dir_path)
fil = open("subreddit_dict_fin.json")
dict_of_subs = json.load(fil)
# crate the list of subs, lowercase letters
list_of_subs = []
for key, value in dict_of_subs.items():
    for sub in value:
        list_of_subs.append(sub[0].lower())

# Simple User Interface over the console
"""Liams functions -----------------------------------------------------------"""

def list_of_subreddits():
    """Displays the list of all the subreddits."""
    print(".\n" * 20)
    print("\n\nCurrently in: Daily data / list\n")
    print("Subreddits are separated in different categories:\n" +
          "normal: List of the top {} normal(sfw) subreddits.\n".format(len(dict_of_subs["normal"])) +
          "nsfw:   List of the top {} nsfw subreddits.\n".format(len(dict_of_subs['nsfw'])) +
          "europe: List of {} european subreddits.\n".format(len(dict_of_subs['europe'])) +
          "usa:    List of {} american subreddits.(Yes, not just from the USA as the name would imply).\n".format(len(dict_of_subs['usa'])))
    while True:
        print("Type in the name of the category of which lists you would like to display!\n" +
              "To exit type in 0.")
        group = input()
        if group in dict_of_subs:
            counter = 1
            for subreddit in dict_of_subs[group]:
                print(str(counter) + ') ' + subreddit[0])
                counter += 1
        elif group == '0':
            break
        elif group == 'exit':
            break
        else:
            print("Invalid category, check the spelling!")


def post_upvotes():
    """Nedela za dolocene subreddite"""
    print(".\n" * 20)
    while True:
        print(".\n"*20)
        print("Displays the post frequency per hour and the average upvotes per hour\n")
        print("If you would like to include all of the data from a specific group of subreddits, type in one of the following:\n" +
              "- normal\n- nsfw\n- europe\n- usa")
        print("If you would like to include data from only one specific subreddit type in:\n- subreddit")
        print("If you would like to look at the data from all the subreddits type in\n- all\n")

        user_input = input()
        if user_input == '0':
            break
        elif user_input in ['normal', 'nsfw', 'europe', 'usa', 'all']:
            an.plot_post_and_avgupv_freq(user_input)
        elif user_input == 'subreddit':
            #todo Ker nedela niti all nedela
            while True:
                print("Enter the name of the subreddit:")
                name = input()
                if name.lower() in list_of_subs:
                    an.plot_post_and_avgupv_freq("specific_sub", specs=name.lower())
                    break
                elif name == '0':
                    break
                else:
                    print("I could not find the data for the sub {} maybe try again?".format(name))

def upv_to_cooment():
    """Dela """
    print(".\n" * 20)
    while True:
        print("Displays comments in relation to upvotes in a scatter plot, goes over all of the submissions to create" +
              " the dots, coloring is used to show the upvote percentage.\n")
        print("If you would like to include all of the data from a specific" +
              " group of subreddits, type in one of the following:\n" +
              "- normal\n- nsfw\n- europe\n- usa")
        print("If you would like to include data from only one specific subreddit type in:\n- subreddit")
        print("If you would like to look at the data from all the subreddits type in\n- all\n")
        user_input = input()
        if user_input == '0':
            break

        # Set the log scale
        print("Would you like the axes to be in a logarithmic scale?(Recommended as the data is uhh...scattered.)\n" +
              "Type in yes or no.")
        log_scale = input()
        if log_scale not in ["yes", "no"]:
            log_scale = False
        else:
            if log_scale == "yes":
                log_scale = True
            else:
                log_scale = False

        if user_input in ['normal', 'nsfw', 'europe', 'usa', 'all']:
            an.scatter_plot_upv_com_ud(user_input, log_scale=log_scale)
        elif user_input == 'subreddit':
            while True:
                print("Enter the name of the subreddit:")
                name = input()
                if name.lower() in list_of_subs:
                    an.scatter_plot_upv_com_ud("specific_sub", specs=name.lower(), log_scale=log_scale)
                    break
                elif name == '0':
                    break
                else:
                    print("I could not find the data for the sub {} maybe try again?".format(name))

def compare_post_upvotes():
    """ Dela, treba še izris grafa popravit"""
    while True:
        print(".\n"*20)
        print("Displays the post frequency per hour and the average upvotes per hour for two " +
              "different groups of subreddits.")
        print("If you would like to include all of the data from two specific groups of subreddits, type in one of the following:\n" +
              "- group")
        print("If you would like to include data from two specific subreddits type in:\n- subreddit")

        user_input = input()

        if user_input == '0':
            break

        elif user_input == "group":
            while True:
                print("Select the 1. st group by typing in the froup name, options:\n- normal\n- nsfw\n- europe\n- usa\n- all\n")
                group1 = input()
                if group1 not in ['normal', 'nsfw', 'europe', 'usa', 'all']:
                    print("Wrong input, try again please!")
                    continue
                print("Select the 2. st group by typing in the froup name, options:\n- normal\n- nsfw\n- europe\n- usa\n- all\n")
                group2 = input()
                if group2 not in ['normal', 'nsfw', 'europe', 'usa', 'all']:
                    print("Wrong input, try again please!")
                    continue
                an.compare_plots_post_avgupv_freq(filter1=group1, filter2=group2,
                                                  what1='time_freq_hour', what2='time_freq_hour_upv')
                break

        elif user_input == 'subreddit':
            while True:
                print("Select the 1. subreddit by typing in the name of the subreddit")
                sub1 = input("r/")
                if sub1 == '0':
                    break
                if sub1 not in list_of_subs:
                    print("I could not find the data for the sub {} maybe try again?".format(sub1))
                    continue
                print("Select the 2. subreddit by typing in the name of the subreddit")
                sub2 = input("r/")
                if sub2 == '0':
                    break
                if sub2 not in list_of_subs:
                    print("I could not find the data for the sub {} maybe try again?".format(sub2))
                    continue
                an.compare_plots_post_avgupv_freq(filter1='specific_sub', filter2='specific_sub',
                                                  what1='time_freq_hour', what2='time_freq_hour_upv',
                                                  specs1=sub1, specs2=sub2)

"""-----------------------------------------------------------------------------"""



"""Bureks functions-------------------------------------------------------------"""



"""-----------------------------------------------------------------------------"""




def daily_data():
    # Introduction
    print(".\n" * 20)
    print("Daily data: \n" +
          "Here's a quick description of how the data was collected, using the python Reddit API Praw.\n" +
          "We've created a program that would go through a pre made list of different subreddits, and would\n" +
          "read the top 100 submissions of that day, extract different data and save it to .json files which\n" +
          "are stored in the directory 'data'. The program was then run on 11 consecutive days, " +
          "from 8.3.2020 to 18.3.2020. \n" +
          "Warning!\n" +
          "We've only read the top 100 submissions for each sub. in a day, so the data may not be as representative\n" +
          "for every subreddit. Ex. subreddits such as memes or dankmemes get over 1000 submissions per day, \n" +
          "reading all of that would be time consuming as we can only get a certain amount of server requests per" +
          "minute.")
    # Main loop with instructions
    while True:
        print("\n\nCurrently in: Daily data\n")
        # Instructions
        print("Here are some commands to navigate through the analysis:\n")
        print("Command         Description")
        print("_" * 80)
        print("list                  ...     To display all of the subreddits used in the analysis.\n" +
              " 0                    ...     Go back.\n" +
              "exit                  ...     Exit to the first page.\n" +
              "post_upvotes          ...     Graphs out the post frequency and average upvotes of subs. or group of subs.\n" +
              "compare_post_upvotes  ...     Similar to post_upvotes except it compares two different ones.\n" +
              "upv_to_comment        ...     Displays a scatter plot of comments in relation to upvotes\n")
        user_input = input()

        if user_input == "list":
            list_of_subreddits()
        elif user_input == '0':
            break
        elif user_input == 'exit':
            return True
        elif user_input == "post_upvotes":
            post_upvotes()
        elif user_input == "upv_to_comment":
            upv_to_cooment()
        elif user_input == "compare_post_upvotes":
            compare_post_upvotes()
        else:
            print('Invalid command, try again!')


def user_data():
    """ To je tvoje burek, ..."""
    print("User data ...... to do ")
    pass


def main():
    """ Main function with the main loop,
    we use functions from the class Analysis to display daily_data graphs."""
    # Main loop
    while True:
        # Welcoming words
        print("Hello and welcome to the Reddit Analysis.\n" +
              "This user interface was made to simplify the navigation through data and data display. \n\n" +
              "We sort the data into two parts:\n\n" +
              "1. Daily data, were the data was collected from 238 different subreddits in 11 consecutive days\n" +
              "2. User data, where ...")
        # Using the input to navigate to different functions
        leave = False
        while True:
            print("\n\nCurrently in: main()\n")
            print("To access Daily data type in '1', to access user data type '2'.\n")
            anws = input()
            if anws == '1':
                leave = daily_data()
            elif anws == '2':
                user_data()
                # leave = user_data()
            else:
                print("Input incorrect, try again!")
            if leave:
                break


if __name__ == '__main__':
    main()
