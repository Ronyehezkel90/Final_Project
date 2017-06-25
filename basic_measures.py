import datetime

import math
import pandas as pd
import requests
import tweepy

from conf import RT3_THRESHOLD

base_address = 'https://twitter.com/{}/status/{}'


class BasicMeasures:
    def __init__(self, connector):
        self.api = connector.api
        self.auth = connector.auth
        self.mentions = {'total_mentions': {}, 'user_mentions': {}}

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
                        response.append(tweet)
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

    def get_rp2(self, original_tweets):
        # RP2 = Number of OTs posted by the author and replied by other users.
        #todo implementation
        for tweet in original_tweets:
            tweet = 2

    def get_retweets(self, tweets):
        return self.count_by_measure('retweets', tweets)

    def get_rt1(self, retweets):
        # RT1 = Number of retweets accomplished by the author
        return retweets.__len__()

    def get_rt2(self, list_of_original_tweets):
        # RT2 = Number of original tweets posted by the author and retweeted by other users
        count = 0
        for tweet in list_of_original_tweets:
            count += tweet.retweet_count
        return count

    def check_rt3_threshold(self, list_of_original_tweets):
        # RT3 = Number of users who have retweeted author's tweets
        retweeters = {}
        counter = 1
        for tweet in list_of_original_tweets:
            if counter < 70:
                if tweet.retweet_count > 0 and tweet.retweet_count < 100:
                    retweets = self.api.retweets(tweet.id, 100)
                    print counter
                    counter += 1
                    for retweet in retweets:
                        retweeters[retweet.author.name] = 1
        return retweeters.__len__()

    def get_rt3(self, list_of_original_tweets):
        # RT3 = Number of users who have retweeted author's tweets
        count_users = 0
        retweeted_tweets = 0
        for tweet in list_of_original_tweets:
            if tweet.retweet_count > 0:
                count_users += tweet.retweet_count
                retweeted_tweets += 1
        return (count_users / float(retweeted_tweets)) * RT3_THRESHOLD if retweeted_tweets> 0 else 0

    def get_ft1(self, user):
        return user[0]['favourites_count']

    def get_ft1_without_own_likes(self, screen_name):
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
        return user[0]['followers_count']

    def get_f3(self, user):
        """
        This measure checks Number of followees of the user.
        """
        return user[0]['friends_count']

    def get_topical_signal(self, all_tweets, discuss_rank):
        return discuss_rank / float(len(all_tweets)) if len(all_tweets)>0 else 0

    def get_discuss_rank(self, all_tweets, topical_hashtags):
        counter = 0
        for tweet in all_tweets:
            for tweet_hashtag in tweet.entities[u'hashtags']:
                if tweet_hashtag['text'].lower() in topical_hashtags:
                    counter += 1
                    break
        return counter

    def get_h_index(self, original_tweets):
        h_counter = 0
        url_tweets = []
        for tweet in original_tweets:
            if tweet.entities[u'urls']:
                url_tweets.append(tweet)
        for url_tweet in url_tweets:
            if url_tweet.retweet_count > len(url_tweets):
                h_counter += 1
        return h_counter

    def get_mention_impact(self, user_dict):
        """
        This measure checks influence level based on tweets mentions and user mentions
        """
        base = 10
        subtracter = user_dict['m3'] * math.log(user_dict['m4'], base) if user_dict['m4'] != 0 else 0
        subtracted = user_dict['m1'] * math.log(user_dict['m2'], base) if user_dict['m2'] != 0 else 0
        return subtracter - subtracted

    def get_spread_rank(self, retweets, tweets):
        time_passed = 0.1
        # proportion by_day
        proportion = 60 * 60 * 24
        for retweet in retweets:
            time_passed += (retweet.created_at - retweet.retweeted_status.created_at).seconds
        return (len(retweets) / (time_passed / proportion)) / len(tweets) if len(tweets)>0 else 0

    def set_user_mentions(self, tweets):
        mentiond_by_user = []
        for tweet in tweets:
            if tweet.entities['user_mentions']:
                for user in tweet.entities['user_mentions']:
                    if user['screen_name'] in self.mentions['total_mentions'].keys():
                        self.mentions['total_mentions'][user['screen_name']] += 1
                        if user['screen_name'] not in mentiond_by_user:
                            mentiond_by_user.append(user['screen_name'])
        for mentiond in mentiond_by_user:
            self.mentions['user_mentions'][mentiond] += 1

    def calculate_user_based_measures(self, all_users_measures_dict):
        for user in all_users_measures_dict:
            all_users_measures_dict[user]['m3'] = self.mentions['total_mentions'][user]
            all_users_measures_dict[user]['m4'] = self.mentions['user_mentions'][user]
            all_users_measures_dict[user]['mention_impact'] = self.get_mention_impact(all_users_measures_dict[user])

    def get_all_basic_measures(self, user, hashtags):
        basic_measures_dict = {}
        screen_name = user[0]['screen_name']
        tweets = self.get_tweets(screen_name)
        self.set_user_mentions(tweets)
        original_tweets = self.get_original_tweets(tweets)
        retweets = self.get_retweets(tweets)
        replies_tweets = self.get_replies_tweets(tweets)
        basic_measures_dict['original_tweets'] = original_tweets.__len__()
        basic_measures_dict['ot1'] = self.get_ot1(original_tweets)
        basic_measures_dict['ot2'] = self.get_ot2(original_tweets)
        basic_measures_dict['ot3'] = self.get_ot3(original_tweets)
        basic_measures_dict['rp1'] = self.get_rp1(replies_tweets)
        basic_measures_dict['rp2'] = self.get_rp2(original_tweets)
        basic_measures_dict['rt1'] = self.get_rt1(retweets)
        basic_measures_dict['rt2'] = self.get_rt2(original_tweets)
        basic_measures_dict['rt3'] = self.get_rt3(original_tweets)
        basic_measures_dict['ft1'] = self.get_ft1(user)
        basic_measures_dict['ft2'] = self.get_ft2(original_tweets)
        basic_measures_dict['m1'] = self.get_m1(original_tweets)
        basic_measures_dict['m2'] = self.get_m2(original_tweets)
        # Very big in compare to others
        basic_measures_dict['f1'] = self.get_f1(user)
        basic_measures_dict['f3'] = self.get_f3(user)
        basic_measures_dict['discuss_rank'] = self.get_discuss_rank(tweets, hashtags)
        basic_measures_dict['topical_signal'] = self.get_topical_signal(tweets, basic_measures_dict['discuss_rank'])
        basic_measures_dict['h_index'] = self.get_h_index(original_tweets)
        basic_measures_dict['spread_rank'] = self.get_spread_rank(retweets, tweets)

        return basic_measures_dict

    def check_all_users(self, users):
        authrized_users = []
        i = 0
        while i <= len(users) / 90:
            users_as_string = ",".join(users[i * 90:(i + 1) * 90])
            response = requests.get(url="https://api.twitter.com/1.1/users/lookup.json?screen_name=" + users_as_string,
                                    auth=self.auth.apply_auth())
            authrized_users += response.json()
            i += 1
        df = pd.DataFrame(authrized_users)
        for user in authrized_users:
            self.mentions['user_mentions'][user['screen_name']] = 0
            self.mentions['total_mentions'][user['screen_name']] = 0
        return df
