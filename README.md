# Social Pipe. A bot to win lot of useless shits.

## BIG NEWS : Social-pipe is more customizable with the conf file. Look at the .conf section !

## DISCLAIMER 

Twitter doesn't really like bots, so use this program at your own risks. I recommend you to create a specific account to use it.

## WTF ?

Few times ago, i saw a blog article talking about a guy who tried to make a twitter bot, designed to find contests on twitter and participate to it. I tried to reproduce this idea on my own way. It's mainly an opportunity for me to make something on python.

## WTF are theses contests ?

You know, the stupid contest which consists to like, retweet and follow in order to win stuff if you're chosen at random...

## Install

This program is developped in Python 3.6. I would highly recommand you to use virtualenv or pew to make it works, cause it has many dependencies.

### Requirements :

- Python 3.6 or maybe 3.5
- Virtualenv or pew.
- Twitter API tokens. 
  - To get tokens, go here : https://developer.twitter.com. 
  - More informations here : https://developer.twitter.com/en/docs/basics/authentication/guides/access-tokens.html
   

### Prepare your env :

```bash
   
   $ cd social-pipe
   $ python3 -m virtualenv .
   $ source bin/activate
   $ pip -r install requirements.txt

```

### Prepare your social-pipe.conf file :

```
   mv social-pipe.conf.tpl social-pipe.conf
   
```
Then edit ```social-pipe.conf``` and set your tokens.

```
[AUTH]
ConsumerKey = ConsumerKey goes here
ConsumerSecret = Consumer secret goes here
AccessToken = AccessToken goes here
AccessTokenSecret = And Guess what ? This is the access token secret here !

```

Set others options : 

```
[OPTIONS]
# Dry run allows you to run the script with no retweet, follow or likes.
# It allows you to run it to make tests and see if it works correctly.
# Possible values : True / False.
DryRun = True

# Amount of tweet parsed in each execution
FetchTweet = <INT>

# Your own screen name here :
ScreenName = <YourScreenName>

# Set region where you want to search
LangSearch = <Contrycode>

```

### Keyword configuration :

Firstly, social-pipe will look for tweet which contains the "contest" keyword. You can specify the word "contest" on your own language

Then, it will look for the keyword "follow", and look for screen names mentionned and finally follow theses names. 

Third, it will lok for the "retweet" keyword and and proceed to the retweet...

Then this is the same thing for quote friend (todo) and favorite tweet.

All of theses keywords can be tuned according your own language. 
Here is an example for french contests :

```
LangSearch = fr
SearchSTR = concours
FollowSTR = follow
RetweetSTR = rt|retweet
QuoteSTR = tag|cite|mention
FavSTR = fav|like
```

As you can see, you can specify many words for different use cases.

### Use it :

Now, you should be ready to play :

```
   $ python social-pipe.py
```

Of Course, if you have more stuff to tune, you can open an issue or try to do it by yourself =)

Enjoy !!!!

Oh, one more thing : 

DON'T BLAME ME IF YOU ARE BANNED BY TWITTER !!!!!!
