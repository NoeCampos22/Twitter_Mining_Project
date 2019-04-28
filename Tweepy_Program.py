# Imports from the Tweepy API
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API

# The import the MongoDB API
import pymongo	

# Imports myTweet class
from myTweet import myTweet

# Imports the file with the Twitter App credentials
import Tw_Credentials

# Another imports to parse the json
import json
import time


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
            time.sleep(1)
                
            return True

        except BaseException as e:
            print("->Error on data: %s" % str(e))   # Catch the error 

        return True


if __name__ == '__main__':
    # An array with the key phrases to filter the tweets
    keyPhrases = ['#AvengersEndGame, EndGame, #Avengers, Avengers, #Vengadores, #AMLO, AMLO, #Rayados, #OrgulloDeSerRayado, #Tigres, #EstoEsTigres, #Pemex, #BuenDomingo, #FelizDomingo, #Monterrey, #Cancun, #LiguillaMX, @GameOfThrones, #ForTheThrone, #GameofThrones, @Marvel, @Avengers, @Wendy, Roast me']

    print("====== Running App ======")
    try:
        # Get the connection to the cluster in MongoDB Atlas
        connection = pymongo.MongoClient("==============")

        print("Conection to database established")

        database = connection['Tweets']     # Get the Database from the conection
        collection = database['Tweets']     # Get the Collection from the database


        # Start to the listen tweets
        Auth = Get_Authentication()
        myStreamListener = MyStreamListener()
        myStream = Stream(Auth, myStreamListener)
        
        print(">> Listening tweets")

    # Send the array of key words (Hashtags or Mentions)
        myStream.filter(track=keyPhrases,  stall_warnings=True)


    except Exception as err:
	#Print if there is an error
        print(err)

    print("Listo")
