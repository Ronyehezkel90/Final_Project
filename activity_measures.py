from basic_measures import BasicMeasures
import tweepy


class ActivityMeasures:
    def __init__(self):
        self.basic_measures = BasicMeasures()
        self.tweets = self.basic_measures.get_tweets('@JohnAlexanderMP')

    def tweet_count_score(self):
        """
        counts the number of original tweets plus the number of retweets
        :return:
        """
        original_tweets = self.basic_measures.get_original_tweets(self.tweets)
        return self.basic_measures.get_ot1(original_tweets) + self.basic_measures.get_rt1(self.tweets)

    def general_activity(self):
        """
        General Activity = OT1+RP1+RT1+FT1
        :return:
        """
        # OT1 = Original Tweets
        OT1 = self.basic_measures.count_by_measure('original_tweets', self.tweets)
        # RP1 = Number of replies posted by user
        RP1 = self.basic_measures.count_by_measure('replies', self.tweets)
        # RT1 = Number of retweets accomplished by the user
        RT1 = self.basic_measures.count_by_measure('retweets', self.tweets)
        # FT1 = Number of tweets of other users marked as favorite (liked) by the user
        FT1 = self.basic_measures.count_by_measure('Likes', self.tweets)
        return OT1 + RP1 + RT1 + FT1
