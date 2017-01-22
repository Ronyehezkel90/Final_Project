from basic_measures import BasicMeasures
import unittest
import requests
from BeautifulSoup import BeautifulSoup

class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.basic_measures = BasicMeasures()
        self.screen_name = '@JohnAlexanderMP'
        self.tweets = self.basic_measures.get_tweets(self.screen_name)

    def test_something(self):
        for tweet in self.tweets:
            print(tweet.text + '\n')

    def test_ot(self):
        original_tweets = self.basic_measures.get_original_tweets()
        ot1 = self.basic_measures.get_ot1(original_tweets)
        self.assertIsNotNone(ot1)
        ot2 = self.basic_measures.get_ot2(original_tweets)
        self.assertIsNotNone(ot2)
        ot3 = self.basic_measures.get_ot3(original_tweets)
        self.assertIsNotNone(ot3)

    def test_rp(self):
        original_tweets = self.basic_measures.get_original_tweets()
        replies_tweets = self.basic_measures.get_replies_tweets()
        rp1 = self.basic_measures.get_rp1(replies_tweets)
        self.assertIsNotNone(rp1)

    def test_rt1(self):
        rt1 = self.basic_measures.get_rt1()
        self.assertIsNotNone(rt1)
    def test_rt(self):
        original_tweets = self.basic_measures.get_original_tweets()
        retweets = self.basic_measures.get_retweets()
        rt1 = self.basic_measures.get_rt1(retweets)
        self.assertIsNotNone(rt1)
        rt2 = self.basic_measures.get_rt2(original_tweets)
        self.assertIsNotNone(rt2)
        rt3 = self.basic_measures.get_rt3(original_tweets)
        self.assertIsNotNone(rt3)

    def test_ft(self):
        original_tweets = self.basic_measures.get_original_tweets()
        #ft1 = self.basic_measures.get_ft1(self.screen_name)
        #ft2 = self.basic_measures.get_ft2(original_tweets)
        ft3 = self.basic_measures.get_ft3()

    def test_m(self):
        original_tweets = self.basic_measures.get_original_tweets()
        m1 = self.basic_measures.get_m1(original_tweets)
        m2 = self.basic_measures.get_m2(original_tweets)
        ron =2

    def test_f(self):
        f1 = self.basic_measures.get_f1(self.screen_name)
        f3 = self.basic_measures.get_f3(self.screen_name)
        ron =2
