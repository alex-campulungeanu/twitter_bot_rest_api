import tweepy
from flask import current_app

from app import app

def create_api():
    consumer_key = app.config["TWITTER_API_KEY"]
    consumer_secret = app.config["TWITTER_API_SECRET_KEY"]
    access_token = app.config["TWITTER_ACCESS_TOKEN"]
    access_token_secret = app.config["TWITTER_ACCESS_TOKEN_SECRET"]

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        current_app.logger.error("Error creating Twitter API", exc_info=True)
        raise e
    return api