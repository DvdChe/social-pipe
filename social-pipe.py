import tweepy
import configparser
import json
import re

from pickle import dump, load
from os import path, remove

###############################################################################

# General config
# ==============

FlagFile = '/tmp/social-pipe.flag'
HistoryFile = 'retweeted.bin'

# Avoiding multiple executions
# ============================

if path.isfile(FlagFile):
    exit(1)

open(FlagFile, 'a')

###############################################################################

# Parsing conf file:
# ==================
conf = configparser.ConfigParser()
conf.read ('auth.conf')

consumer_key        = conf['AUTH']['ConsumerKey']
consumer_secret     = conf['AUTH']['ConsumerSecret']
access_token        = conf['AUTH']['AccessToken']
access_token_secret = conf['AUTH']['AccessTokenSecret']

###############################################################################

# Connect to Twitter:
# ===================

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

###############################################################################

# Lets search Contest tweet
# =========================

ContestTweet = tweepy.Cursor(
        api.search,q='concours',
        lang='fr',
        tweet_mode='extended'
        ).items(50)

###############################################################################

# Parsing the tweet to know what to do.
# ====================================

tRetweeted = []
tFollowed  = []

for tweet in ContestTweet:

    # If it's a retweet :
    # ===================

    if hasattr(tweet, 'retweeted_status'):

        TweetText = tweet.retweeted_status.full_text
        TweetId   = tweet.retweeted_status.id

        if TweetId not in tRetweeted:

            print('----------------------')

            # Let's find if there is suckers to follow:
            # =========================================

            if re.search('follow',TweetText,re.IGNORECASE):
                accounts=re.findall(r'[@]\w+',TweetText)

                for account in accounts:
                    print('I will have to follow', account)
                    tFollowed.append(account)

            # If It needs to retweet
            # ======================

            if re.search('rt',TweetText,re.IGNORECASE) or re.search('retweet',TweetText,re.IGNORECASE):
                print("I must retweet ",TweetId)
                print(TweetText)
                tRetweeted.append(str(TweetId))

            print('----------------------')

print(tRetweeted)

fp = open(HistoryFile, 'wb')
dump(tRetweeted,fp)
fp.close()

remove(FlagFile)
