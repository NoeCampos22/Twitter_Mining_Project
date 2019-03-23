# Tweets Mining Project

It is a project from my advanced database class where I needed to make a program in [Python](https://www.python.org/) to get and save tweets in a NoSQL database. 

I used the python API named [Tweepy](http://www.tweepy.org/) to listen or even write tweets and [PyMongo](https://api.mongodb.com/python/current/) to make the connection to my database in [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) and save the tweets.

## Files

### myTweet.py 
It is a Tweet class I created to store only the attributes that I need from the original [Tweet object](https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/intro-to-tweet-json) that gets from Tweepy API. 

Attributes:
- created_at:       Creation date
- lang:             Language
- text:             Text from the tweet
- source:           From which device the tweet was made
- rt:               If it is a retweet or not
- rt_count:         Number of retweets
- fav_count:        Number of favs
- hashtags[]:       Array of hashtags
- mentions[]:       Array of mentions
- media[]:          Array of media
- location:         The location
- user_verified:    If the user it is verified or not
- user_followers:   Number of followers

### Tw_Credentials.py
It is a file that contains the Consumer API Keys and the Access tokens from the Twitter App created from a [Twitter Developer Account](https://developer.twitter.com/en/apply-for-access.html).

**Note:** Yo need to change the - from
```
ACC_TOKEN = "-"
ACC_TOKEN_SECRET = "-"
CON_KEY = "-"
CON_KEY_SECRET = "-"
```
for the keys given in the settings of your app.

### Tweepy_Program.py
It is the main program where gets the authentication from the twitter app, make the connection to the data base, listen and store the tweets.

**Note:** Yo need to change the ======== from
```
connection = pymongo.MongoClient("========")
```
for the URL from the MongoDB Cluster.

### runPyScript.sh
Since I made the program in ubuntu, I also made a Shell script to run the python script for 10 minutes and then kill the process.


## Another Sources
- [PyMongo Tutorial](https://www.mongodb.com/blog/post/getting-started-with-python-and-mongodb)
- [MongoDB Conection](https://pythondata.com/collecting-storing-tweets-with-python-and-mongodb/)



