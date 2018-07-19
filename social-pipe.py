import tweepy
import configparser
import json
import re
import csv

from os import path, remove

#Avoiding multiple executions
PathFlag = '/tmp/social-pipe.flag'
if path.isfile(PathFlag):
    exit(1)    
    
open(PathFlag, 'a')

#with open('retweeted.csv',a) as retweeted_csvfile:
#    reader = retweeted_csv.reader(retweeted_csvfile, 
#                                  delimiter=',', 
#                                  quotechar='|')
#
#    writer = retweeted_csv.writerow(retweeted_csvfile, 
#                                    delimiter=',', 
#                                    quotechar='|',
#                                    quoting=csv.QUOTE_MINIMAL)





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

#Lets search Contest tweet
ContestTweet = tweepy.Cursor(
        api.search,q='concours', 
        lang='fr',
        tweet_mode='extended'
        ).items(5)

#Parsing the tweet to know what to do.
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

        #If It need to retweet 
        if re.search('rt',TweetText,re.IGNORECASE) or re.search('retweet',TweetText,re.IGNORECASE):
            print("I must retweet ",TweetId)
            print(TweetText)

        
    print('----------------------')

remove(PathFlag)
