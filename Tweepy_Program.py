from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
from myTweet import myTweet

import codecs
import json
import unicodedata
import Tw_Credentials
import pymongo

collection = ""

# Get the authentication of the twitter app
def Get_Authentication():
    # Validate the Con
    Auth = OAuthHandler(Tw_Credentials.CON_KEY,
                        Tw_Credentials.CON_KEY_SECRET)
    # Validate the Acces Tokens
    Auth.set_access_token(Tw_Credentials.ACC_TOKEN,
                        Tw_Credentials.ACC_TOKEN_SECRET)
    return Auth


class MyStreamListener(StreamListener):

    def on_status(self, status):
        print(status.text.encode("ascii", errors='replace'))
        print("-"*10)



        # If it gets an error
    def on_error(self, status):
        # status 420 is a warning to stop doing this
        if status == 420:
            return False
        # Print the error status
        print(status)




    # If it gets a data
    def on_data(self, data):
        try:
            encoded = data.encode('utf-8')  # Translate the characters

            parsed = json.loads(encoded)    # Loads the tweet object

            # Create the tweet object with the info we need and return the json
            Tweet = myTweet(parsed).serialize()

            # Send the tweet to the database on MongoDB Cluster
            collection.insert_one(Tweet)

            # To know it has saved a tweet
            print(".")
                
            return True

        except BaseException as e:
            print("->Error on data: %s" % str(e))   # Catch the error 

        return True


if __name__ == '__main__':
    print("====== Running App ======")

    try:
        # Get the connection to the cluster
        connection = pymongo.MongoClient("mongodb://NoeCampos:221999@twitterproject-shard-00-00-qncgc.mongodb.net:27017,twitterproject-shard-00-01-qncgc.mongodb.net:27017,twitterproject-shard-00-02-qncgc.mongodb.net:27017/test?ssl=true&replicaSet=TwitterProject-shard-0&authSource=admin&retryWrites=true")
        print("Conection to database established")
        database = connection['Tweets']     # Get the Database from the conection
        collection = database['Tweets']     # Get the Collection from the database


        # Start of the program
        Auth = Get_Authentication()
        myStreamListener = MyStreamListener()
        myStream = Stream(Auth, myStreamListener)
        
        print(">> Listening tweets")
        myStream.filter(track=['#AvengersEndGame, #Avengers, #Vengadores'])

        #with open('Tweets.txt') as json_file:  
        #    data = json.load(json_file)
        #    collection.insert_many(data,True)
        #    print(data)


    except Exception as err:
        # do whatever you need
        print(err)

    print("Listo")
