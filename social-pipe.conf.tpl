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


# Determine how many tweets will be analysed in the research
FetchTweet = 5
SearchSTR = concours
FollowSTR = follow
RetweetSTR = rt|retweet
QuoteSTR = tag|cite|mention
FavSTR = fav|like
