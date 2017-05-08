from basic_measures import BasicMeasures
import unittest
from activity_measures import ActivityMeasures
import numpy as np
import matplotlib.pyplot as plt


class MyTestCase(unittest.TestCase):


    def test_activity_measures(self):
        activity_measures = ActivityMeasures()
        print activity_measures.tweet_count_score()
        ron = 2

    def test_all_basics(self):
        basic_measures = BasicMeasures()
        user = basic_measures.api.get_user('@' + 'djalbo')
        basics = basic_measures.get_all_basic_measures(user)
        ron=2

    def test_plots(self):
        # a = [1, 5, 54]
        # b = [99,12,2]
        # plt.plot(a)
        # plt.plot(b)
        # plt.axis([0, 3, 0, 100])
        # plt.show()


        # x = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
        # y = np.array([20, 21, 22, 23])
        # my_xticks = ['John', 'Arnold', 'Mavis', 'Matt']
        # plt.xticks(x, my_xticks)
        # plt.plot(x, y)
        # plt.show()
        a = {'m1': 2, 'm2': 5, 'm3': 4}
        b = {'m1': 3, 'm2': 7, 'm3': 5}
        dict_of_users_dicts = {
            'a': a,
            'b': b
        }
        x = np.arange(3)
        my_xticks =''
        max_value=0
        for user_dict in dict_of_users_dicts.values():
            plt.plot(x, user_dict.values())
            my_xticks=user_dict.keys()
            if max(user_dict.values())>max_value:
                max_value = max(user_dict.values())
        plt.xticks(x, my_xticks)
        y= np.arange(max_value+1)
        plt.yticks(y)
        plt.show()

    def test_get_followers(self):
        basic_measures = BasicMeasures()
        followers = basic_measures.get_all_followers()
        ron=2

