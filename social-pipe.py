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
AuthConfFile         = path.dirname(path.abspath(__file__))+'/auth.conf'     # auth conf
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
                accounts = re.findall(r'[@]\w+',TweetText)

                #Log += 'Following now : '

                for account in accounts:
                    print('I will have to follow', account)
                    #api.create_friendship(account)
                    tFollowed.append(account)
                    #Log += account,','

            if Author not in tFollowed:
                api.create_friendship(Author)
                tFollowed.append(Author)
                #Log += 'Following Author :',str(AuthorScrenName)
                print(type(AuthorScrenName))

            # If It needs to retweet
            # ======================
            if TweetId not in tRetweeted :

                if re.search('rt',TweetText,re.IGNORECASE) or re.search('retweet',TweetText,re.IGNORECASE):

                    try:
                        api.retweet(TweetId)
                    except:
                        pass

                    tRetweeted.append(str(TweetId))

print(tRetweeted)
print(tFollowed)
fp = open(str(RetweetedHistoryFile), 'wb')
pickle.dump(tRetweeted,fp)
fp.close()

fp = open(str(FollowedHistoryFile), 'wb')
pickle.dump(tFollowed,fp)
fp.close()

#print(Log)
#remove(FlagFile)
#print(type(Log))
