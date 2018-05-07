import tweepy
import sys
import twitter
from tweepy import OAuthHandler


class TObject(object):
    """
    Generic Twitter Class for sentiment analysis.
    """
    def __init__(self, auth='males'):
        from twitter_apps.Keys import provide_keys
        """
        Class constructor or initialization method.
        """
        key = provide_keys(auth)

        try:
            self.api = twitter.Api(consumer_key=key['consumer_key'],
                                   consumer_secret=key['consumer_secret'],
                                   access_token_key=key['access_token_key'],
                                   access_token_secret=key['access_token_secret'])
        except Exception as e:
            print(e)
            print("Authentication Failed...", file=sys.stderr)


class TwitterObject(object):
    """
    Generic Twitter Class for sentiment analysis.
    """

    def __init__(self, auth='males'):
        from twitter_apps.Keys import provide_keys
        """
        Class constructor or initialization method.
        """
        # keys and tokens from the Twitter Dev Console
        key = provide_keys(auth)

        consumer_key = key['consumer_key']
        consumer_secret = key['consumer_secret']
        access_token = key['access_token_key']
        access_token_secret = key['access_token_secret']

        # attempt authentication

        # create OAuthHandler object
        self.auth = OAuthHandler(consumer_key, consumer_secret)

        # set access token and secret
        self.auth.set_access_token(access_token, access_token_secret)

        try:
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)

        except:
            print("Error: Authentication Failed")
            sys.exit(-1)

    def get_friends(self, screen_name):
        try:
            return self.api.friends_ids(screen_name=screen_name, wait_on_rate_limit=True,
                                        wait_on_rate_limit_notify=True)
        except:
            return "Protected"

    def get_rate_limit(self):
        return self.api.rate_limit_status()
