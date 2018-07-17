import tweepy
import sys 
import configparser


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

#Send stdin to twitter :
for line in sys.stdin:
    api.update_status(line)

