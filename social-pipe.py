import tweepy
import sys 
import configparser
import json
import re

#Parsing conf file:
conf = configparser.ConfigParser()
conf.read ('auth.conf')

consumer_key        = conf['AUTH']['ConsumerKey']
consumer_secret     = conf['AUTH']['ConsumerSecret'] 
access_token        = conf['AUTH']['AccessToken'] 
access_token_secret = conf['AUTH']['AccessTokenSecret'] 


#Connect to Twitter:
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

ContestTweet = tweepy.Cursor(
        api.search,q='concours', 
        lang='fr',
        tweet_mode='extended'
        ).items(5)

for tweet in ContestTweet:
    
    if hasattr(tweet, 'retweeted_status'):
        
        TweetText = tweet.retweeted_status.full_text
        TweetId   = tweet.retweeted_status.id
        print('----------------------')
        #print(TweetText)
        
        #Let's find if there is suckers to follow: 
        if re.search('follow',TweetText,re.IGNORECASE):
            accounts=re.findall(r'[@]\w+',TweetText)
            for account in accounts:
                print('I will have to follow', account)

        #print('Have to retweet ID', TweetId)
        
    print('----------------------')
