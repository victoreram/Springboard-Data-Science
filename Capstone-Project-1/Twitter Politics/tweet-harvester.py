# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 14:41:23 2018

@author: ramir
"""

import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
 
consumer_key = 'jJumdM6YPcuW4FzW39YlSRdHy'
consumer_secret = 'vy6g4vV9ODZE1yaG1W8ZcMXi0PJaUhf7A7wu2oPTwEmaBcfkce'
access_token = '963856913527123968-WbLSqivAKCZHDIFuQ5OL1ObRsLkjq4y'
access_secret = 'm6rev0hu4h0nwX1pxlpvhyyUo1AqcQ1ph67UXLrqGaZ0i'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)
#search = api.search(q='trump')
#search.

class MyListener(StreamListener):
 
    def on_data(self, data):
        try:
            with open('btc.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True
 
    def on_error(self, status):
        print(status)
        return True
        
    def on_status(self, status):
#        description = status.user.description
#        loc = status.user.location
#        text = status.text
#        coords = status.coordinates
#        name = status.user.screen_name
#        user_created = status.user.created_at
#        followers = status.user.followers_count
#        id_str = status.id_str
#        created = status.created_at
#        retweets = status.retweet_count
#        bg_color = status.user.profile_background_color
#        table = db["tweets"]
#        table.insert(dict(
#            user_description=description,
#            user_location=loc,
#            coordinates=coords,
#            text=text,
#            user_name=name,
#            user_created=user_created,
#            user_followers=followers,
#            id_str=id_str,
#            created=created,
#            retweet_count=retweets,
#            user_bg_color=bg_color,
#            polarity=sent.polarity,
#            subjectivity=sent.subjectivity,
#        ))
        if status.retweeted_status:
            return
        print(status.text)
 
twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['#bitcoin'])
#stream_listener = StreamListener()