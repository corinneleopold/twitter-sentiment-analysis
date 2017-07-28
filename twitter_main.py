import tweepy
from tweepy import OAuthHandler
import sys
from sentiment import get_sentiment

class TwitterClass(object):
    def __init__(self):
        # Enter Twitter API key and token information here
        consumer_key = 'XXX'
        consumer_secret = 'XXX'
        access_token = 'XXX'
        access_token_secret = 'XXX'

        # Authentication attempt
        try:
        	self.auth = OAuthHandler(consumer_key, consumer_secret)
        	self.auth.set_access_token(access_token, access_token_secret)
        	self.api = tweepy.API(self.auth)	# Create api object
        except:
            print("ERROR: Authentication Failed")
            sys.exit(1)

    # Retrieve and parse tweets for a certain query
    # Determine sentiments for each tweet
    def get_tweets(self, query):
        allTweets = []
        try:
            tweets = self.api.search(q=query,lang='en',rpp=50,include_entities=True)  # Get tweets for query
            for tweet in tweets:
                cleanTweet = {}
                cleanTweet['text'] = tweet.text
                sent_categories = get_sentiment(tweet.text) # Retrieve sentiment categories
                cleanTweet = parse_sentiments(cleanTweet, sent_categories)  # Update cleanTweet to contain sentiments
        except:
            print "Unable to retrieve tweets"

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

