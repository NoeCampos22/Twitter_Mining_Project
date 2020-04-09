"""
Author: Noé Amador Campos Casillo
Email: ama-noe@outlook.com
Description: It is a class to filter and store just the data 
I need from the original Tweet object.
Last Update: 09-April-2020
"""

import re
import datetime


class myTweet:
    """
    A class to summarize the original Tweet object received from
    Tweepy (Twitter API for Python)
    """

    def __init__(self, ogTweet):
        """
        It is the constructor to my version of the tweet object.

        Parameters:
        - ogTweet: The tweet object.
        """

        # Get tweet data
        self.__getTweetData(ogTweet)

        # Get user information
        self.__getUserData(ogTweet)

        # Get if it is a retweet or not
        self.__getRetweet(ogTweet)

        # Get all the data from the entities
        self.__getFromEntities(ogTweet)

        # Get the place data
        self.__getFromPlace(ogTweet)

    def __getTweetData(self, ogTweet):
        """
        Private function to get data about the tweet object.

        Parameters:
        - ogTweet: The tweet object.
        """

        self.tw_id_str = ogTweet['id_str']
        self.tw_created_at = ogTweet['created_at']
        self.tw_coordinates = ogTweet['coordinates']
        self.tw_is_quote_status = ogTweet['is_quote_status']
        self.tw_in_reply_to_user_id_str = ogTweet['in_reply_to_user_id_str']
        self.tw_in_reply_to_status_id_str = ogTweet['in_reply_to_status_id_str']

        # If the text has more than 140 chars, the full text is inside
        # the extended_tweet object.
        if hasattr(ogTweet, 'extended_tweet'):
            self.tw_text = ogTweet['extended_tweet']['full_text']
        else:
            self.tw_text = ogTweet['text']

    def __getRetweet(self, ogTweet):
        """
        Private function to get if the received tweet is a retweet or not.

        Parameters:
        - ogTweet: The tweet object.
        """

        if 'retweeted_status' in ogTweet:
            self.rt_isRetweet = True
            self.rt_OgTweetID = ogTweet['retweeted_status']['id_str']
            self.rt_OgRetwCount = ogTweet['retweeted_status']['retweet_count']
            self.rt_OgFavCount = ogTweet['retweeted_status']['favorite_count']
        else:
            self.rt_isRetweet = False
            self.rt_OgTweetID = ""
            self.rt_OgRetwCount = 0
            self.rt_OgFavCount = 0

    def __getUserData(self, ogTweet):
        """
        Private function to get information from the tweet's author

        Parameters:
        - ogTweet: The tweet object.
        """
        # User information
        self.usr_name = ogTweet['user']['name']
        self.usr_id_str = ogTweet['user']['id_str']
        self.usr_verified = ogTweet['user']['verified']
        self.usr_location = ogTweet['user']['location']
        self.usr_screenname = ogTweet['user']['screen_name']
        self.usr_listedcount = ogTweet['user']['listed_count']
        self.usr_friendscount = ogTweet['user']['friends_count']
        self.usr_statusescount = ogTweet['user']['statuses_count']
        self.usr_followerscount = ogTweet['user']['followers_count']
        self.usr_favouritescount = ogTweet['user']['favourites_count']

    def __getFromEntities(self, ogTweet):
        """
        Private function to get the list of the hashtags, media files or urls
        that are used on the tweet

        Parameters:
        - ogTweet: The tweet object.
        """
        self.ent_urls = ""
        self.ent_media = ""
        self.ent_hashtags = ""

        if hasattr(ogTweet['entities'], 'media'):
            for media in ogTweet['entities']['media']:
                self.ent_media += media['expanded_url'] + " | "

        for hasht in ogTweet['entities']['hashtags']:
            self.ent_hashtags += hasht['text'] + " | "

        for url in ogTweet['entities']['urls']:
            self.ent_urls += url['url'] + " | "

        self.ent_urls = self.ent_urls[:-3]
        self.ent_media = self.ent_media[:-3]
        self.ent_hashtags = self.ent_hashtags[:-3]

    def __getFromPlace(self, ogTweet):
        """
            Private function that checks if the tweet has information
            about the place the tweet was made from.

            Parameters:
                - ogTweet: The tweet object.
        """

        # Check if the place object exists or not and save it if so
        if hasattr(ogTweet, 'place'):
            self.geo_name = ogTweet['name']
            self.geo_country = ogTweet['country']
            self.geo_full_name = ogTweet['full_name']
            self.geo_place_type = ogTweet['place_type']
            self.geo_country_code = ogTweet['country_code']
            self.geo_bounding_box = ogTweet['bounding_box']

        else:
            self.geo_name = ""
            self.geo_country = ""
            self.geo_full_name = ""
            self.geo_place_type = ""
            self.geo_country_code = ""
            self.geo_bounding_box = {}

    def serialize(self):
        """
        It returns the object as a dictionary
        """
        return self.__dict__
