# Social Pipe. A bot to win lot of useless shits.

## WTF ?

Few times ago, i saw an blog article talking about a guy who tried to make a twitter bot, designed to find contests on twitter and participate to it. I tried to reproduce this idea on my own way. It's mainly an opportunity for me to make something on python.

## WTF are theses contests ?

You know, the stupid contest which consists to like, retweet and follow in order to win stuff if you're chosen at random...

## Install

This program is developped in Python 3.6. I would highly recommand you to user virtualenv or pew to make it works, cause it has many dependencies to setup.

### Requirements :

    - Python 3.6 or 3.5 ?
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

### Use it :

Now, you should be ready to play :

```
   $ python social-pipe.py
```

By default, the bot will look for posts containing the "concours" word ("contest" in French) and fetch the first 50 words.

It will look if it's needed to follow people to participate, and it will check if the tweet needs to be added in favorite. Finaly, the author of tweet will be followed.

### WHAT IF I'M NOT AN OMELETTE DU FROMAGE ??!

Edit social-pipe.py, look for the following block

```python
###############################################################################

# Lets search Contest tweet
# =========================

ContestTweet = tweepy.Cursor(
        api.search,q='concours',
        lang='fr',
        tweet_mode='extended'
        ).items(NFetchTweet)
```

And if you're a English mate, 

```python
###############################################################################

# Lets search Contest tweet
# =========================

ContestTweet = tweepy.Cursor(
        api.search,q='contest', # Switched to contest
        lang='en',              # Switched to en
        tweet_mode='extended'
        ).items(NFetchTweet)
```

As you can see, this program use Tweepy lib.
With the search method, you can add more criteria such geolocation. Relevant if you're an US guy or an Australian, for instance.

You will also have to locate theses blocs :

```python

# Let's find if there is suckers to follow:
# =========================================

if re.search('follow',TweetText,re.IGNORECASE):
    ScreenNames = re.findall(r'[@]\w+',TweetText)


#[...]

# If it needs to be liked
# =======================

# Replace the "fav" word by the terme which means add to favorite or like in your own language
if re.search('fav',TweetText,re.IGNORECASE):

#[...]

```

Of Course, if you have more stuff to tune, you can open an issue or try to do it by yourself =)


