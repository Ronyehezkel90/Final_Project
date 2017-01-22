import tweepy
from tweepy import OAuthHandler
import datetime

consumer_key = 'P819tguRDdVJf8nXP36CquWMm'
consumer_secret = 'sdgPVTpaOUtnTbe019Mx641rc7qGDN89nEVBKG7H5OoCWkew3D'
access_token = '773769927333408768-qTYJOrWCAzRMx5juSpEhkkzu454vyrO'
access_secret = 'oyBxEVjOYgqpbvU5rwC7QYmz46NDc4OpNGPxRfbmBQEee'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

tweets = []


def get_ten_statuses():
    for tweet in tweepy.Cursor(api.home_timeline).items(10):
        # Process a single status
        print(tweet.user.name)
        print(tweet.text)


def get_tweets(name):
    for tweet in tweepy.Cursor(api.user_timeline, screen_name=name, exclude_replies=False, include_rts=True).items():
        if one_year_ago_tweet(tweet):
            tweets.append(tweet)
        else:
            return


def count_by_measure(measure):
    retweets = False
    replies = False
    original_tweets = False
    favourites_count = False

    if measure == 'TweetRank':
        original_tweets = True
    elif measure == 'TweetCountScore':
        retweets = True
        original_tweets = True
    elif measure == 'Replies':
        replies = True
    elif measure == 'Retweets':
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
                    continue

            elif tweet.in_reply_to_screen_name:
                if replies:
                    count += 1
                    continue

            elif original_tweets:
                count += 1

    return count


def signal_strength():
    # OT1/(OT1+RT1)
    OT1 = count_by_measure('TweetRank')
    RT1 = count_by_measure('Retweets')
    return OT1 / (OT1 + RT1)


def general_activity():
    # General Activity = OT1+RP1+RT1+FT1
    # OT1 = Original Tweets
    OT1 = count_by_measure('TweetRank')
    # RP1 = Number of replies posted by user
    RP1 = count_by_measure('Replies')
    # RT1 = Number of retweets accomplished by the user
    RT1 = count_by_measure('Retweets')
    # FT1 = Number of tweets of other users marked as favorite (liked) by the user
    FT1 = count_by_measure('Likes')

    return OT1 + RP1 + RT1 + FT1


def one_year_ago_tweet(tweet):
    one_year_ago = datetime.datetime.today() - datetime.timedelta(days=365)
    if tweet.created_at >= one_year_ago:
        return True
    return False

# def tweet_rank(name, measure):
#     count=0
#     print("inside TweetRank")
#     for tweet in tweepy.Cursor(api.user_timeline, screen_name=name, exclude_replies=False, include_rts=True).items():
#         if one_year_ago_tweet(tweet):
#             count+=1
#         else:
#             print(count)
#             return count
#     return count

# def tweet_count_score(name):
#     return tweet_rank(name, False)
