"""
Author: Noé Amador Campos Casillo
Email: ama-noe@outlook.com
Description: The python script in charge of using tweepy to the 
mining of tweets given certain key words
Last Update: 09-April-2020
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
# Count how many tweets were mined
TWEETS_COUNT = 0
# Count how many tweets were rejected
REJECT_COUNT = 0


def printResult(cChar):
    """
    Function to print a point or a asteristic(error)
    """
    global TWEETS_COUNT

    # Increase the tweets counter
    TWEETS_COUNT += 1

    if TWEETS_COUNT % 35 == 0:
        print(cChar)
    else:
        print(cChar, end=' ')


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
            global REJECT_COUNT

            # Loads the tweet object
            parsed = json.loads(data)

            # This is because sometimes the API returns a Limit notices object
            # More info:
            # https://developer.twitter.com/en/docs/tweets/filter-realtime/overview/statuses-filter
            if 'id_str' in parsed:

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

                # Print a dot
                printResult('.')

            return True

        except Exception as ex:
            REJECT_COUNT += 1
            print(ex)

        return True


if __name__ == '__main__':
    # An array with the key phrases to filter the tweets
    keyWords = ['2019nCoV', 'coronavirus 2019', 'covid-19', 'organizacion mundial de la salud',
                'protocolo de investigacion', 'salud publica', 'OMS', 'secretaria de salud', 'secretario de salud',
                'world health organization', 'centro de salud', 'centro de investigacion', 'anticuerpos monoclonales',
                'Coronavirus Outbreak ', 'tasa de mortalidad', 'virus wuhan', 'no es coronavirus', 'C-O-V-I-D',
                'actualización coronavirus', 'coronavirus', 'covid', 'COVID', '#Coronavirus',
                '#coronavirus', '#COVID19', '#China', 'contagios', 'brotes', 'epidemias', 'mascarillas',
                'Centro de Salud', 'pacientes', 'casos positivos', '#CoronavirusMexico', '#CoronavirusChino',
                '#CoronavirusOutbreak']

    print("\n====== Running App ======")

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

        # Close the CSV File
        FILE_MINING.close()

        print("\n\n>> Mining finished.")
        print(str(TWEETS_COUNT - REJECT_COUNT) +
              " tweets were written in the coronavirusTweets.csv file")

    # Catch the excepetion
    except Exception as err:
        print()
        print(err)
