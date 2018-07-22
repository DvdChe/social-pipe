import tweepy
import configparser
import re
import pickle

from os import path, remove

###############################################################################

# General config
# ==============

FlagFile             = '/tmp/social-pipe.flag' # Flag file to avoid multiple exec
RetweetedHistoryFile = path.dirname(path.abspath(__file__))+'/retweeted.bin' # Previously retweeted
FollowedHistoryFile  = path.dirname(path.abspath(__file__))+'/followed.bin'  # Previously followed
AuthConfFile         = path.dirname(path.abspath(__file__))+'/social-pipe.conf'     # auth conf
NFetchTweet          = 50                                                     # Number of loaded tweets
Log                  = ''

# Avoiding multiple executions
# ============================

#if path.isfile(FlagFile):
#    print("Error : ", FlagFile,"exists. Is Social pip is already running ?")
#    exit(1)
#
#open(FlagFile, 'a')

###############################################################################

# Parsing conf file:
# ==================
conf = configparser.ConfigParser()
conf.read (str(AuthConfFile)    )

consumer_key        = conf['AUTH']['ConsumerKey']
consumer_secret     = conf['AUTH']['ConsumerSecret']
access_token        = conf['AUTH']['AccessToken']
access_token_secret = conf['AUTH']['AccessTokenSecret']

DryRunConf          = conf['OPTIONS']['DryRun']

if DryRunConf == 'True':
    DryRun = True

else:
    DryRun = False

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
        ).items(NFetchTweet)

 ##############################################################################

 # Lets load allready retweeded stuffs
 # ==================================

if path.isfile(str(RetweetedHistoryFile)):
    f = open(RetweetedHistoryFile, 'rb')
    tRetweeted = pickle.load(f)

else:
    tRetweeted = []

if path.isfile(str(FollowedHistoryFile)):
    f = open(FollowedHistoryFile, 'rb')
    tFollowed = pickle.load(f)

else:
    tFollowed = []

###############################################################################

# Parsing the tweet to know what to do.
# ====================================

for tweet in ContestTweet:

    # If it's a retweet :
    # ===================

    if hasattr(tweet, 'retweeted_status'):

        TweetText = tweet.retweeted_status.full_text
        TweetId   = tweet.retweeted_status.id
        Author = tweet.retweeted_status.user.id_str
        AuthorScrenName = tweet.retweeted_status.user.id_str

        if str(TweetId) not in tRetweeted:

            # Let's find if there is suckers to follow:
            # =========================================

            if re.search('follow',TweetText,re.IGNORECASE):
                ScreenNames = re.findall(r'[@]\w+',TweetText)

                print(ScreenNames)

                #Log += 'Following now : '

                for ScreenName in ScreenNames:

                    user=(api.get_user(screen_name = ScreenName))
                    print('I will have to follow', ScreenName,'/',user.id)

                    if not DryRun:
                        api.create_friendship(user.id)

                    tFollowed.append(user.id)
                    #Log += account,','

            if Author not in tFollowed:
                if not DryRun:
                    api.create_friendship(Author)
                tFollowed.append(Author)
                #Log += 'Following Author :',str(AuthorScrenName)
                #print(type(AuthorScrenName))

            # If It needs to retweet
            # ======================
            if TweetId not in tRetweeted :

                if re.search('rt',TweetText,re.IGNORECASE) or re.search('retweet',TweetText,re.IGNORECASE):

                    try:
                        if not DryRun:
                            api.retweet(TweetId)
                    except:
                        pass

                    tRetweeted.append(str(TweetId))

#print(tRetweeted)
#print(tFollowed)
fp = open(str(RetweetedHistoryFile), 'wb')
pickle.dump(tRetweeted,fp)
fp.close()

fp = open(str(FollowedHistoryFile), 'wb')
pickle.dump(tFollowed,fp)
fp.close()

#print(Log)
#remove(FlagFile)
#print(type(Log))
