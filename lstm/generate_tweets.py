import pandas as pd
import myinputs
import re
import tensorflow as tf
import numpy as np 
import matplotlib.pyplot as plt
import os

from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Embedding, LSTM, Dense, Bidirectional
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam


def clean(val):
	val = str(val)
	val = re.sub(r"http\S+", "", val) 
	val = re.sub(r'pic.twitter.com/[\w]*',"", val)
	val = re.sub('[^a-zA-Z0-9\n\s\.?!-]', '', val)
	return val

handle=myinputs.handle
df_tweets = pd.read_excel(handle + '.xlsx')
df_tweets.drop(df_tweets.columns[0], axis=1,inplace=True)

df_tweets.drop_duplicates(keep='first', inplace=True)
df_tweets['clean_tweet'] = df_tweets['tweet'].apply(clean)
df_tweets.drop('tweet', axis=1, inplace=True)

tweets = df_tweets['clean_tweet'].str.lower().tolist()

tokenizer= Tokenizer()
tokenizer.fit_on_texts(tweets)
total_words = len(tokenizer.word_index)+1

input_sequences = []
for tweet in tweets:
	token_list = tokenizer.texts_to_sequences([tweet])[0]
	for i in range(1, len(token_list)):
		n_gram_sequence = token_list[:i+1]
		input_sequences.append(n_gram_sequence)

# pad sequences 
max_sequence_len = max([len(x) for x in input_sequences])
input_sequences = np.array(pad_sequences(input_sequences, maxlen=max_sequence_len, padding='pre'))

# create predictors and label
xs, labels = input_sequences[:,:-1],input_sequences[:,-1]

ys = tf.keras.utils.to_categorical(labels, num_classes=total_words)

dirname = os.getcwd()
checkpoint_path = os.path.join(dirname, 'cp.ckpt')

cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                 save_weights_only=True,
                                                 verbose=1)


model = Sequential()
model.add(Embedding(total_words, 100, input_length=max_sequence_len-1))
model.add(Bidirectional(LSTM(25)))
model.add(Dense(total_words, activation='softmax'))

adam = Adam(lr=0.00001)
model.compile(loss='categorical_crossentropy', optimizer=adam, metrics=['accuracy'])

if myinputs.mode=='train':
	history = model.fit(xs, ys, epochs=50, callbacks=[cp_callback],verbose=1)
	print model.summary()
	print(model)

	plt.plot(history.history['accuracy'])
	plt.xlabel("Epochs")
	plt.ylabel('accuracy')
	plt.show()


if myinputs.mode='generate':
	model.load_weights(checkpoint_path) 
	seed_text = myinputs.seed_text
	next_words = myinputs.next_words

	 
	for _ in range(next_words):
		token_list = tokenizer.texts_to_sequences([seed_text])[0]
		token_list = pad_sequences([token_list], maxlen=max_sequence_len-1, padding='pre')
		predicted = model.predict_classes(token_list, verbose=0)
		output_word = ""
		for word, index in tokenizer.word_index.items():
			if index == predicted:
				output_word = word
				break
		seed_text += " " + output_word
	print(seed_text)

