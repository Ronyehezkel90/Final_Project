import datetime
import tweepy

base_address = 'https://twitter.com/{}/status/{}'


class BasicMeasures:
    def __init__(self, connector):
        self.api = connector.api

    def get_all_followers(self):
        # NOT WORKING
        followers = []
        for followers_page in tweepy.Cursor(self.api.followers, screen_name='zehavagalon').pages():
            followers.extend(followers_page)
        return followers

    def get_tweets(self, name):
        tweets = []
        for tweet in tweepy.Cursor(self.api.user_timeline, screen_name=name, exclude_replies=False,
                                   include_rts=True).items():
            if self.one_year_ago_tweet(tweet):
                tweets.append(tweet)
            else:
                break
        return tweets

    def one_year_ago_tweet(self, tweet):
        one_year_ago = datetime.datetime.today() - datetime.timedelta(days=365)
        if tweet.created_at >= one_year_ago:
            return True
        return False

    def count_by_measure(self, measure, tweets):
        response = []
        retweets = False
        replies = False
        original_tweets = False
        favourites_count = False

        if measure == 'original_tweets':
            original_tweets = True
        elif measure == 'TweetCountScore':
            retweets = True
            original_tweets = True
        elif measure == 'replies':
            replies = True
        elif measure == 'retweets':
            retweets = True

        count = 0

        if measure == 'Likes':
            tweet = tweets[0]
            count = tweet.user.favourites_count

        else:
            for tweet in tweets:

                if hasattr(tweet, 'retweeted_status'):
                    if retweets:
                        count += 1
                        response.append(tweet)
                        continue

                elif tweet.in_reply_to_screen_name:
                    if replies:
                        count += 1
                        continue

                elif original_tweets:
                    count += 1
                    response.append(tweet)

        return response

    def get_original_tweets(self, tweets):
        return self.count_by_measure('original_tweets', tweets)

    def get_ot1(self, list_of_original_tweets):
        # OT1 = Original Tweets
        return list_of_original_tweets.__len__()

    def get_ot2(self, list_of_original_tweets):
        # OT2 = Number of URL links shared by their OTs.
        count = 0
        for tweet in list_of_original_tweets:
            count += tweet.entities['urls'].__len__()
        return count

    def get_ot3(self, list_of_original_tweets):
        # OT3 = Number of hashtags included in their OTs.
        count = 0
        for tweet in list_of_original_tweets:
            count += tweet.entities['hashtags'].__len__()
        return count

    def get_replies_tweets(self, tweets):
        return self.count_by_measure('replies', tweets)

    def get_rp1(self, list_of_replies_tweets):
        # RP1 = Number of replies posted by the author
        return list_of_replies_tweets.__len__()

    def get_retweets(self, tweets):
        return self.count_by_measure('retweets', tweets)

    def get_rt1(self, tweets):
        # RT1 = Number of retweets accomplished by the author
        return self.count_by_measure('retweets', tweets).__len__()

    def get_rt2(self, list_of_original_tweets):
        # RT2 = Number of original tweets posted by the author and retweeted by other users
        count = 0
        for tweet in list_of_original_tweets:
            count += tweet.retweet_count
        return count

    def get_rt3(self, list_of_original_tweets):
        # RT3 = Number of users who have retweeted author's tweets
        retweeters = {}
        for tweet in list_of_original_tweets:
            for retweet in self.api.retweets(tweet.id, 100):
                retweeters[retweet.author.name] = 1
        return retweeters.__len__()

    def get_ft1(self, screen_name):
        # FT1 = Number of tweets of other users marked as favourites (liked) by the author
        page_number = 1
        first_pagination = True
        result = None
        while True:
            tweets_liked_by_user = self.api.favorites(screen_name, page=page_number)
            if tweets_liked_by_user.__len__() != 0:
                if first_pagination:
                    result = tweets_liked_by_user
                    first_pagination = False
                else:
                    result += tweets_liked_by_user
            else:
                break
            page_number += 1
        count = 0
        if result:
            for tweet in result:
                if str(tweet.author.screen_name) != screen_name[1:]:
                    count += 1
                else:
                    ron = 2
        return count

    def get_ft2(self, list_of_original_tweets):
        # Number of author's tweets marked as favorite (liked) by other users
        count = 0
        for tweet in list_of_original_tweets:
            # I did it to avoid tweets that liked only by the user itself
            if tweet.favorite_count > 1:
                count += 1
        return count

    def get_m1(self, list_of_original_tweets):
        """
        This measure checks Number of mentions to other users by the author
        just from original tweets
        """
        count = 0
        for tweet in list_of_original_tweets:
            count += tweet.entities[u'user_mentions'].__len__()
        return count

    def get_m2(self, list_of_original_tweets):
        """
        This measure checks Number of users mentioned by the author.
        just from original tweets
        """
        count = 0
        mentiond_users_dict = {}
        for tweet in list_of_original_tweets:
            if tweet.entities[u'user_mentions'].__len__() > 0:
                for mentioned in tweet.entities[u'user_mentions']:
                    if mentioned[u'id'] in mentiond_users_dict:
                        mentiond_users_dict[mentioned[u'id']] += 1
                    else:
                        mentiond_users_dict[mentioned[u'id']] = 1
        return mentiond_users_dict.values().__len__()

    def get_f1(self, user):
        """
        This measure checks Number of followers of the user.
        """
        return user.followers_count

    def get_f3(self, user):
        """
        This measure checks Number of followees of the user.
        """
        return user.friends_count

    def get_all_basic_measures(self, user):
        basic_measures_dict = {}
        name = user.name
        tweets = self.get_tweets(name)
        original_tweets = self.get_original_tweets(tweets)
        basic_measures_dict['original_tweets'] = original_tweets.__len__()
        basic_measures_dict['ot1'] = self.get_ot1(original_tweets)
        basic_measures_dict['ot2'] = self.get_ot2(original_tweets)
        basic_measures_dict['ot3'] = self.get_ot3(original_tweets)
        replies_tweets = self.get_replies_tweets(tweets)
        basic_measures_dict['replies_tweets'] = replies_tweets.__len__()
        basic_measures_dict['retweets'] = self.get_retweets(tweets).__len__()
        basic_measures_dict['rp1'] = self.get_rp1(replies_tweets)
        basic_measures_dict['rt1'] = self.get_rt1(tweets)
        basic_measures_dict['rt2'] = self.get_rt2(original_tweets)
        basic_measures_dict['rt3'] = self.get_rt3(original_tweets)
        # Need to fix ft1
        # basic_measures_dict['ft1'] = self.get_ft1(user.screen_name)
        basic_measures_dict['ft2'] = self.get_ft2(original_tweets)
        basic_measures_dict['m1'] = self.get_m1(original_tweets)
        basic_measures_dict['m2'] = self.get_m2(original_tweets)
        # Very big in compare to others
        # basic_measures_dict['f1'] = self.get_f1(user)
        basic_measures_dict['f3'] = self.get_f3(user)
        return basic_measures_dict
