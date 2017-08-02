import tweepy
from tweepy import OAuthHandler
import sys
from sentiment import get_sentiment
import json
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

class TwitterClass(object):
    def __init__(self):
        # Twitter API key and token information
        consumer_key = 'XXX'
        consumer_secret = 'XXX'
        access_token = 'XXX'
        access_token_secret = 'XXX'

        # Authentication attempt
        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.auth)    # Create api object
        except:
            print("ERROR: Authentication Failed")
            sys.exit(1)

    # Retrieve and parse tweets for a certain query
    # Determine sentiments for each tweet
    def get_tweets(self, query):
        allTweets = []
        try:
            tweets = self.api.search(q=query,lang='en',rpp=50,include_entities=True)  # Get tweets for query
        except:
            print "Unable to retrieve tweets"
            return

        for tweet in tweets:
            cleanTweet = {}
            sent_categories = get_sentiment(tweet.text) # Retrieve sentiment categories
            cleanTweet = self.parse_sentiments(cleanTweet, sent_categories)  # Store sentiments in cleanTweet
            cleanTweet['text'] = tweet.text
            allTweets.append(cleanTweet)
        return allTweets

    # Parses Watson Tone Analyzer results
    # Returns dictionary with entries in the format [sentiment : score]
    def parse_sentiments(self, cleanTweet, categories):
        cleanTweet['anger'] = categories[0]['tones'][0]['score']
        cleanTweet['disgust'] = categories[0]['tones'][1]['score']
        cleanTweet['fear'] = categories[0]['tones'][2]['score']
        cleanTweet['joy'] = categories[0]['tones'][3]['score']
        cleanTweet['sadness'] = categories[0]['tones'][4]['score']
        cleanTweet['analytical'] = categories[1]['tones'][0]['score']
        cleanTweet['confident'] = categories[1]['tones'][1]['score']
        cleanTweet['tentative'] = categories[1]['tones'][2]['score']
        cleanTweet['openness'] = categories[2]['tones'][0]['score']
        cleanTweet['conscientiousness'] = categories[2]['tones'][1]['score']
        cleanTweet['extraversion'] = categories[2]['tones'][2]['score']
        cleanTweet['agreeableness'] = categories[2]['tones'][3]['score']
        cleanTweet['emotional_range'] = categories[2]['tones'][4]['score']
        return cleanTweet

    def build_plot(self, tweets):
        # Display aggregate sentiments about query topic
        c = Counter()
        for dicts in tweets:
            dicts.pop('text', None) # Remove text field
            c.update(dicts)
        tweets_dict = dict(c)
        avg_sentiments = [t/len(tweets) for t in tweets_dict.values()]  # Calculate average sentiment
        labels = tweets_dict.keys()
        labels_pos = np.arange(len(labels))
        plt.bar(labels_pos, avg_sentiments, align='center', alpha=0.5)
        plt.xticks(labels_pos,labels)
        plt.xticks(rotation=90)
        plt.ylabel("Sentiment Level")
        plt.show()

    # Method for analysis beyond sentiment identification
#    def do_stuff(self, tweets):
#        tweets_json = [json.dumps(status._json) for status in tweets]   # Access tweepy status object via _json property
#        tweets_json = [json.loads(tweet) for tweet in tweets_json]


tc = TwitterClass()
tweets = tc.get_tweets(query="sample")
tc.build_plot(tweets)
