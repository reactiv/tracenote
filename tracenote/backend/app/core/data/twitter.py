import json
import os
import tweepy

BEARER_TOKEN = os.getenv('BEARER_TOKEN')
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')


class TwitterReader:
    def __init__(self):
        self.client = tweepy.Client(
            bearer_token=BEARER_TOKEN,
            consumer_key=API_KEY,
            consumer_secret=API_SECRET,
            access_token=ACCESS_TOKEN,
            access_token_secret=ACCESS_TOKEN_SECRET
        )

    def _get_liked_tweets(self, user_name, stop_id=None):
        account = self.client.get_user(username=user_name)
        account_id = account.data.id

        all_liked_tweets = []
        for tweet in tweepy.Paginator(
                self.client.get_liked_tweets,
                account_id,
                tweet_fields=['author_id', 'created_at', 'public_metrics', 'entities']).flatten():
            all_liked_tweets.append(tweet.data)
        return all_liked_tweets

    def get_liked_tweets(self, user_name, stop_id=None):
        return json.load(open('/Users/jamesgin/tracenote/tracenote/backend/app/notebooks/mytweets.json', 'r'))

    def get_users(self, ids):
        batches = [ids[i:i + 100] for i in range(0, len(ids), 100)]
        all_users = []
        for batch in batches:
            all_users.extend(self.client.get_users(ids=batch).data)
        return all_users

