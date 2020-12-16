import tweepy 
import generate_tweets as gt

mode='print'  #has to be 'tweet' or 'print'

if mode=='tweet':
	consumer_key = 'dJ30fM3EKMumCePiyJNJ3e7ob' 
	consumer_secret = 'u5XNXRxduS3WHD2JzZIgyvDxsevYD6818CMdMEc5Z0v3reQqun' 
	access_token = '1338787696412651522-IW0b60Itfgyk7T52lkGvmdDOqT4sMQ' 
	access_token_secret = 'Z72CYDo9EfuzEojnanTDDHeURb6VQ3poBjoo7rSwK15Mb' 

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)

	api.update_status(gt.get_tweet())

if mode=='print':
	print(gt.get_tweet())
