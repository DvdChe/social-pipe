# Don't forget to rename this file to social-pipe.conf

[AUTH]
ConsumerKey = ConsumerKey goes here
ConsumerSecret = Consumer secret goes here
AccessToken = AccessToken goes here
AccessTokenSecret = And Guess what ? This is the access token secret here !

[OPTIONS]
# Dry run allows you to run the script with no retweet, follow or likes.
# It allows you to run it to make tests and see if it works correctly.
# Possible values : True / False.
DryRun = True

# Amount of tweet parsed in each execution
FetchTweet = 20

# Your own screen name here :
ScreenName = <YourScreenName>

# Set region where you want to search
LangSearch = fr


# Keywords that use to parse tweets :
# You can specify many word on the same parameter with | separator
# E/G : plip|plop|plup 

# Keyword for contest
SearchSTR = concours

FollowSTR = 'follow|suivre|suis|suivez'

RetweetSTR = 'rt|retweet'
QuoteSTR = 'tag|taggez|cite|mentionne|mention'
FavSTR = 'like|fav'

# Logger levels:
# 10 DEBUG ( Most verbose )
# 20 INFO
# 30 WARNING
# 40 ERROR

LogLevel = 40

