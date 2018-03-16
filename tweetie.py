#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 01:35:33 2017

@author: nimesh
"""

import sys
import tweepy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def loadkeys(filename):
    """"
    load twitter api keys/tokens from CSV file with form
    consumer_key, consumer_secret, access_token, access_token_secret
    """
    with open(filename) as f:
        items = f.readline().strip().split(', ')
        return items

def authenticate(filename):
    """
    Given a file name containing the Twitter keys and tokens,
    create and return a tweepy API object.
    """
    keys = loadkeys(filename)
    auth = tweepy.OAuthHandler(keys[0], keys[1])
    auth.set_access_token(keys[2], keys[3])
    api = tweepy.API(auth)    
    return api
    

 
    
def fetch_tweets(api, name):
    """
    Given a tweepy API object and the screen name of the Twitter user,
    create a list of tweets where each tweet is a dictionary with the
    following keys:
       id: tweet ID
       created: tweet creation date
       retweeted: number of retweets
       text: text of the tweet
       hashtags: list of hashtags mentioned in the tweet
       urls: list of URLs mentioned in the tweet
       mentions: list of screen names mentioned in the tweet
       score: the "compound" polarity score from vader's polarity_scores()
    Return a dictionary containing keys-value pairs:
       user: user's screen name
       count: number of tweets
       tweets: list of tweets, each tweet is a dictionary
    For efficiency, create a single Vader SentimentIntensityAnalyzer()
    per call to this function, not per tweet.
    """
    new_tweets = api.user_timeline(screen_name = name,count=200)
    sa = SentimentIntensityAnalyzer()
    tweet_list = []
    for tweet in new_tweets:
        tweet_dict = {
                'id': tweet.id,
                'created': tweet.created_at,
                'retweeted': tweet.retweet_count,
                'text': tweet.text,
                'hashtags': tweet.entities.get('hashtags'),
                'urls': tweet.entities['urls'],
                'mentions': [t['screen_name'] for t in tweet.entities['user_mentions']],
                'score': sa.polarity_scores(tweet.text)['compound']
                }
        tweet_list.append(tweet_dict)
    return {'user': name, 'count': api.get_user(name).statuses_count, 'tweets': tweet_list}

def fetch_following(api,name):
    """
    Given a tweepy API object and the screen name of the Twitter user,
    return a a list of dictionaries containing the followed user info
    with keys-value pairs:
       name: real name
       screen_name: Twitter screen name
       followers: number of followers
       created: created date (no time info)
       image: the URL of the profile's image
    To collect data: get a list of "friends IDs" then get
    the list of users for each of those.
    """
    def get_friends(name):
        users = []
        page_count = 0
        for user in tweepy.Cursor(api.friends, name, count=100).pages():
            page_count += 1
            users.extend(user)
        return users
    p = get_friends(name)
    
    users=[]
    for user in p:
        d = {'name':user.name,
             'screen_name':user.screen_name,
             'followers': user.followers_count,
             'created':user.created_at.date(),
             'image':user.profile_image_url_https
                }
        users.append(d)
    return sorted(users, key=lambda x: -x['followers'])
        
        
        
        
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    