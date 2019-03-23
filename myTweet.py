import re
import datetime

# It is a tweet class but only with the attributes that interest me
class myTweet:

    ## Constructor
    def __init__(self, ogTweet):
        ts = datetime.datetime.strptime(ogTweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
        self.created_at = ts
        self.lang = ogTweet['lang']
        self.text = ogTweet['text']
        self.__getSource(ogTweet)
        self.__getRetweet(ogTweet)
        self.__getHashtags(ogTweet)
        self.__getMentions(ogTweet)
        self.__getMedia(ogTweet)
        self.location = ogTweet['user']['location']
        self.user_verified = ogTweet['user']['verified']
        self.user_followers = ogTweet['user']['followers_count']

    ## Private function to get the source
    def __getSource(self, ogTweet):
        cleanr = re.compile('<.*?>')
        self.source = re.sub(cleanr, '', ogTweet["source"])

    ## Private function to get the retweet information
    def __getRetweet(self, ogTweet):      
        if ogTweet.has_key('retweeted_status') == True:
            self.rt = True
            self.rt_count = ogTweet['retweeted_status']['retweet_count']
            self.fav_count = ogTweet['retweeted_status']['favorite_count']
        else:
            self.rt = False
            self.rt_count = 0
            self.fav_count = 0


    ## Private function to get the hashtag list
    def __getHashtags(self, ogTweet):
        self.hashtags = []

        for hasht in ogTweet['entities']['hashtags']:
            self.hashtags.append(hasht['text'])

    
    ## Private function to get the user mention list
    def __getMentions(self, ogTweet):
        self.mentions = []

        for user in ogTweet['entities']['user_mentions']:
            self.mentions.append(user['screen_name'])

    
    ## Private function to get the media type list
    def __getMedia(self, ogTweet):
        self.media = []

        if ogTweet['entities'].has_key('media') == True:
            for media in ogTweet['entities']['media']:
                self.media.append(media['type'])


    def serialize(self):
        return self.__dict__