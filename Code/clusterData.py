import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np

def readDataset(filename):
	df = pd.read_csv(filename, index_col=None, encoding='ISO-8859-1', header=0)
	return df

def setVectorizer(data):
    vectorizer = TfidfVectorizer(stop_words = 'english', binary=True, min_df=0.04, strip_accents='unicode', 
                             lowercase=True, sublinear_tf=True)
    vectorizer.fit(data)

    return vectorizer

def setVectorizerForVisualization(data):
    vectorizer = TfidfVectorizer(stop_words = 'english', binary=True, min_df=0.01, strip_accents='unicode', 
                             lowercase=True, sublinear_tf=True)
    vectorizer.fit(data)

    return vectorizer

def clusterWithKmeans(data):
	
	kMeansClustering = KMeans(n_clusters=7, init='k-means++', n_init=30, max_iter=250, random_state=42).fit(data) 
	return kMeansClustering 

# Online clustering
def jacc_similarity(vector1, vector2):
    jacc_num = 0
    jacc_den = len(vector1)
    for index in vector1:
        if index in vector2:
            jacc_num += 1
            jacc_den -= 1
    jacc_den += len(vector2)
    return jacc_num / jacc_den

def onlineClusterJaccardAlgorithm(tweets):
    JaccGroup = []
    JackTweet = []
    JackCluster = []
    
    centroids = np.zeros(shape=(1,tweets[0].shape[1]))
    NTweets = np.zeros(shape=(1,1))
    
    #Assign first tweet as a new cluster
    centroids = np.vstack((centroids, tweets[0]))
    centroids = np.delete(centroids, 0, 0)
    
    NTweets = np.vstack((NTweets, 1))
    NTweets = np.delete(NTweets, 0, 0)
    for tweet in tweets:
      count = -1
      maxIndex = -1
      similarity =-1
      for centroid in centroids:
        wordsCentroid = np.where(centroid != 0)[1]
        wordsTweet = np.where(tweet != 0)[1]
        count+=1
        if(len(wordsCentroid)!=0):
          value = jacc_similarity(wordsTweet, wordsCentroid)
          if(value > similarity):
            similarity = value
            maxIndex = count
      
      if(similarity>0.2):
        centroids[maxIndex] = (tweet + centroids[maxIndex]) / 2.0
        NTweets[maxIndex] = NTweets[maxIndex] + 1
        JaccGroup.append(maxIndex)
        JackCluster.append(maxIndex)
        JackTweet.append(tweet)
      else:
        if(np.count_nonzero(tweet)>0):
          centroids = np.vstack((centroids, tweet))
          NTweets = np.vstack((NTweets, 1))
          JaccGroup.append(centroids.shape[1])
          JackCluster.append(maxIndex)
          JackTweet.append(tweet)
        else:
          JaccGroup.append(-1)
      #print("Similarity: ",similarity)
      #print("Centroid: ",maxIndex)
    print("# centroids jaccard: ", centroids.shape)
    return centroids, NTweets, JaccGroup

df = readDataset('./preprocessed.csv')

vectorizer = setVectorizer(df['preProcessed'].values.astype('U'))
vectorizedData = vectorizer.transform(df['preProcessed'].values.astype('U'))

vectorizerVis = setVectorizerForVisualization(df['preProcessed'].values.astype('U'))
vectorizerVisData = vectorizerVis.transform(df['preProcessed'].values.astype('U'))

#Normal clustering
cluster = clusterWithKmeans(vectorizedData)
df['clusterd'] = cluster.labels_
centroids  = cluster.cluster_centers_
wordsCluster = []

for label in cluster.labels_:
    out = ''
    centroid  = centroids[label]
    for word in np.where(centroid > 0)[0]:
          out = out + vectorizer.get_feature_names()[word]+" "
    out = out[:-1]
    wordsCluster.append(out)

wordsTweet = []
for tweet in df['preProcessed'].values.astype('U'):
    out = ''
    for word in tweet.split():
        if(word in vectorizer.get_feature_names()):
            out = out + word + " "
    out = out[:-1]
    wordsTweet.append(out)

df['centroid'] = wordsCluster
df['important'] = wordsTweet


# Online clustering
JaccCentroides, JaccNTweets, JackLabels = onlineClusterJaccardAlgorithm(vectorizedData.todense())
df['Jackcluster'] = JackLabels

df.to_csv('clustered.csv', index=False)