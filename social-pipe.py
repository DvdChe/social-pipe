#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#                    Version 2, December 2004
#
# Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>
#
# Everyone is permitted to copy and distribute verbatim or modified
# copies of this license document, and changing it is allowed as long
# as the name is changed.
#
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#
#  0. You just DO WHAT THE FUCK YOU WANT TO.


import tweepy
import configparser
import re
import pickle
import datetime
import random

from os import path, remove

###############################################################################

# General config
# ==============

CurrentLocation = str(path.dirname(path.abspath(__file__)))

FlagFile = str('/tmp/social-pipe.flag')
RetweetedHistoryFile = CurrentLocation+'/retweeted.bin'
FollowerNameFile = CurrentLocation+'/followers.bin'
AuthConfFile = CurrentLocation+'/social-pipe.conf'
Log = str('')

# Avoiding multiple executions
# ============================

#if path.isfile(FlagFile):
#    print("Error : ", FlagFile, "exists. Is Social pip is already running ?")
#    exit(1)

StartTime = datetime.datetime.now()
print('============ Starting Social-Pipe @', StartTime, ' ============')

#open(FlagFile, 'a')

###############################################################################

# Parsing conf file:
# ==================
conf = configparser.ConfigParser()
conf.read(str(AuthConfFile))

consumer_key = str(conf['AUTH']['ConsumerKey'])
consumer_secret = str(conf['AUTH']['ConsumerSecret'])
access_token = str(conf['AUTH']['AccessToken'])
access_token_secret = str(conf['AUTH']['AccessTokenSecret'])

DryRunConf = str(conf['OPTIONS']['DryRun'])
NFetchTweet = int(conf['OPTIONS']['FetchTweet'])
OwnScreenName = str(conf['OPTIONS']['ScreenName'])

if DryRunConf == 'True':
    DryRun = True
    print('This is a dry run. Nothing will happens.')

else:
    DryRun = False

###############################################################################

# Connect to Twitter:
# ===================

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

###############################################################################

# Get list of follewers :
# ======================

tFollowers = []

if not path.isfile(FollowerNameFile):

    print('No followers list file found. Generating... It may take a while')

    followers = tweepy.Cursor(api.followers_ids,
                              screen_name=OwnScreenName).items()

    for follower in followers:
        UserObj = api.get_user(user_id=follower)
        # Using screen_name cause it's more easy to parse when it's needed
        # check if user is already followed
        tFollowers.append('@'+UserObj.screen_name)

    fp = open(str(FollowerNameFile), 'wb')
    pickle.dump(tFollowers, fp)
    fp.close()

f = open(FollowerNameFile, 'rb')
tFollowers = pickle.load(f)

###############################################################################

# Lets search Contest tweet
# =========================

ContestTweet = tweepy.Cursor(
        api.search, q='concours',
        lang='fr',
        tweet_mode='extended'
        ).items(NFetchTweet)

##############################################################################

# Lets load allready retweeded stuffs
# ==================================

if path.isfile(str(RetweetedHistoryFile)):
    f = open(RetweetedHistoryFile, 'rb')
    tRetweeted = pickle.load(f)

else:
    tRetweeted = []

###############################################################################

# Parsing the tweet to know what to do.
# ====================================

for tweet in ContestTweet:

    # If it's a retweet :
    # ===================

    if hasattr(tweet, 'retweeted_status'):

        TweetText = tweet.retweeted_status.full_text
        TweetId = tweet.retweeted_status.id
        Author = tweet.retweeted_status.user.id_str
        AuthorScrenName = tweet.retweeted_status.user.id_str

        if str(TweetId) not in tRetweeted:

            # Let's find if there is suckers to follow:
            # =========================================

            if re.search('follow', TweetText, re.IGNORECASE):
                ScreenNames = re.findall(r'[@]\w+', TweetText)

                for ScreenName in ScreenNames:

                    try:
                        user = api.get_user(screen_name=ScreenName)

                        if not DryRun:
                            api.create_friendship(user.id)

                        print('Followed :', ScreenName)

                    except:
                        pass

            if not DryRun:
                api.create_friendship(Author)

            # If It needs to retweet
            # ======================
            if TweetId not in tRetweeted:

                RegTweet = re.compile('rt|retweet', re.IGNORECASE)
                RegTag = re.compile('tag|cite|mention', re.IGNORECASE)

                if re.search(RegTweet, TweetText):
                    try:
                        if not DryRun:
                            retweet = api.retweet(TweetId)

                        print('Retweeted :', TweetId)

                    except:
                        pass

                    tRetweeted.append(str(TweetId))

                # If it needs to be liked
                # =======================
                RegFav = re.compile('fav|like', re.IGNORECASE)
                if re.search(RegFav, TweetText):
                    try:
                        if not DryRun:
                            api.create_favorite(TweetId)
                            print('Favorited : ', TweetId)
                    except:
                        pass


fp = open(str(RetweetedHistoryFile), 'wb')
pickle.dump(tRetweeted, fp)
fp.close()

StopTime = datetime.datetime.now()

print('============ Social-Pipe Stopped @ ', StopTime, ' ============')

remove(FlagFile)
