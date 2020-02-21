# Imports from the Tweepy API
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API

# Imports myTweet class
from myTweet import myTweet

# Imports the file with the Twitter App credentials
import Tw_Credentials

# Another imports to parse the json
import json
import time


def Get_Authentication():
    # Get the authentication of the twitter app
    # Validate the Con
    Auth = OAuthHandler(Tw_Credentials.CON_KEY,
                        Tw_Credentials.CON_KEY_SECRET)
    # Validate the Acces Tokens
    Auth.set_access_token(Tw_Credentials.ACC_TOKEN,
                          Tw_Credentials.ACC_TOKEN_SECRET)
    return Auth


class MyStreamListener(StreamListener):

    def on_error(self, status):
        # status 420 is a warning to stop doing this
        if status == 420:
            return False
        # Print the error status
        print(status)

    def on_data(self, data):
        try:
            encoded = data.encode('utf-8')  # Translate the characters

            parsed = json.loads(encoded)    # Loads the tweet object

            # Create the tweet object with the info we need and return the json
            Tweet = myTweet(parsed).serialize()

            return True

        except BaseException as e:
            print("->Error on data: %s" % str(e))   # Catch the error

        return True


if __name__ == '__main__':
    # An array with the key phrases to filter the tweets
    keyPhrases = ['']

    print("====== Running App ======")
    try:
        # Start to the listen tweets
        Auth = Get_Authentication()
        myStreamListener = MyStreamListener()
        myStream = Stream(Auth, myStreamListener)

        print(">> Listening tweets")

    # Send the array of key words (Hashtags or Mentions)
        myStream.filter(track=keyPhrases,  stall_warnings=True)

    except Exception as err:
        # Print if there is an error
        print(err)

    print("Listo")
