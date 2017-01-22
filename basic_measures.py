import datetime
import urllib2
import tweepy
from BeautifulSoup import BeautifulSoup
from connector import Connector
from lxml.html import parse
import requests

tweets = []
base_address = 'https://twitter.com/{}/status/{}'


class BasicMeasures:
    def __init__(self):
        my_connector = Connector()
        self.api = my_connector.api

    def get_tweets(self, name):
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

    def count_by_measure(self, measure):
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

    def general_activity(self):
        # General Activity = OT1+RP1+RT1+FT1
        # OT1 = Original Tweets
        OT1 = self.count_by_measure('original_tweets')
        # RP1 = Number of replies posted by user
        RP1 = self.count_by_measure('replies')
        # RT1 = Number of retweets accomplished by the user
        RT1 = self.count_by_measure('retweets')
        # FT1 = Number of tweets of other users marked as favorite (liked) by the user
        FT1 = self.count_by_measure('Likes')

        return OT1 + RP1 + RT1 + FT1

    def get_original_tweets(self):
        return self.count_by_measure('original_tweets')

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

    def get_replies_tweets(self):
        return self.count_by_measure('replies')

    def get_rp1(self, list_of_replies_tweets):
        # RP1 = Number of replies posted by the author
        return list_of_replies_tweets.__len__()

    def get_retweets(self):
        return self.count_by_measure('retweets')

    def get_rt1(self):
        # RT1 = Number of retweets accomplished by the author
        return self.count_by_measure('retweets').__len__()

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
        user = self.api.get_user(screen_name)
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

    ####################Both methods are not completed
    # returns list(retweet users),list(favorite users) for a given screen_name and status_id
    def get_ft31(self):
        # url ='https://twitter.com/JohnAlexanderMP/status/776252037566652416'
        # r = requests.get(url)
        # soup = BeautifulSoup(r.text)
        # Find the nunber of replies
        # str(soup.find("span", {"class": "ProfileTweet-actionCountForPresentation"}).text)
        # ul = soup.find("ul", {"class": "stats"})
        screen_name = 'JohnAlexanderMP'
        status_id = '776252037566652416'
        url = urllib2.urlopen('https://twitter.com/' + screen_name + '/status/' + status_id)
        root = parse(url).getroot()

        num_rts = 0
        num_favs = 0
        rt_users = []
        fav_users = []
        mashu = root.find_class('activity-popup-dialog-users clearfix')[0]
        for ul in root.find_class('activity-popup-dialog-users clearfix'):
            for li in ul.cssselect('li'):
                cls_name = li.attrib['class']
                if cls_name.find('retweet') >= 0:
                    num_rts = int(li.cssselect('a')[0].attrib['data-tweet-stat-count'])
                elif cls_name.find('favorit') >= 0:
                    num_favs = int(li.cssselect('a')[0].attrib['data-tweet-stat-count'])
                elif cls_name.find('avatar') >= 0 or cls_name.find('face-pile') >= 0:  # else face-plant
                    for users in li.cssselect('a'):
                        # apparently, favs are listed before retweets, but the retweet summary's listed before the fav summary
                        # if in doubt you can take the difference of returned uids here with retweet uids from the official api
                        if num_favs > 0:  # num_rt > 0:
                            # num_rts -= 1
                            num_favs -= 1
                            # rt_users.append(users.attrib['data-user-id'])
                            fav_users.append(users.attrib['data-user-id'])
                        else:
                            # fav_users.append(users.attrib['data-user-id'])
                            rt_users.append(users.attrib['data-user-id'])
            return rt_users, fav_users

    def get_ft32(self):
        url = 'https://twitter.com/i/activity/favorited_popup?id=776252037566652416'
        r = requests.get(url)
        ron = 2

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

    def get_f1(self, screen_name):
        """
        This measure checks Number of followers of the user.
        """
        user = self.api.get_user(screen_name)
        return user.followers_count

    def get_f3(self, screen_name):
        """
        This measure checks Number of followees of the user.
        """
        user = self.api.get_user(screen_name)
        return user.friends_count
