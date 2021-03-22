import os
import pandas as pd
import glob
import nltk

from nltk.tokenize import TweetTokenizer
from nltk.stem import PorterStemmer
from nltk.stem import SnowballStemmer
from nltk.stem import WordNetLemmatizer 
from nltk.corpus import stopwords 

import re
import string

nltk.download('stopwords')
nltk.download('wordnet')

#Global variables

lemmatizer = WordNetLemmatizer() 

tknzr = TweetTokenizer(preserve_case=False, reduce_len=True, strip_handles=True)

#stemmer = PorterStemmer()
stemmer = SnowballStemmer("english") #snowball is faster, improvement of Porter stemmer

stop_words_en = set(stopwords.words('english')) 
stop_words_es = set(stopwords.words('spanish')) 
#excluded = set(string.punctuation.replace('#','').replace('@',''))

def readDataset(filename):
  df = pd.read_csv(filename)
  return df

def stopWordsTextEnglish(word_tokens):
  words_filtered_en = [w for w in word_tokens if not w in stop_words_en]
  return words_filtered_en
  
def stopWordsTextSpanish(word_tokens):
  words_filtered_es = [w for w in word_tokens if not w in stop_words_es]
  return words_filtered_es

def tokenizeTweet(text):
  out_ = ''

  #No url
  text = re.sub(r"http\S+", "", text)
  
  #Remove numbers from tweet
  text = re.sub(r'\d+', '', text)

  #Replace # with empty
  text = text.replace(' # ','')

  #Remove symbols from tweet
  text = re.sub(r'\W', ' ', text)
  #text = "".join([char.lower() for char in text if char not in excluded]) 
  
  # remove all single characters
  text = re.sub(r'\s+[a-zA-Z]\s+', ' ', text)

  # Remove single characters from the start
  text = re.sub(r'\^[a-zA-Z]\s+', ' ', text) 

  #No double space
  text = re.sub('\s+', ' ', text).strip()

  #Remove short words
  text = re.sub(r'\b\w{1,3}\b', '', text)

  terms = tknzr.tokenize(text)

  words_filtered_en = stopWordsTextEnglish(terms)
  
  for token in words_filtered_en:
      out_ += lemmatizer.lemmatize(token.lower()) + " "
      #out_ += stemmer.stem(token.lower()) + " "
  return out_

def preprocessText(data):
  tweets_preprocessed = []
	
  for tweet in data.iloc[:, 1]:
    tweets_preprocessed.append(tokenizeTweet(tweet))
  
  return tweets_preprocessed

df = readDataset('./dataframe.csv')

df['preProcessed'] = preprocessText(df)
df.to_csv('preprocessed.csv', index=False)


