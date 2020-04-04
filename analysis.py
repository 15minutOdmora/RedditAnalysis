import numpy as np
import matplotlib.pyplot as plt
import os
import json


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
        Searches for the 'what' data in the 'where' data group, adds them up in lists, returs a touple(or triple) of lists
        where = 'data', 'counted_data', 'analysed_data'
        what1, what2, what3 = depends where we search.
        specs = are only used if we want a speciffic sub. """
        data1, data2, data3 = [], [], []

        if where == 'data':  # Reads from the 'data' file

            if filter == 'all':  # Ads up all the lists from every subreddit from every day
                for date in self.date_files[:2]:
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
                for subname in specs:
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
                else:
                    return sub[what1], sub[what2]

            if filter == 'specific_sub':
                sub = json.load(open(self.counted_data_dir + r'\{}.json'.format(specs)))
                if what2 is None:
                    return sub[what1]
                else:
                    return sub[what1], sub[what2]

            if filter in ['normal', 'europe', 'usa', 'nsfw']:
                for file in os.listdir(os.fsencode(self.counted_data_dir)):
                    filename = os.fsdecode(file)
                    if filename[:-5] in self.sorted_subs[filter]:
                        sub = json.load(open(self.counted_data_dir + r'\{}'.format(filename)))
                        data1.append(sub[what1])
                        if what2 is None:
                            pass
                        else:
                            data2.append(sub[what2])
                if what2 is None:
                    return data1
                else:
                    return data1, data2

        elif where == 'analysed_data':  # Reads from the analysed where we have rankings in a json file

            if filter == 'all':
                if what2 is None:
                    return self.sorted_data['all'][what1]
                elif what3 is None:
                    return self.sorted_data['all'][what1], self.sorted_data['all'][what2]
                else:
                    return self.sorted_data['all'][what1], self.sorted_data['all'][what1], self.sorted_data['all'][what1]

            if filter in ['normal', 'europe', 'usa', 'nsfw']:
                if what2 is None:
                    return self.sorted_data[filter][what1]
                elif what3 is None:
                    return self.sorted_data[filter][what1], self.sorted_data[filter][what2]
                else:
                    return self.sorted_data[filter][what1], self.sorted_data[filter][what1],\
                           self.sorted_data[filter][what1]

    def meaning(self, shortcut):
        if shortcut in ['upvotes', 'comments']:
            return shortcut
        elif shortcut == 'number_of_submissions':
            return 'Number of submissions'
        elif shortcut == 'ud_ratio':
            return 'Upvote/Downvote Ratio'
        elif shortcut == 'uc_ratio':
            return 'Upvote/Comment Ratio'
        # todo add others

    def scatter_plot_upv_com_ud(self, filter, specs=None, lin_regression=False, log_scale=False):
        """ PYPLOT:
        plots the scatter plot of all the data from the filter(normal, nsfw...) and the lin. regression function"""
        plt.style.use('seaborn')
        # Use the search function to get all the data
        points = self.search(where='data', filter=filter,
                             what1='upvotes', what2='comments', what3='ud_ratio', specs=specs)

        # Set the log scaling to the axes if true
        if log_scale:
            plt.yscale('log')
            plt.xscale('log')
        # Plot and set the settings to the scatter
        plt.scatter(points[0], points[1], c=points[2], cmap='summer', s=30, edgecolor='black', alpha=0.7)

        # Add a colorbar and set the label
        cbar = plt.colorbar()
        cbar.set_label('Upvote/Downvote Ratio')

        # Zoom out
        plt.margins(5, 5)  # Nastavljeno za log scale

        # Set labels
        plt.xlabel('Upvotes')
        plt.ylabel('Comments')

        # Calculates and plots the lin. regression function if lin_regression is set to True
        if lin_regression:
            x = np.array(points[0])
            y = np.array(points[1])
            k, n = np.polyfit(x, y, 1)
            print('Linear regression function = {} x + {}'.format(round(k, 3), round(n, 3)))
            plt.plot(x, k*x + n)
        plt.show()

    def plot_post_and_avgupv_freq(self, filter, specs=None):
        #todo finish this function start over actually
        freq, upv = self.search('counted_data', what1="time_freq_hour", what2="time_freq_hour_upv",
                                filter=filter, specs=specs)
        all_freq, all_upv = np.zeros((1, 24)), np.zeros((1, 24))
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
        x_axis = np.array([x for x in range(1, 25)])
        # avg_freq = np.array([all_freq[x]/24 for x in range(len(all_upv))])
        avg_upv = np.array([all_upv[x]/all_freq[x] for x in range(len(all_upv))])
        plt.style.use('ggplot')
        plt.subplot(211)
        plt.plot(x_axis, avg_upv[0], c='red')
        plt.ylabel('Average Upvotes / Hour')

        plt.subplot(212)
        plt.plot(x_axis, all_freq[0], c='blue')
        plt.ylabel('Posts / Hour')

        plt.show()


    def compare_plots_post_avgupv_freq(self, filter1, filter2, what1, what2, specs1=None, specs2=None):
        """ METHOD:
        Displays 4 plots for two different groups/subreddits left = group1, right = group2"""
        # Search the data:
        group1 = self.search(where='counted_data', filter=filter1, what1=what1, what2=what2, specs=specs1)
        group2 = self.search(where='counted_data', filter=filter2, what1=what1, what2=what2, specs=specs2)
        print(group1)
        print(group2)
        # Set the time period, and the data variables
        if what1 == 'time_freq_hour':
            time_period = 24
        else:
            time_period = 72
        post_freq1, post_upv1 = np.zeros((1, time_period)), np.zeros((1, time_period))
        post_freq2, post_upv2 = np.zeros((1, time_period)), np.zeros((1, time_period))
        if filter1 == "specific_sub":
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

        if filter2 == "specific_sub":
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

        # Plot everything out
        hours = [x for x in range(24)]

        # Use subplots
        fig, axs = plt.subplots(2, 2)
        axs[0, 0].plot(hours, avg_upv1[0])  # Upper left plot
        axs[0, 0].set_title('{} average upvotes per hour'.format(filter1))
        axs[0, 1].plot(hours, avg_upv2[0], 'tab:orange')  # Upper right plot
        axs[0, 1].set_title('{} average upvotes per hour'.format(filter2))
        axs[1, 0].plot(hours, post_freq1[0], 'tab:green')  # Bottom left plot
        axs[1, 0].set_title('{} posts in spec. hour'.format(filter1))
        axs[1, 1].plot(hours, post_freq2[0], 'tab:red')  # Bottom right plot
        axs[1, 1].set_title('{} posts in spec. hour'.format(filter2))

        # Set the labels
        for ax in axs.flat:
            ax.set(xlabel='x-label', ylabel='y-label')

        # Hide x labels and tick labels for top plots and y ticks for right plots.
        for ax in axs.flat:
            ax.label_outer()

        plt.show()

    def sorted_bar_chart(self, filter, what, top, specs=None):
        """ METHOD:
        Displays sorted bar-charts of subs. ranked by different categories """
        #todo uredit sirine barov, y-os, awards ...
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
                title_text = "All rewards recieved in coins worth for each {} subreddit in a 10 day period".format(filter)
                label_text = "Number of coins worth"
            else:
                title_text = "All {} awards recieved for each {} subreddit in a 10 day period".format(specs, filter)
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
            for i, v in enumerate(sub_data[::-1]):
                if specs == 'coins':
                    k = str(v / 1000) + 'k'
                else:
                    k = str(v)
                plt.text(25 + v, 2 * i + 1.3, k, color='black', fontsize=7)
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
            for i, v in enumerate(sub_data[::-1]):
                plt.text(10, 2*i +1.4, str(round(v)), color='white', fontsize=7)

            plt.show()

    def stats(self):
        """ FUNCTION: Returns different statistic data for spec.sub or group of subs """
        pass

#an = Analysis(r'C:\Users\laptop\Desktop\RedditAnalysis\RedditAnalysis')
#an.sorted_bar_chart(filter='europe', what='s_awards', top=13, specs='coins')
# an.scatter_plot_upv_com_ud(filter='specific_sub',specs=['askmen'], log_scale=True)
# an.plot_post_and_avgupv_freq()
# an.compare_plots_post_avgupv_freq(filter1='europe', filter2='usa', what1='time_freq_hour', what2='time_freq_hour_upv')
# "All rewards recieved in coins worth for each 'nsfw' subreddit in a 10 day period"
if __name__ == '__main__':
    pass