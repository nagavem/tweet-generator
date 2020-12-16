import gpt_2_simple as gpt2
import random

def get_tweet():

	sess = gpt2.start_tf_sess()
	gpt2.load_gpt2(sess)

	tweet = gpt2.generate(sess,
              		  length=40,
              		  temperature=1,
              		  truncate='<!.>',
              		  nsamples=1,
              		  batch_size=1,
              		  return_as_list=True
              		  )[0]
	tweet=str(tweet)
	tweet.replace('&amp;','&')
	min_length = random.randint(20,100)
	if len(tweet)-1<=min_length:
		min_length=0
	terminate=0
	for index,char in enumerate(tweet):
		if char in ['.','!','?']:
			terminate=index+1
			break
	if terminate==0:
		terminate=len(tweet)
	tweet=tweet[:terminate]	
	return tweet


