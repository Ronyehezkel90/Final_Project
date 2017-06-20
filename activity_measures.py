import math

from basic_measures import BasicMeasures
import tweepy


class ActivityMeasures:
    def __init__(self):
        self.basic_measures_dict = None

    def tweet_count_score(self):
        """
        counts the number of original tweets plus the number of retweets
        :return:
        """
        return self.basic_measures_dict['original_tweets'] + self.basic_measures_dict['retweets']

    def general_activity(self):
        """
        General Activity = OT1+RP1+RT1+FT1
        :return:
        """
        # OT1 = Original Tweets
        # RP1 = Number of replies posted by user
        # RT1 = Number of retweets accomplished by the user
        # FT1 = Number of tweets of other users marked as favorite (liked) by the user
        general_activity = 0
        measures_to_sum = ['ot1', 'rp1', 'rt1', 'ft1']
        for measure in measures_to_sum:
            general_activity += self.basic_measures_dict[measure]
        return general_activity

    def signal_strength(self):
        """
        Signal Strength = OT1/(OT1+RT1)
        :return:
        """
        if self.basic_measures_dict['ot1'] == 0:
            return 0
        return self.basic_measures_dict['ot1'] / (self.basic_measures_dict['ot1'] + self.basic_measures_dict['rt1'])

    def activity_score(self):
        """
        Activity Score = f1 + f3 + tweets
        :return:
        """
        activity_score = 0
        measures_to_sum = ['f1', 'f3', 'original_tweets', 'replies_tweets', 'retweets']
        for measure in measures_to_sum:
            activity_score += self.basic_measures_dict[measure]
        return activity_score

    def follower_rank(self):
        """
        Follower Rank = F1/(F1+F3)
        :return:
        """
        if self.basic_measures_dict['f1'] == 0:
            return 0
        return self.basic_measures_dict['f1'] / (self.basic_measures_dict['f1'] + self.basic_measures_dict['f3'])

    def popularity(self):
        """
        popularity = 1-(e^(-lamda*f1))
        lamda = 1
        :return:
        """
        return 1 - (math.exp(-1 * self.basic_measures_dict['f1']))

    def get_all_activity_measures(self, basic_measures_dict):
        self.basic_measures_dict = basic_measures_dict
        activity_measures_dict = {}
        activity_measures_dict['tweet_count_score'] = self.tweet_count_score()
        activity_measures_dict['general_activity'] = self.general_activity()
        # activity_measures_dict['topical_signal'] = self.topical_signal()
        activity_measures_dict['signal_strength'] = self.signal_strength()
        activity_measures_dict['activity_score'] = self.activity_score()
        activity_measures_dict['follower_rank'] = self.follower_rank()
        activity_measures_dict['popularity'] = self.popularity()
        return activity_measures_dict
