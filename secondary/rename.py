import os

# Function to rename multiple files
dates = ['08_03_2020_14', '09_03_2020_19', '10_03_2020_20', '11_03_2020_17',
                           '12_03_2020_20', '13_03_2020_20','14_03_2020_19', '15_03_2020_19',
                           '16_03_2020_23', '17_03_2020_20', '18_03_2020_18']
def main():
    """ METHOD: Renames all the files to lowercase letters."""
    for date in dates:
        for file in os.listdir(os.fsencode(r'C:\Users\laptop\Desktop\RedditAnalysis\RedditAnalysis\data\{}'.format(date))):
            filename = os.fsdecode(file)
            if filename.endswith(".json"):
                dirr = r'C:\Users\laptop\Desktop\RedditAnalysis\RedditAnalysis\data\{}'.format(date)
                print(filename)
                os.rename(dirr + r'\{}'.format(filename), dirr + r'\{}'.format(filename.lower()))

# Driver Code
if __name__ == '__main__':
    # Calling main() function
    main()