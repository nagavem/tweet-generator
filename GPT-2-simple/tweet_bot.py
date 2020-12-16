import tweepy 
import generate_tweets as gt

mode='print'  #has to be 'tweet' or 'print'

if mode=='tweet':
	consumer_key = '' 
	consumer_secret = '' 
	access_token = '' 
	access_token_secret = '' 

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)

	api.update_status(gt.get_tweet())

if mode=='print':
	print(gt.get_tweet())
