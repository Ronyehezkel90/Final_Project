import tweepy
from tweepy import OAuthHandler


class Connector:
    def __init__(self):
        consumer_key = 'P819tguRDdVJf8nXP36CquWMm'
        consumer_secret = 'sdgPVTpaOUtnTbe019Mx641rc7qGDN89nEVBKG7H5OoCWkew3D'
        access_token = '773769927333408768-qTYJOrWCAzRMx5juSpEhkkzu454vyrO'
        access_secret = 'oyBxEVjOYgqpbvU5rwC7QYmz46NDc4OpNGPxRfbmBQEee'
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)
        self.api = tweepy.API(auth)

    def get_rate_limits(self):
        return self.api.rate_limit_status()
