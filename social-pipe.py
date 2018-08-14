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
import logging

from logging.handlers import RotatingFileHandler
from os import path, remove


###############################################################################

# Logging configuration
# =====================

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')

file_handler = RotatingFileHandler('social-pipe.log', 'a', 1000000, 1)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
logger.addHandler(file_handler)


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

if path.isfile(FlagFile):
    logging.error("FlagFile exists. Is Social pipe is already running ?")
    exit(1)

StartTime = datetime.datetime.now()
logging.info('============ Starting Social-Pipe @%s ============', StartTime)

open(FlagFile, 'a')

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

LangSearch = str(conf['OPTIONS']['LangSearch'])

ContestSearchSTR = str(conf['OPTIONS']['SearchSTR'])
FollowSTR = str(conf['OPTIONS']['FollowSTR'])
RetweetSTR = str(conf['OPTIONS']['RetweetSTR'])
QuoteSTR = str(conf['OPTIONS']['QuoteSTR'])
FavSTR = str(conf['OPTIONS']['FavSTR'])

if DryRunConf == 'True':
    DryRun = True
    logging.info('This is a dry run. Nothing will happens.')

else:
    DryRun = False

###############################################################################

# Connect to Twitter:
# ===================

try:
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

except tweepy.TweepError as e:
    logging.error(e)
    remove(FlagFile)
    exit(e.message[0]['code'])


###############################################################################

# Get list of follewers :
# ======================

tFollowers = []

if not path.isfile(FollowerNameFile):

    logging.info('No followers list file found. Generating... It may take a while')

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


def SearchTweet(Keyword, lang, NumFetch):

    out = tweepy.Cursor(
            api.search, q=Keyword,
            lang=lang,
            tweet_mode='extended'
            ).items(NumFetch)
    return out


ContestTweet = SearchTweet(ContestSearchSTR, LangSearch, NFetchTweet)


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

try:

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

                if re.search(FollowSTR, TweetText, re.IGNORECASE):
                    ScreenNames = re.findall(r'[@]\w+', TweetText)

                    for ScreenName in ScreenNames:

                        try:
                            user = api.get_user(screen_name=ScreenName)

                        except tweepy.error.TweepError:
                            logging.warning('%s may be already followed', user.screen_name)
                            pass

                        else:
                            if not DryRun:
                                api.create_friendship(user.id)
                                logging.info('Followed : %s ', ScreenName)


                if not DryRun:
                    api.create_friendship(Author)

                # If It needs to retweet
                # ======================
                if TweetId not in tRetweeted:

                    RegTweet = re.compile(RetweetSTR, re.IGNORECASE)
                    RegTag = re.compile(QuoteSTR, re.IGNORECASE)

                    if re.search(RegTweet, TweetText):
                        try:
                            if not DryRun:
                                retweet = api.retweet(TweetId)

                            logging.info('Retweeted : %s',TweetId)

                        except tweepy.error.TweepError:
                            logging.info('Warning : Tweet  %s may already RT',TweetId )
                            pass

                        tRetweeted.append(str(TweetId))

                    # If it needs to be liked
                    # =======================
                    RegFav = re.compile(FavSTR, re.IGNORECASE)
                    if re.search(RegFav, TweetText):
                        try:
                            if not DryRun:
                                api.create_favorite(TweetId)
                                logging.info('Favorited : %s', TweetId)
                        except tweepy.error.TweepError:
                            logging.info('Warning : Tweet  %s already in fav', TweetId )
                            pass

except tweepy.error.TweepError:
    logging.error('Unexpected error')
    pass

fp = open(str(RetweetedHistoryFile), 'wb')
pickle.dump(tRetweeted, fp)
fp.close()

StopTime = datetime.datetime.now()

logging.info('============ Social-Pipe Stopped @ %s ============', StopTime)

remove(FlagFile)
