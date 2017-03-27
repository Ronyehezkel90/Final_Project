from basic_measures import BasicMeasures
import unittest
from activity_measures import ActivityMeasures
import numpy as np
import matplotlib.pyplot as plt


class MyTestCase(unittest.TestCase):
    # def setUp(self):
    # self.basic_measures = BasicMeasures()
    # self.screen_name = '@JohnAlexanderMP'
    # self.tweets = self.basic_measures.get_tweets(self.screen_name)
    #
    # def test_something(self):
    #     for tweet in self.tweets:
    #         print(tweet.text + '\n')
    #
    # def test_ot(self):
    #     original_tweets = self.basic_measures.get_original_tweets()
    #     ot1 = self.basic_measures.get_ot1(original_tweets)
    #     self.assertIsNotNone(ot1)
    #     ot2 = self.basic_measures.get_ot2(original_tweets)
    #     self.assertIsNotNone(ot2)
    #     ot3 = self.basic_measures.get_ot3(original_tweets)
    #     self.assertIsNotNone(ot3)
    #
    # def test_rp(self):
    #     original_tweets = self.basic_measures.get_original_tweets()
    #     replies_tweets = self.basic_measures.get_replies_tweets()
    #     rp1 = self.basic_measures.get_rp1(replies_tweets)
    #     self.assertIsNotNone(rp1)
    #
    # def test_rt1(self):
    #     rt1 = self.basic_measures.get_rt1()
    #     self.assertIsNotNone(rt1)
    #
    # def test_rt(self):
    #     original_tweets = self.basic_measures.get_original_tweets()
    #     retweets = self.basic_measures.get_retweets()
    #     rt1 = self.basic_measures.get_rt1(retweets)
    #     self.assertIsNotNone(rt1)
    #     rt2 = self.basic_measures.get_rt2(original_tweets)
    #     self.assertIsNotNone(rt2)
    #     rt3 = self.basic_measures.get_rt3(original_tweets)
    #     self.assertIsNotNone(rt3)
    #
    # def test_ft(self):
    #     original_tweets = self.basic_measures.get_original_tweets()
    #     # ft1 = self.basic_measures.get_ft1(self.screen_name)
    #     # ft2 = self.basic_measures.get_ft2(original_tweets)
    #     ft3 = self.basic_measures.get_ft3()
    #
    # def test_m(self):
    #     original_tweets = self.basic_measures.get_original_tweets()
    #     m1 = self.basic_measures.get_m1(original_tweets)
    #     m2 = self.basic_measures.get_m2(original_tweets)
    #     ron = 2
    #
    # def test_f(self):
    #     f1 = self.basic_measures.get_f1(self.screen_name)
    #     f3 = self.basic_measures.get_f3(self.screen_name)
    #     ron = 2

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
