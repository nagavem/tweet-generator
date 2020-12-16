import pandas as pd
import snscrape.modules
import myinputs

handle=myinputs.handle
tweets=snscrape.modules.twitter.TwitterUserScraper(handle + ' since:2010-03-01 lang:en')

df_tweets = pd.DataFrame(columns=['tweet'])

for tweet in tweets.get_items():	
	dict_row={'tweet': tweet.content}
	df_tweets = df_tweets.append(dict_row,ignore_index=True)


df_tweets.to_excel(handle + '.xlsx')

