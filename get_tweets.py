from dotenv import load_dotenv, find_dotenv
import pandas as pd
import tweepy
import time
import os

""" 
Load .env file containing 'CONSUMER_KEY' and 'CONSUMER_SECRET' variables
"""
load_dotenv(find_dotenv(), verbose=True)

consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')

# Connect to twitter API
auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth)

def get_related_tweets(text_query):
    # list to store tweets
    tweets_list = []
    # no of tweets
    count = 50
    try:
        # Pulling individual tweets from query
        for tweet in api.search(q=text_query, count=count, lang='en'):
            # Adding to list that contains all tweets
            tweets_list.append({'created_at': tweet.created_at,
                                'tweet_id': tweet.id,
                                'tweet_text': tweet.text})
        return pd.DataFrame.from_dict(tweets_list)

    except BaseException as e:
        print('failed on_status,', str(e))
        time.sleep(3)

if __name__ == "__main__":
    print(f"Number of extracted tweets : {get_related_tweets('covid').shape[0]}")