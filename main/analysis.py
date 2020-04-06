import numpy as np
import matplotlib.pyplot as plt
import os
import json
import math


class Analysis:
    def __init__(self, dir):
        self.dir = dir
        self.counted_data_dir = self.dir + r'\counted_data'
        self.data_files = self.dir + r'\data'
        self.sorted_data = json.load(open(self.dir + r'\analysed_data\sorted_data.json'))
        self.subs = json.load(open(self.dir + r'\subreddit_dict_fin.json'))
        self.date_files = ['08_03_2020_14', '09_03_2020_19', '10_03_2020_20', '11_03_2020_17',
                           '12_03_2020_20', '13_03_2020_20', '14_03_2020_19', '15_03_2020_19',
                           '16_03_2020_23', '17_03_2020_20', '18_03_2020_18']
        # Create a dict with only the lower names of subs, keys = normal, nsfw ...
        self.sorted_subs = dict()
        for key, value in self.subs.items():
            self.sorted_subs[key] = [dat[0].lower() for dat in value]

    def search(self, where, filter, what1, what2=None, what3=None, specs=None):
        """FUNCTION:
        Searches for the 'what' data in the 'where' data group, adds them up in lists, returs a touple(or triple) of
        lists where = 'data', 'counted_data', 'analysed_data'
        what1, what2, what3 = depends where we search.
        specs = are only used if we want a speciffic sub. """
        data1, data2, data3 = [], [], []

        if where == 'data':  # Reads from the 'data' file

            if filter == 'all':  # Ads up all the lists from every subreddit from every day
                for date in self.date_files:
                    for file in os.listdir(os.fsencode(self.data_files + r'\{}'.format(date))):
                        filename = os.fsdecode(file)
                        if filename.endswith(".json"):
                            sub = json.load(open(self.data_files + r'\{}\{}'.format(date, filename)))
                            data1 += sub[what1]
                            if data2 is not None:
                                data2 += sub[what2]
                            if what3 is not None:
                                data3 += sub[what3]
                return data1, data2, data3

            elif filter == 'specific_sub':  # Only adds up from the specific sub specs
                for _ in specs:
                    for date in self.date_files:
                        for file in os.listdir(os.fsencode(self.data_files + r'\{}'.format(date))):
                            filename = os.fsdecode(file)
                            if filename[:-5] in specs:
                                if filename.endswith(".json"):
                                    sub = json.load(open(self.data_files + r'\{}\{}'.format(date, filename)))
                                    data1 += sub[what1]
                                    if data2 is not None:
                                        data2 += sub[what2]
                                    if what3 is not None:
                                        data3 += sub[what3]
                return data1, data2, data3

            elif filter in ['normal', 'europe', 'usa', 'nsfw']:  # Only adds up from the subs in the category filter
                for date in self.date_files:
                    for file in os.listdir(os.fsencode(self.data_files + r'\{}'.format(date))):
                        filename = os.fsdecode(file)
                        if filename[:-5] in self.sorted_subs[filter]:
                            if filename.endswith(".json"):
                                sub = json.load(open(self.data_files + r'\{}\{}'.format(date, filename)))
                                data1 += sub[what1]
                                if data2 is not None:
                                    data2 += sub[what2]
                                if what3 is not None:
                                    data3 += sub[what3]
                return data1, data2, data3

        elif where == 'counted_data':  # Reads from the 'counted_data' file

            if filter == 'all':  # Appends all the lists
                sub = json.load(open(self.counted_data_dir + r'\all_sub_data.json'))
                if what2 is None:
                    return sub[what1]
                elif what3 is None and what2 is not None:
                    return sub[what1], sub[what2]
                else:
                    return sub[what1], sub[what2], sub[what3]

            if filter == 'specific_sub':
                sub = json.load(open(self.counted_data_dir + r'\{}.json'.format(specs)))
                if what2 is None:
                    return sub[what1]
                elif what3 is None and what2 is not None:
                    return sub[what1], sub[what2]
                else:
                    return sub[what1], sub[what2], sub[what3]
            if filter in ['normal', 'europe', 'usa', 'nsfw']:
                for file in os.listdir(os.fsencode(self.counted_data_dir)):
                    filename = os.fsdecode(file)
                    if filename[:-5] in self.sorted_subs[filter]:
                        sub = json.load(open(self.counted_data_dir + r'\{}'.format(filename)))
                        data1.append(sub[what1])
                        if what2 is None:
                            pass
                        elif what3 is None and what2 is not None:
                            data2.append(sub[what2])
                        elif what3 is not None:
                            data2.append(sub[what2])
                            data3.append(sub[what3])

                if what2 is None:
                    return data1
                elif what3 is None and what2 is not None:
                    return data1, data2
                else:
                    return data1, data2, data3
        elif where == 'analysed_data':  # Reads from the analysed where we have rankings in a json file

            if filter == 'all':
                if what2 is None:
                    return self.sorted_data['all'][what1]
                elif what3 is None:
                    return self.sorted_data['all'][what1], self.sorted_data['all'][what2]
                else:
                    return self.sorted_data['all'][what1], self.sorted_data['all'][what2], self.sorted_data['all'][what3]

            if filter in ['normal', 'europe', 'usa', 'nsfw']:
                if what2 is None:
                    return self.sorted_data[filter][what1]
                elif what3 is None:
                    return self.sorted_data[filter][what1], self.sorted_data[filter][what2]
                else:
                    return self.sorted_data[filter][what1], self.sorted_data[filter][what1],\
                           self.sorted_data[filter][what1]

    def meaning(self, sho):
        """Returns the meaning of shortcuts(sho) used in bar charts"""
        if sho == "s_avg_comments":
            return "average number of comments"
        elif sho == "s_avg_upvotes":
            return "average number of upvotes"
        elif sho == "s_avg_ud_ratio":
            return "average upvote/downvote ratio"
        elif sho == "s_avg_uc_ratio":
            return "upvote/comment ratio"
        elif sho == "s_topcomupv_to_upv":
            return "number of upvotes of the top comment / number of upvotes on post"
        elif sho == "s_topcomupv_to_2topcomupv":
            return "number of upvotes of the top comment / number of upvotes on the 2nd top comment"
        else:
            return "error: No title"

    def scatter_plot_upv_com_ud(self, filter, specs=None, lin_regression=False, log_scale=False):
        """ PYPLOT:
        plots the scatter plot of all the data from the filter(normal, nsfw...) and the lin. regression function"""
        plt.style.use('seaborn')
        # Use the search function to get all the data
        points = self.search(where='data', filter=filter,
                             what1='upvotes', what2='comments', what3='ud_ratio', specs=specs)
        num_of_posts = len(points[0])

        # Set the log scaling to the axes if true
        if log_scale:
            plt.yscale('log')
            plt.xscale('log')
        # Plot and set the settings to the scatter
        plt.scatter(points[0], points[1], c=points[2], cmap='summer', s=30, edgecolor='black', alpha=0.7)

        # Add a colorbar and set the label
        cbar = plt.colorbar()
        cbar.set_label('Upvote/Downvote ratio')

        # Zoom out
        plt.margins(5, 5)  # Nastavljeno za log scale

        # Set labels
        plt.xlabel('Upvotes')
        plt.ylabel('Comments')
        if filter == "specific_sub":
            tit = "r/" + specs[0].upper() + specs[1:]
        else:
            tit = "the group " + filter[0].upper() + filter[1:]
        plt.title("The relation of upvotes to comments in {}.\n Number of posts: {}".format(tit, num_of_posts))

        # Calculates and plots the lin. regression function if lin_regression is set to True
        if lin_regression:
            x = np.array(points[0])
            y = np.array(points[1])
            k, n = np.polyfit(x, y, 1)
            print('Linear regression function = {} x + {}'.format(round(k, 3), round(n, 3)))
        plt.show()

    def plot_post_and_avgupv_freq(self, filter, specs=None):
        """Plots the average upvotes per hour and post freq."""
        freq, upv = self.search('counted_data', what1="time_freq_hour", what2="time_freq_hour_upv",
                                filter=filter, specs=specs)
        all_freq, all_upv = np.zeros((1, 25)), np.zeros((1, 25))
        if filter in ["specific_sub", "all"]:
            index = 0
            for number in freq[0]:
                all_freq[0, index] += number
                index += 1
            index = 0
            for number in upv[0]:
                all_upv[0, index] += number
                index += 1
        else:
            for sub in freq:
                index = 0
                for post in sub[0]:
                    all_freq[0, index] += post
                    index += 1
            for sub in upv:
                index = 0
                for post in sub[0]:
                    all_upv[0, index] += post
                    index += 1

        x_axis = np.array([x for x in range(0, 25)])
        # connect the last number with the first one as they should be the same
        ar = []
        for x in range(25):
            if x < 24:
                ar.append(all_upv[0, x]/all_freq[0, x])
            else:
                ar.append(all_upv[0, 0]/all_freq[0, 0])
        avg_upv = np.array(ar)
        plt.style.use('ggplot')
        plt.subplot(211)
        plt.xlim(0, 24)
        plt.plot(x_axis, avg_upv, c='red')
        plt.title("Average post upvotes per hour and number of posts per hour\n(UTC)")
        plt.ylabel('Average number of upvotes')

        plt.subplot(212)
        plt.xlim(0, 24)
        all_freq[0, 24] = all_freq[0, 0]
        plt.plot(x_axis, all_freq[0], c='blue')
        plt.ylabel("Number of posts")
        plt.xlabel("Hour")
        plt.show()

    def compare_plots_post_avgupv_freq(self, filter1, filter2, what1, what2, specs1=None, specs2=None):
        """ METHOD:
        Displays 4 plots for two different groups/subreddits left = group1, right = group2"""
        # Search the data:
        group1 = self.search(where='counted_data', filter=filter1, what1=what1, what2=what2, specs=specs1)
        group2 = self.search(where='counted_data', filter=filter2, what1=what1, what2=what2, specs=specs2)
        # Set the time period, and the data variables
        if what1 == 'time_freq_hour':
            time_period = 24
        else:
            time_period = 72
        post_freq1, post_upv1 = np.zeros((1, time_period)), np.zeros((1, time_period))
        post_freq2, post_upv2 = np.zeros((1, time_period)), np.zeros((1, time_period))
        if filter1 in ["specific_sub", "all"]:
            for i in range(len(group1[0][0])):
                post_freq1[0, i] += group1[0][0][i]
            for i in range(len(group2[0][0])):
                post_freq2[0, i] += group2[0][0][i]
        else:
            # Add up the lists for the two groups
            for sub in range(len(group1[0])):  # Post freq. p. time period group1
                for i in range(len(group1[0][sub][0])):
                    post_freq1[0, i] += group1[0][sub][0][i]
            for sub in range(len(group2[0])):  # Post freq. p. time period group2
                for i in range(len(group2[0][sub][0])):
                    post_freq2[0, i] += group2[0][sub][0][i]

        if filter2 in ["specific_sub", "all"]:
            for i in range(len(group1[1][0])):
                post_upv1[0, i] += group1[1][0][i]
            for i in range(len(group2[1][0])):
                post_upv2[0, i] += group2[1][0][i]
        else:
            for sub in range(len(group1[1])):  # Sum of upvotes p. h. group1
                for i in range(len(group1[1][sub][0])):
                    post_upv1[0, i] += group1[1][sub][0][i]
            for sub in range(len(group2[1])):  # Sum of upvotes p. h. group2
                for i in range(len(group2[1][sub][0])):
                    post_upv2[0, i] += group2[1][sub][0][i]

        # Create the average upv. p. h. for the two groups
        avg_upv1, avg_upv2 = np.zeros((1, 24)), np.zeros((1, 24))
        for i in range(len(post_upv1[0])):
            avg_upv1[0, i] = post_upv1[0, i] / post_freq1[0, i]
        for i in range(len(post_upv2[0])):
            avg_upv2[0, i] = post_upv2[0, i] / post_freq2[0, i]

        # Label names
        hours = [x for x in range(24)]
        if filter1 == "specific_sub":
            name1 = specs1
            name2 = specs2
        else:
            name1 = filter1
            name2 = filter2
        # Use subplots
        fig, axs = plt.subplots(2, 2)
        axs[0, 0].plot(hours, avg_upv1[0])  # Upper left plot
        axs[0, 0].set_title('{}'.format(name1))
        axs[0, 1].plot(hours, avg_upv2[0], 'tab:orange')  # Upper right plot
        axs[0, 1].set_title('{}'.format(name2))
        axs[1, 0].plot(hours, post_freq1[0], 'tab:green')  # Bottom left plot
        axs[1, 1].plot(hours, post_freq2[0], 'tab:red')  # Bottom right plot

        # Set the labels
        counter = 0
        for ax in axs.flat:
            if counter == 0:
                ax.set(xlabel='0', ylabel='Average upvotes per hour')
            elif counter == 2:
                ax.set(xlabel='Hour', ylabel='Number of posts per hour')
            elif counter == 3:
                ax.set(xlabel='Hour', ylabel='3')

            counter += 1
        # Hide x labels and tick labels for top plots and y ticks for right plots.
        for ax in axs.flat:
            ax.label_outer()

        plt.show()

    def sorted_bar_chart(self, filter, what, top, specs=None):
        """ METHOD:
        Displays sorted bar-charts of subs. ranked by different categories """
        data = self.search(where='analysed_data', filter=filter, what1=what)
        if what == 's_awards':
            if specs == 'platinum':
                color = 'aquamarine'
            elif specs == 'coins':
                color = 'yellow'
            else:
                color = specs

            # title text and label text
            if specs == 'coins':
                title_text = "All rewards recieved in coins worth for each" + \
                             " {} subreddit in a 11 day period".format(filter)
                label_text = "Number of coins worth"
            else:
                title_text = "All {} awards recieved for each {} subreddit in a 11 day period".format(specs, filter)
                label_text = "Number of {} awards".format(specs)

            specs_dict = {'silver': 0, 'gold': 1, 'platinum': 2, 'coins': 3}
            if len(data[specs_dict[specs]]) < top:
                top = len(data[specs_dict[specs]])
            sub_names, sub_data = list(), list()
            for index in range(top):
                num = data[specs_dict[specs]][index][1]
                sub_names.append(data[specs_dict[specs]][index][0])
                sub_data.append(num)
            plt.barh(y=[2 * x for x in range(top, 0, -1)], width=sub_data, tick_label=sub_names, height=1.6,
                     color=color, edgecolor='black', linewidth=0.5)

            # Setting the numbers on bars
            """for i,+ v in enumerate(sub_data[::-1]):
                if specs == 'coins':
                    k = str(v / 1000) + 'k'
                else:
                    k = str(v)
                plt.text(25 + v, 2 * i + 1.3, k, color='black', fontsize=7)"""
            plt.title(title_text)
            plt.xlabel(label_text)
            plt.show()

        else:
            if len(data) < top:
                top = len(data)

            sub_names, sub_data = list(), list()
            for index in range(top):
                sub_names.append(data[index][0])
                sub_data.append(data[index][1])
            plt.barh(y=[2*x for x in range(top, 0, -1)], width=sub_data, tick_label=sub_names, height=1.6)
            # Setting the numbers on bars
            """for i, v in enumerate(sub_data[::-1]):
                plt.text(10, 2*i +1.4, str(round(v)), color='white', fontsize=7)"""
            plt.title("Top {} subreddits from the category {}\n ranked by {}".format(top, filter, self.meaning(what)))
            plt.show()

    def number_of_submissions_prediction(self):
        """Coming soon"""
        pass

    def standard_deviation(self, filter, specs=None):
        """Returns the standard deviation for upvotes, comments, and us_ratio"""
        upv, com, ud = self.search(where="data", filter=filter,
                                   what1="upvotes", what2="comments", what3="ud_ratio", specs=specs)
        # Calc. the averages, lengths of the lists should in theory be the same
        length = len(upv)
        avg_upv = sum(upv) / length
        avg_com = sum(com) / length
        avg_ud = sum(ud) / length
        # Calculate the s. deviation
        d_upv, d_com, d_ud = 0, 0, 0
        for i in range(length):
            d_upv += (upv[i] - avg_upv)**2
            d_com += (com[i] - avg_com)**2
            d_ud += (ud[i] - avg_ud)**2
        return math.sqrt(d_upv/(length-1)), math.sqrt(d_com/(length-1)), math.sqrt(d_ud/(length-1))

    def stats(self, filter, specs=None):
        """ FUNCTION: returns a list of different stats from group/subreddit
        touple of averages: (sum_num_of_submissions, sum_number_comments,
                                sum_num_upvotes, sum_ud ,[sum_of_awards_list_of3lists],
                                sum_title_length_words)"""
        # Fetch the data, for the groups
        if filter in ["europe", "nsfw", "normal", "usa"]:
            num_sub, com, upv = self.search('counted_data', filter=filter,
                              what1="number_of_submissions", what2="comments", what3="upvotes")
            ud, awards, title_len = self.search('counted_data', filter=filter,
                              what1="ud_ratio", what2="awards", what3="title_length")
            # calculate the averages
            sum_num_sub = sum(num_sub)
            sum_com = round(sum(com), 2)
            sum_upv = round(sum(upv), 2)
            sum_ud = round(sum(ud), 2)
            # do the averages for the awards and title lengths
            silver, gold, plat, words = 0, 0, 0, 0
            for i in range(len(awards)):
                silver += awards[i][0]
                gold += awards[i][1]
                plat += awards[i][2]
                words += title_len[i][0]

            return sum_num_sub, sum_com, sum_upv, sum_ud, [silver, gold, plat], words
        else:
            num_sub, com, upv = self.search('counted_data', filter=filter,
                                            what1="number_of_submissions", what2="comments", what3="upvotes",
                                            specs=specs)
            ud, awards, title_len = self.search('counted_data', filter=filter,
                                                what1="ud_ratio", what2="awards", what3="title_length",
                                                specs=specs)
            return num_sub, com, upv, ud, awards, title_len[0]


#if __name__ == '__main__':