import tweepy
import os
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import requests

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

driver = webdriver.Chrome(ChromeDriverManager().install())

print('this is my twitter bot')
FILE_NAME = 'last_seen_id.txt'

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = (f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

def reply_to_tweets():
    print("...retreiving")
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    mentions = api.mentions_timeline(last_seen_id)
    content = driver.page_source
    soup = BeautifulSoup(content)
    url = "https://www.worldometers.info/coronavirus/"
    r = requests.get(url)
    data= r.text
    soup = BeautifulSoup(data, 'html.parser')
    span = soup.find('div',attrs={'class':'maincounter-number'})
    cases = span.span.text
    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.text)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)
        if '@' in mention.text.lower():
            print('found @updates_covid')
            print('responding back...')
            api.update_status('@' + mention.user.screen_name + ' ' +
                    'Currently there are '+ cases +'confirmed Covid-19 cases.'+ "#coronavirus", mention.id)

def tweet_reply():
    print('working')
    twts = api.search(q="#coronavirus")
    url = "https://www.worldometers.info/coronavirus/"
    r = requests.get(url)
    data= r.text
    soup = BeautifulSoup(data, 'html.parser')
    span = soup.find('div',attrs={'class':'maincounter-number'})
    cases = span.span.text
    while True:
        for s in twts:
            sn = s.user.screen_name
            m = str('@' + s.user.screen_name + ' ' +
                'Currently there are '+ cases +'confirmed Covid-19 cases.')
            api.update_status(m, s.id)

