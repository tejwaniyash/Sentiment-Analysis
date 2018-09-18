

import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np
import re
import nltk
from bs4 import BeautifulSoup
from nltk.corpus import stopwords

class KaggleWord2VecUtility(object):
    """KaggleWord2VecUtility is a utility class for processing raw HTML text into segments for further learning"""

    @staticmethod
    def review_to_wordlist( review, remove_stopwords=False ):
        
        review_text = BeautifulSoup(review, "lxml").get_text()
        
        review_text = re.sub("[^a-zA-Z]"," ", review_text)
       
        words = review_text.lower().split()
      
        if remove_stopwords:
            stops = set(stopwords.words("english"))
            words = [w for w in words if not w in stops]
      
        return(words)

   
    @staticmethod
    def review_to_sentences( review, tokenizer, remove_stopwords=False ):
       
        raw_sentences = tokenizer.tokenize(review.decode('utf8').strip())
        
        sentences = []
        for raw_sentence in raw_sentences:
           
            if len(raw_sentence) > 0:
                
                sentences.append( KaggleWord2VecUtility.review_to_wordlist( raw_sentence, \
                  remove_stopwords ))
       
        return sentences

if __name__ == '__main__':
    train = pd.read_csv("J:/DeepLearningMovies-master/DeepLearningMovies-master/labeledTrainData.tsv", header=0, \
                    delimiter="\t", quoting=3)
    test = pd.read_csv( "J:/DeepLearningMovies-master/DeepLearningMovies-master/testData.tsv", header=0, delimiter="\t", \
                   quoting=3 )

    print ('The first review is:')
    print (train["review"][0])
   #input("Press Enter to continue...")


    print ('Download text data sets. If you already have NLTK datasets downloaded, just close the Python download window...')
    nltk.download('stopwords')

   
    clean_train_reviews = []
    clean_test_reviews = []
    
    print ("Cleaning and parsing the training set movie reviews...\n")
    for i in range( 0, len(train["review"])):
        if( i < len(train['review'])):
            clean_train_reviews.append(" ".join(KaggleWord2VecUtility.review_to_wordlist(train["review"][i], True)))
        else:
            clean_test_reviews.append(" ".join(KaggleWord2VecUtility.review_to_wordlist(train["review"][i], True)))
            
    print (clean_train_reviews[0])
    

    print ("Creating the bag of words...\n")


    vectorizer = CountVectorizer(analyzer = "word",   \
                             tokenizer = None,    \
                             preprocessor = None, \
                             stop_words = None,   \
                             max_features = 5000)

   
    train_data_features = vectorizer.fit_transform(clean_train_reviews)

    np.asarray(train_data_features)
    print ("Training the random forest (this may take a while)...")
    forest = RandomForestClassifier(n_estimators = 100) 
    forest = forest.fit( train_data_features, train["sentiment"] )
    clean_test_reviews = []

    print ("Cleaning and parsing the test set movie reviews...\n")
    for i in range(0,len(test["review"])):
        clean_test_reviews.append(" ".join(KaggleWord2VecUtility.review_to_wordlist(test["review"][i], True)))
    test_data_features = vectorizer.transform(clean_test_reviews)
    np.asarray(test_data_features)

    
    print ("Predicting test labels...\n")
    result = forest.predict(test_data_features)

    
    output = pd.DataFrame( data={"id":test["id"], "sentiment":result} )

    
    output.to_csv(os.path.join(os.path.dirname(__file__), 'data', 'Bag_of_Words_model.csv'), index=False, quoting=3)
    print ("Wrote results to Bag_of_Words_model.csv")


