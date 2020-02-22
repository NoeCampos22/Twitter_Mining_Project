"""
Author: Noé Amador Campos Casillo
Email: ama-noe@outlook.com
Description: The python script in charge of using tweepy to the 
mining of tweets given certain key words
Last Update: 22-Feb-2020
"""

# Imports from the Tweepy API
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API

# Imports myTweet class
from myTweet import myTweet

# To check if the file exist
import os.path

# Imports the file with the Twitter App credentials
import Tw_Credentials

# Another imports to parse the json
import json
import time
import csv

# Variable to store the pointer to the CSV file
FILE_MINING = None
# Variable to know if the output file already exists or not
FILE_EXISTS = False
# Variable to count how many tweets were mined
TWEETS_COUNT = 0


def Get_Authentication():
    """
    Get the authentication of the twitter app
    """

    # Validate the Credentials
    Auth = OAuthHandler(Tw_Credentials.CON_KEY,
                        Tw_Credentials.CON_KEY_SECRET)
    # Validate the Acces Tokens
    Auth.set_access_token(Tw_Credentials.ACC_TOKEN,
                          Tw_Credentials.ACC_TOKEN_SECRET)
    return Auth


class MyStreamListener(StreamListener):
    """
    Class in charge of getting the tweets
    """

    def on_error(self, status):
        # status 420 is a warning to stop doing this
        if status == 420:
            return False
        # Print the error status
        print(status)

    def on_data(self, data):
        try:
            # Get the global variables
            global FILE_EXISTS
            global FILE_MINING
            global TWEETS_COUNT

            # Loads the tweet object
            parsed = json.loads(data)

            # Create the tweet object with the info we need and return the json
            Tweet = myTweet(parsed).serialize()

            # Object to write a dictionary on a csv
            dictWriter = csv.DictWriter(
                FILE_MINING, fieldnames=Tweet.keys(), delimiter=',', lineterminator='\n')

            # If the file did not exists
            if not FILE_EXISTS:
                # Writes the headers
                dictWriter.writeheader()
                FILE_EXISTS = True

            # Write the dict on the file
            dictWriter.writerow(Tweet)

            # Plus one to the counter
            TWEETS_COUNT += 1

            # Print in the terminal
            if TWEETS_COUNT % 15 == 0:
                print('.')
            else:
                print('.', end=' ')

            return True

        except BaseException as e:
            print("->Error on data: %s" % str(e))   # Catch the error

        return True


if __name__ == '__main__':
    # An array with the key phrases to filter the tweets
    keyWords = ['china', "parodehombres"]

    print("====== Running App ======")
    try:
        # Start to the listen tweets
        Auth = Get_Authentication()
        myStreamListener = MyStreamListener()
        myStream = Stream(Auth, myStreamListener)

        # Check if the CSV file already exits
        if os.path.exists('coronavirusTweets.csv'):
            FILE_EXISTS = True

        # Open the file where the tweets are going to be write
        FILE_MINING = open('coronavirusTweets.csv', 'a+',
                           encoding='UTF-8', newline='')

        print("\n>> Listening tweets")

        # Filter the tweets by language (spanish) and the keywords
        myStream.filter(languages=["es"], track=keyWords, stall_warnings=True)

    # To stop the program
    except KeyboardInterrupt:
        FILE_MINING.close()
        print("\n\n>> Mining finished.")
        print(str(TWEETS_COUNT) +
              " tweets were written in the coronavirusTweets.csv file")

    except Exception as err:
        # Print if there is an error
        print(err)
