from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
from myTweet import myTweet

import codecs
import json
import unicodedata
import Tw_Credentials

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
            with codecs.open("Tweets.txt", 'a', 'utf-8') as tf:
                encoded = data.encode('utf-8')  # Translate the characters

                parsed = json.loads(encoded)    # Loads the tweet object

                # Create the tweet object with the info we need and return the json
                Tweet = myTweet(parsed).serialize()

                # Get the json format
                JSONtxt = json.dumps(Tweet, indent=2, sort_keys=True)

                # Write the json in the file
                tf.write(JSONtxt)
                tf.write(",\n")


                print(JSONtxt)
                print(" ")
                
            return True

        except BaseException as e:
            print("->Error on data: %s" % str(e))   # Catch the error 

        return True


if __name__ == '__main__':
    print("====== Running App ======")
    
    # Start of the program
    Auth = Get_Authentication()
    myStreamListener = MyStreamListener()
    myStream = Stream(Auth, myStreamListener)
    
    print(">> Listening to tweets")
    myStream.filter(track=['Avengers, avengers, vengadores'])
    
    print("Listo")
