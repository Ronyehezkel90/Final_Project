import tweepy
from tweepy import OAuthHandler

class Connector:
    def __init__(self):
        consumer_key = 'P819tguRDdVJf8nXP36CquWMm'
        consumer_secret = 'sdgPVTpaOUtnTbe019Mx641rc7qGDN89nEVBKG7H5OoCWkew3D'
        self.auth = OAuthHandler(consumer_key, consumer_secret)

    def get_rate_limits(self):
        return self.api.rate_limit_status()

    def application_authorization(self):
        access_token = '773769927333408768-qTYJOrWCAzRMx5juSpEhkkzu454vyrO'
        access_secret = 'oyBxEVjOYgqpbvU5rwC7QYmz46NDc4OpNGPxRfbmBQEee'
        self.auth.set_access_token(access_token, access_secret)
        self.api = tweepy.API(self.auth)

    def user_authorization(self, verifier):
        self.auth.get_access_token(verifier)
        self.api = tweepy.API(self.auth)
