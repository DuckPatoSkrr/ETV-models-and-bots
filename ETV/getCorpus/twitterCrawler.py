# original code from https://gist.github.com/vickyqian/f70e9ab3910c7c290d9d715491cde44c

import tweepy
import csv

# input your credentials here
consumer_key = 'GgMseCkn6T7Kw6JmKrxu2XPY5'
consumer_secret = 'MKgBQXM7mOngz0RL0K32N3yJorDuDky86jbHOTxPFpbSgCskOr'
access_token = '1425539622-VnOGh5OJHxQJNN3cz9Rv7ktPNMgyDdJlbLb3RWH'
access_token_secret = 'kEDXDuBeKOUAhwis6y6n3s2RooFgdxHQCBmoP7lBRYVAf'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

# Open/Create a file to append data
corpus_file = open('sports.txt', 'a', encoding="utf-8")

print("Opened file")
i = 0
queue = "referee"

for tweet in tweepy.Cursor(api.search, q=queue, count=100, lang="en", since="2021-01-01").items():
    print(f"Adding tweet {i}")
    # to separate tweets, we make sure they all end in a dot
    final_tweet = tweet.text
    if not final_tweet.endswith('.'):
        final_tweet = final_tweet + '.'
    corpus_file.write(final_tweet)
    i = i + 1
    if i >= 5000:
        break

print("Closing file with words from " + queue)
corpus_file.close()
print("Done")
