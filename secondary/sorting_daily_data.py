import json

class Sorting:
    """ The class reads all of the data, and sorts the subreddits in different orders
        each function sorts differently """
    def __init__(self, file_path):
        self.file_path = file_path
        self.sorted_data = dict()
        self.sorted_data['europe'] = dict()
        self.sorted_data['usa'] = dict()
        self.sorted_data['nsfw'] = dict()
        self.sorted_data['normal'] = dict()
        self.sorted_data['all'] = dict()

    def s_avg_comments(self, list_of_subs):
        """FUNCTION:
        Returns a sorted(by comments) list(descending order) of tuples = (sub.name, sub.avg_comments)"""
        data = []
        for sub_name in list_of_subs:
            sub_name = sub_name.lower() + '.json'
            sub = json.load(open(self.file_path + '/' + sub_name))
            data.append((sub_name[:-5], round(sub['comments'] / sub['number_of_submissions'], 5)))
        sorted_data = sorted(data, key=lambda x: x[1], reverse=True)
        return sorted_data

    def s_avg_upvotes(self, list_of_subs):
        """FUNCTION:
        Returns a sorted(by upvotes) list(descending order) of tuples = (sub.name, sub.avg_comments)"""
        data = []
        for sub_name in list_of_subs:
            sub_name = sub_name.lower() + '.json'
            sub = json.load(open(self.file_path + '/' + sub_name))
            data.append((sub_name[:-5], round(sub['upvotes'] / sub['number_of_submissions'], 5)))
        sorted_data = sorted(data, key=lambda x: x[1], reverse=True)
        return sorted_data

    def s_avg_ud_ratio(self, list_of_subs):
        """FUNCTION:
        Returns a sorted(by ud_ratio) list(descending order) of tuples = (sub.name, sub.avg_comments)"""
        data = []
        for sub_name in list_of_subs:
            sub_name = sub_name.lower() + '.json'
            sub = json.load(open(self.file_path + '/' + sub_name))
            data.append((sub_name[:-5], round(sub['ud_ratio'] / sub['number_of_submissions'], 5)))
        sorted_data = sorted(data, key=lambda x: x[1], reverse=True)
        return sorted_data

    def s_avg_uc_ratio(self, list_of_subs):
        """FUNCTION:
        Returns a sorted(by uc_ratio) list(descending order) of tuples = (sub.name, sub.avg_comments)"""
        data = []
        for sub_name in list_of_subs:
            sub_name = sub_name.lower() + '.json'
            sub = json.load(open(self.file_path + '/' + sub_name))
            data.append((sub_name[:-5], round(sub['upvotes'] / sub['comments'], 5)))
        sorted_data = sorted(data, key=lambda x: x[1])
        return sorted_data

    def s_awards(self, list_of_subs):
        """FUNCTION:
        Returns a sorted(by amount of awards) list of lists(descending order) of touples =
            = [[silver], [gold], [plat], [coints worth of awards]] tuples = (sub.name, sorting unit)"""
        silver, gold, plat, coins = [], [], [], []
        for sub_name in list_of_subs:
            sub_name = sub_name.lower() + '.json'
            sub = json.load(open(self.file_path + '/' + sub_name))
            silver.append((sub_name[:-5], sub['awards'][0]))
            gold.append((sub_name[:-5], sub['awards'][1]))
            plat.append((sub_name[:-5], sub['awards'][2]))
            coin_worth = sub['awards'][0] * 100 + sub['awards'][1] * 500 + sub['awards'][2] * 1800
            coins.append((sub_name[:-5], coin_worth))
        sorted_silver =  sorted(silver, key=lambda x: x[1], reverse=True)
        sorted_gold = sorted(gold, key=lambda x: x[1], reverse=True)
        sorted_plat = sorted(plat, key=lambda x: x[1], reverse=True)
        sorted_coins = sorted(coins, key=lambda x: x[1], reverse=True)
        return [sorted_silver, sorted_gold, sorted_plat, sorted_coins]

    def s_topcomupv_to_upv(self, list_of_subs):
        """FUNCTION:
        Returns a sorted(by upvotes) list(descending order) of tuples = (sub.name, sub.avg_comments)"""
        data = []
        for sub_name in list_of_subs:
            sub_name = sub_name.lower() + '.json'
            sub = json.load(open(self.file_path + '/' + sub_name))
            if sub['topcom_counter'] <= 0:
                continue
            data.append((sub_name[:-5], round(sub['topcomupv_to_upv'] / sub['topcom_counter'], 5)))
        sorted_data = sorted(data, key=lambda x: x[1], reverse=True)
        return sorted_data

    def s_topcomupv_to_2topcomupv(self, list_of_subs):
        """FUNCTION:
        Returns a sorted(by upvotes) list(descending order) of tuples = (sub.name, sub.avg_comments)"""
        data = []
        for sub_name in list_of_subs:
            sub_name = sub_name.lower() + '.json'
            sub = json.load(open(self.file_path + '/' + sub_name))
            if sub['topcom_counter'] <= 0:
                continue
            data.append((sub_name[:-5], round(sub['topcomupv_to_2topcomupv'] / sub['topcom_counter'], 5)))
        sorted_data = sorted(data, key=lambda x: x[1], reverse=True)
        return sorted_data

    def call_functions(self, dict_of_subs):
        """METHOD:
        Calls all the sorting functions and saves the data to the self.sorted_data dict"""
        list_of_all_subs = []
        for key, value in dict_of_subs.items(): # Iterates over the subreddit_dict_fin dictionary
            list_of_subs = []
            for subreddit in value:
                list_of_subs.append(subreddit[0])
                list_of_all_subs.append(subreddit[0])
            # Call each function and save the sorted data in the category in the dict.
            self.sorted_data[key]['s_avg_comments'] = self.s_avg_comments(list_of_subs)
            self.sorted_data[key]['s_avg_upvotes'] = self.s_avg_upvotes(list_of_subs)
            self.sorted_data[key]['s_avg_ud_ratio'] = self.s_avg_ud_ratio(list_of_subs)
            self.sorted_data[key]['s_avg_uc_ratio'] = self.s_avg_uc_ratio(list_of_subs)
            self.sorted_data[key]['s_awards'] = self.s_awards(list_of_subs)
            self.sorted_data[key]['s_topcomupv_to_upv'] = self.s_topcomupv_to_upv(list_of_subs)
            self.sorted_data[key]['s_topcomupv_to_2topcomupv'] = self.s_topcomupv_to_2topcomupv(list_of_subs)
        # Sort the data of all subreddits
        self.sorted_data['all']['s_avg_comments'] = self.s_avg_comments(list_of_all_subs)
        self.sorted_data['all']['s_avg_upvotes'] = self.s_avg_upvotes(list_of_all_subs)
        self.sorted_data['all']['s_avg_ud_ratio'] = self.s_avg_ud_ratio(list_of_all_subs)
        self.sorted_data['all']['s_avg_uc_ratio'] = self.s_avg_uc_ratio(list_of_all_subs)
        self.sorted_data['all']['s_awards'] = self.s_awards(list_of_all_subs)
        self.sorted_data['all']['s_topcomupv_to_upv'] = self.s_topcomupv_to_upv(list_of_all_subs)
        self.sorted_data['all']['s_topcomupv_to_2topcomupv'] = self.s_topcomupv_to_2topcomupv(list_of_all_subs)

    def save_to_json(self):
        """METHOD:
            Saves the dict as a json file """
        with open(r'C:\Users\laptop\Desktop\RedditAnalysis\RedditAnalysis\analysed_data\sorted_data.json', 'w') as file:
            json.dump(self.sorted_data, file)

counted_data = r'C:\Users\laptop\Desktop\RedditAnalysis\RedditAnalysis\counted_data'
subs_dict = json.load(open(r'C:\Users\laptop\Desktop\RedditAnalysis\RedditAnalysis\subreddit_dict_fin.json'))

def main():
    data = Sorting(file_path=counted_data)
    data.call_functions(subs_dict)
    data.save_to_json()

if __name__ == '__main__':
    main()

