# Tweets Mining Project

It is a project for a Hackathon, that had as main topic the COVID-19, in which I was in charge of mining tweets. The resulting dataset was used to analyze sentiment, identify entities and keywords, among other things to make a series of dashboards and also try to identify fake news that were shared on this social network.

The script use the python API named [Tweepy](http://www.tweepy.org/), specifically the [Stream Tweets functionality](http://docs.tweepy.org/en/latest/streaming_how_to.html), to listen tweets and filter them. Then, saves all the important attributes of each tweet and finally, writes the tweets on a CSV file with the the [CSV library](https://docs.python.org/3/library/csv.html).

## Files

### Tweepy_Program.py
It is the main program. It is where the authentication from the twitter app is obtained, and the tweets are listened, filtered and stored on the CSV file.

### myTweet.py 
It is a Tweet class I created to store only the important attributes from the original [Tweet object](https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/intro-to-tweet-json) that gets from Tweepy API. 

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