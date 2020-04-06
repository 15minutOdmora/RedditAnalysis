import json
import os
import time
from analysis import Analysis
from user_plots import histogram, all_users, top_14_plot, general_commons

"""Liams settings"""
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

"""Gaspers settings"""
# Preloads and sorts data to be used in plotting a histogram
with open('non_relational', 'r') as fp:
    data_histo = json.load(fp)

mod_plots, prem_plots, both = 0, 0, 0
for item1, item2 in zip(data_histo['is_mod'], data_histo['is_premium']):
    # checks if users have premium or are mods, or both
    if item1 and item1 == item2:
        both += 1
    elif item1:
        mod_plots += 1
    elif item2:
        prem_plots += 1
    else:
        pass

top_14_data = json.load(open('top_14', 'r'))  # preloads data for ease of access
# .json file contains data what other subreddits users post in
# looks at specific subreddits
common_connections = json.load(open('incommon_sort', 'r'))
# preloads .json containing subreddits that some other subreddits have in common
# and the number of times the connection appears between users


# Simple User Interface over the console
"""Liams functions -----------------------------------------------------------"""


def list_of_subreddits():
    """Displays the list of all the subreddits."""
    print("\n" * 30)
    print("\n\nCurrently in: Daily data / list\n")

    print("Subreddits are separated in these categories:\n" +
          "normal: List of the top " +
          "{} normal(sfw) subreddits by number of subscribers.\n".format(len(dict_of_subs["normal"])) +
          "nsfw:   List of the top {} nsfw subreddits by number of subscribers.\n".format(len(dict_of_subs['nsfw'])) +
          "europe: List of {} european subreddits.\n".format(len(dict_of_subs['europe'])) +
          "usa:    List of {} american subreddits.".format(len(dict_of_subs['usa'])) +
          "(Yes, not just from the USA as the name would imply).\n")
    while True:
        print("Type in the name of the category of the list you would like to display!\n" +
              "To exit type in 0.")
        group = input("In:")
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
    """Displays a plot(graph) of average upvotes in relation to the time posted."""
    while True:
        print("\n"*30)
        print("\n\nCurrently in: Daily data / post_upvotes\n")
        print("Displays the frequency of posts per hour and the average upvotes per hour.\n")
        print("If you would like to include all of the data from a specific group of subreddits," +
              " type in one of the following:\n- normal\n- nsfw\n- europe\n- usa")
        print("If you would like to include data from only one specific subreddit type in:\n- subreddit")
        print("If you would like to look at the data from all the subreddits type in\n- all\n")
        print("To exit type in 0.\n")
        user_input = input("In:")
        if user_input == '0':
            break
        # If its in the category just call the function
        elif user_input in ['normal', 'nsfw', 'europe', 'usa', 'all']:
            an.plot_post_and_avgupv_freq(user_input)
        # If its for a specific sub. ask for the name of the sub.
        elif user_input == 'subreddit':
            while True:
                print("Enter the name of the subreddit:")
                name = input("r/")
                if name.lower() in list_of_subs:
                    an.plot_post_and_avgupv_freq("specific_sub", specs=name.lower())
                    break
                elif name == '0':
                    break
                else:
                    print("I could not find the data for the sub {} maybe try again?".format(name))


def upv_to_comment():
    """Displays a scatter plot of upvotes in relation to comments, coloring indicates the ud_ratio"""
    while True:
        print("\n"*30)
        print("Currently in: Daily data / upv_to_comment")
        # Description and commands
        print("Displays comments in relation to upvotes in a scatter plot, goes over all of the submissions to create" +
              " the dots,\n coloring is used to show the upvote/downvote ratio" +
              "(The percentage of upvotes from all votes on the submission).\n")
        print("If you would like to include all of the data from a specific" +
              " group of subreddits, type in one of the following:\n" +
              "- normal\n- nsfw\n- europe\n- usa")
        print("If you would like to include data from only one specific subreddit type in:\n- subreddit")
        print("If you would like to look at the data from all the subreddits type in:\n- all\n")
        user_input = input("In:")
        if user_input == '0':
            break
        # Set the log scale
        print("Would you like the axes to be in a logarithmic scale?(Recommended as the data is uhh...scattered.)\n" +
              "Type in yes or no.")
        log_scale = input("In:")
        if log_scale not in ["yes", "no"]:
            log_scale = False
        else:
            if log_scale == "yes":
                log_scale = True
            else:
                log_scale = False
        # If its in the group just display it
        if user_input in ['normal', 'nsfw', 'europe', 'usa', 'all']:
            print("This might take a few seconds...")
            an.scatter_plot_upv_com_ud(user_input, log_scale=log_scale)
        # If it's a specific subreddit ask for the name
        elif user_input == 'subreddit':
            while True:
                print("Enter the name of the subreddit:")
                name = input("r/")
                if name.lower() in list_of_subs:
                    an.scatter_plot_upv_com_ud("specific_sub", specs=name.lower(), log_scale=log_scale)
                    break
                elif name == '0':
                    break
                else:
                    print("I could not find the data for the sub {} maybe try again?".format(name))


def compare_post_upvotes():
    """ Compares two groups or subreddits, by the average upvotes per certain hour and number of posts in hour"""
    while True:
        print("\n"*30)
        print("\n\nCurrently in: Daily data / compare_post_upvotes\n")
        print("Displays the post frequency per hour and the average upvotes per hour for two " +
              "different groups of subreddits.")
        print("If you would like to include all of the data from two specific" +
              " groups of subreddits, type in one of the following:\n- group")
        print("If you would like to include data from two specific subreddits type in:\n- subreddit")

        user_input = input("In")

        if user_input == '0':
            break
        # If the user wants to compare two groups
        elif user_input == "group":
            while True:
                print("Select the 1. st group by typing in the group name," +
                      " options:\n- normal\n- nsfw\n- europe\n- usa\n- all\n")
                group1 = input("In")
                if group1 not in ['normal', 'nsfw', 'europe', 'usa', 'all']:
                    print("Wrong input, try again please!")
                    continue
                print("Select the 2. st group by typing in the group name," +
                      " options:\n- normal\n- nsfw\n- europe\n- usa\n- all\n")
                group2 = input("In:")
                if group2 not in ['normal', 'nsfw', 'europe', 'usa', 'all']:
                    print("Wrong input, try again please!")
                    continue
                an.compare_plots_post_avgupv_freq(filter1=group1, filter2=group2,
                                                  what1='time_freq_hour', what2='time_freq_hour_upv')
                break
        # If the user wants to compare two subreddits
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
                    print("I could not find the data for the sub r/{} maybe try again?".format(sub2))
                    continue
                an.compare_plots_post_avgupv_freq(filter1='specific_sub', filter2='specific_sub',
                                                  what1='time_freq_hour', what2='time_freq_hour_upv',
                                                  specs1=sub1, specs2=sub2)


def sub_ranking():
    """Displays bar charts of different groups of subreddits ranked by different parameters"""
    while True:
        print("\n"*30)
        print("\n\nCurrently in: Daily data / sub_ranking\n")
        print("Displays bar charts of of subreddits ranked by different parameters")
        print("Type in one of the following groups, for the bar charts to be displayed\n" +
              "- normal\n- nsfw\n- europe\n- usa\n- all\n")
        user_input = input("In:")
        # If the user input fits a group
        if user_input in ["all", "normal", "europe", "usa", "nsfw"]:
            while True:
                print("The subrreddits in different categories are " +
                      "sorted in a few ways shown below. Thype in the command that you would like to sort by:\n")
                print("   Command                       Description")
                print("- s_avg_comments             ... Sorted by the average number of comments.")
                print("- s_avg_upvotes              ... Sorted by the average number of upvotes.")
                print("- s_avg_ud_ratio             ... Sorted by the average upvote/downvote ratio" +
                      "(The percentage of upvotes from all votes on the submission).")
                print("- s_avg_uc_ratio             ... Sorted by the average upvote/comment ratio.")
                print("- s_awards                   ... Sorted by the amount of awards or coins worth.")
                print("- s_topcomupv_to_upv         ... Sorted by the average top_comment_upvotes/post_upvotes ratio.")
                print("- s_topcomupv_to_2topcomupv  ... Sorted by the average top_comment_" +
                      "upvotes/2nd_top_comment_upvotes ratio.")
                commands = ["s_avg_comments", "s_avg_upvotes", "s_avg_ud_ratio", "s_avg_uc_ratio",
                            "s_awards", "s_topcomupv_to_upv", "s_topcomupv_to_2topcomupv"]
                user_command = input("In:")
                if user_command in commands:
                    # If user command is awards, ask for more a more specific command
                    if user_command == "s_awards":
                        while True:
                            print("Choose by what you would like to sort by:\n" +
                                  "- silver\n- gold\n- platinum\n- coins\n")
                            user_input_specs = input("In:")
                            if user_input_specs in ["silver", "gold", "platinum", "coins"]:
                                an.sorted_bar_chart(filter=user_input, what=user_command,
                                                    top=25, specs=user_input_specs)
                            elif user_input_specs == '0':
                                break
                            else:
                                print("Incorrect input, maybe try again?")
                    else:
                        an.sorted_bar_chart(filter=user_input, what=user_command, top=25, specs=None)

                elif user_command == '0':
                    break
                else:
                    print("Incorrect input, maybe try again?")

        elif user_input == '0':
            break
        else:
            print("Incorrect input, maybe try again?")


def stats_display(name, data, s_deviation):
    """ Prints the stats/data in a somewhat pretty format, gets the data from the stats function in the analysis.py"""
    # Put the data into variables
    total_submissions, total_comments, total_upvotes, total_ud = data[0], data[1], data[2], data[3]
    silver, gold, plat = data[4][0], data[4][1], data[4][2]
    coins = silver * 100 + gold * 500 + plat * 1800
    total_words = data[5]
    dev_upvotes, dev_comments, dev_ud_ratio = s_deviation[0], s_deviation[1], s_deviation[2]
    avg_upvotes = round(total_upvotes/total_submissions, 2)
    avg_comments = round(total_comments/total_submissions, 2)
    avg_ud = round(total_ud/total_submissions, 2)
    avg_words = round(total_words/total_submissions, 2)
    while True:
        print("Here are some numbers from {}, all of it was collected in a 11 day period.\n".format(name))
        print("Number of submissions:       " +
              "{} which is around {} per day.".format(total_submissions, total_submissions//11))
        print("Total number of upvotes:     {}".format(total_upvotes))
        print("Total number of comments:    {}".format(total_comments))
        print("\n")
        print("A total of " +
              "{} silver awards, {} gold awards and {} platinum awards were given.".format(silver, gold, plat))
        print("The total worth of those awards adds up to {} coins.".format(coins))
        print("\n")
        print("A submission recieves: - around {} upvotes on average,".format(avg_upvotes) +
              " with a standard deviation of {}".format(round(dev_upvotes, 2)))
        print("                       - around {} comments on average,".format(avg_comments) +
              " with a standard deviation of {}".format(round(dev_comments, 2)))
        print("                       - and has the average upvote/downvote ratio of {} ".format(avg_ud) +
              "with a standard deviation of {}".format(round(dev_ud_ratio, 2)))
        print("The average number of words in title was {}.".format(avg_words))
        print("\n Type in anything to exit back.")
        input("In")
        break


def stats():
    """ Prints out some basic stats"""
    while True:
        print("\n"*30)
        print("\n\nCurrently in: Daily data / stats\n")
        print("This will print out some basic data such as number of submissions, averages and so on...\n" +
              "Please keep in mind that some subreddits have a lot more submissions per day than we could manage " +
              "to scrape. Data might not be as representative for some 'bigger' subreddits.\n")
        print("Type in one of the following groups, for the data to be displayed:\n" +
              "- normal\n- nsfw\n- europe\n- usa\n- all\n" +
              "If you would like to look at data of one specific subreddit type in:\n" +
              "- subreddit")
        user_input = input("In:")

        # If its for a specific subreddit, ask for what subreddit
        if user_input == "subreddit":
            while True:
                print("enter the name of the subreddit you would like the data to be displayed:")
                sub_input = input("r/").lower()
                if sub_input in list_of_subs:
                    print("This might take a few seconds...")
                    numbers = an.stats(filter="specific_sub", specs=sub_input)
                    deviation = an.standard_deviation(filter="specific_sub", specs=sub_input)
                    stats_display(sub_input, numbers, deviation)
                else:
                    print("I could not find the data for the sub. r/{} maybe try again?".format(sub_input))

        # If its for a group of subreddits
        elif user_input in ["all", "normal", "europe", "usa", "nsfw"]:
            print("This might take a few seconds...")
            numbers = an.stats(filter=user_input, specs=None)
            deviation = an.standard_deviation(filter=user_input, specs=None)
            stats_display("the group " + user_input, numbers, deviation)
        elif user_input == '0':
            break
        else:
            print("Incorrect input, maybe try again?")


def daily_data():
    """Main part of the daily data, can access other display functions from here"""
    # Introduction
    print("\n" * 30)
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
          " minute.\n")
    print("Type in anything to continue.")
    input("In: ")
    # Main loop with instructions
    while True:
        print("\n"*30)
        print("\n\nCurrently in: Daily data\n")
        # Instructions
        print("Here are some commands to navigate through the analysis, type in the command:\n")
        print("Command                       Description")
        print("_" * 100)
        print("list                  ...     Displays all of the subreddits used in the analysis.\n" +
              " 0                    ...     Go back. (This can be used at any time)\n" +
              "post_upvotes          ...     Graphs out the post frequency and average upvotes of subs. " +
              "or group of subs.\n" +
              "compare_post_upvotes  ...     Similar to post_upvotes except it compares between two subs." +
              " or group of subs.\n" +
              "upv_to_comment        ...     Displays a scatter plot of comments in relation to upvotes.\n" +
              "sub_ranking           ...     Displays bar charts of subreddits ranked by different parameters.\n" +
              "stats                 ...     Prints out some basic statistics.")
        user_input = input("In:")

        if user_input == "list":
            list_of_subreddits()
        elif user_input == '0':
            break
        elif user_input == 'exit':
            return True
        elif user_input == "post_upvotes":
            post_upvotes()
        elif user_input == "upv_to_comment":
            upv_to_comment()
        elif user_input == "compare_post_upvotes":
            compare_post_upvotes()
        elif user_input == "sub_ranking":
            sub_ranking()
        elif user_input == "stats":
            stats()
        else:
            print('Invalid command, try again!')
            time.sleep(2)


def user_data():
    """ Interface for user data"""
    print("\n"*20)
    print("Daily data: \n" +
          "The data that is represented in the following histograms, was extracted from Reddit API Praws\n" +
          "queries from Reddit user object instances. Through a sorting program called DailyUserdata, which\n" +
          "received .json files of collected DailyData dumps, and then iterated through its 'usernames' list,\n" +
          "the program created its own dictionary of data, which contained: user comment karma, user post karma,\n" +
          "booleans of if user is a moderator or has premium, month and hour of posting last 100 comments, \n" +
          "and all the subreddits the user submitted posts in, to which a frequency counter was appended. \n" +
          "Other extracted data includes number of comments and post submission of the last 100 instances, \n" +
          "number of submissions with over 1000 karma.\n" +
          "The only data used in the end was frequency of posting, if the user is a moderator or has premium\n" +
          "and names of subreddits most visited, where the frequency of posting tells us which" +
          " ones are most visited.\n" +
          "Description of histograms:\n" +
          "1. Shows ratio of users who are moderators, have premium, are moderators with premium, and normal users.\n" +
          "2. Shows what users of a specific subreddit visit besides the subreddit looked at," +
          " with a number that suggests\n" +
          "popularity or frequency of posting/commenting in those subreddits.\n" +
          "3. Shows what users of 2 different subreddits have most in common." +
          " Which other subreddits the users of seemingly" +
          "opposing interests, both visit. Y-axis is the ocurrence of visits among them." +
          " X-axis are the subreddits the users\n" +
          "looked at both visit or post/submit in.\n" +
          "The second and third histogram are limited to so few subreddits," +
          " due to the time complexity of data extraction.\n")

    while True:
        print("\n\nCurrently in: User data\n")
        # Instructions
        print("Here are some commands to navigate through the analysis:\n")
        print("Command         Description")
        print("_" * 80)
        print(" 0                    ...     Go back.\n" +
              "mod_premium           ...     Graphs a percent histogram of number of mods and users with premium\n" +
              "all_mp                ...     Number of users used in histogram mod_premium\n" +
              "top_14                ...     Bar chart of top 14 other visited subreddits from select subreddits\n" +
              "common                ...     Bar chart of top 10 in common subreddits of select subreddits \n")

        user_input = input()

        if user_input == "list":
            list_of_subreddits()
        elif user_input == '0':
            break
        elif user_input == "mod_premium":
            histogram(mod_plots, prem_plots, both)
        elif user_input == 'all_mp':
            all_users(data_histo)
        elif user_input == 'common':
            print('Enter a number corresponding to what histogram you would like to see:', '\n')
            print('0: AdviceAnimals vs AnimalsBeingBros', '\n',
                  '1: cats vs dankmemes', '\n',
                  '2: gonewild vs atheism', '\n',
                  '3: StarWars vs Art', '\n',
                  '4: Sydney vs Germany', '\n',
                  '5: TittyDrop vs iphone')
            user_input = input()
            general_commons(common_connections[int(user_input)])
        elif user_input == 'top_14':
            print('Enter the name of the subreddit you wish to see:', '\n', list(top_14_data.keys()))
            user_input = input()
            if user_input not in list(top_14_data.keys()):
                print('This is not an option.')
            else:
                top_14_plot(user_input)
        else:
            print('Invalid command, try again!')


def main():
    """ Main function with the main loop,
    we use functions from the class Analysis to display daily_data graphs."""
    # Main loop
    while True:
        # Welcoming words
        print("Hello and welcome to the Reddit Analysis.\n" +
              "This user interface was made to simplify the navigation through data and data display. \n\n" +
              "We sort the data into two parts:\n\n" +
              "1. Daily data, where the data was collected from 238 different subreddits in 11 consecutive days\n" +
              "2. User data, where the data was collected from user profiles.")
        # Using the input to navigate to different functions
        leave = False
        while True:
            print("\n\nCurrently in: main()\n")
            print("To access Daily data type in '1', to access user data type '2'.\n")
            anws = input("In:")
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
