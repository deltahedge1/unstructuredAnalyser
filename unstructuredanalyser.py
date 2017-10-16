# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 21:55:44 2017

@author: ihassan1
"""
import re
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from stemming.porter2 import stem

stop_words = set(stopwords.words("english"))
#checkwords = open('C:/Users/ihassan1/AAA/ANZ Breech Local/searchwords.txt').read().splitlines()


class unstructuredAnalyser(object):
    
    #added checkwords as an input so that we can shoose the source
    def __init__(self, checkwords = []):
        self.checkwords = checkwords
        self.checkwords = self._checkwords2()
    #use this to remove stopwords and get all the meaningful words
    
    #this is to get stemmed words and words
    def _checkwords2(self):
        checkwords_temp = [word.lower().strip() for word in self.checkwords] #change all the words to lowercase and strip any trailing spaces
        checkwords2 = [(word,stem(word)) for word in checkwords_temp] #get a tuple of stemmed words and words
        return checkwords2   
    
    def remove_stopwords(self, text):
        try:
            str(text)
            w = ""
            for sent in sent_tokenize(text):
                for word in word_tokenize(sent):
                    if word.lower() not in stop_words:
                        w = w + " " + word            
            return w
        except:
            return ""
        
    def return_countwords(self, text):
        try:
            text = str(stem(text))
            
            #get a unique list of words that we can check from
            unique_words =[]
            for word in self.checkwords:
                unique_words.append(word[1])
            
            unique_words = set(unique_words)
            
            #use the unique list to get the count based on stemming but only counting unique words
            w=0
            for sent in sent_tokenize(text):
                for word in unique_words:
                    rePattern = re.compile(r"\b(%s)\b" %str(word))
                    if bool(rePattern.search(sent)) == True:
                        w +=1
            return w
        except:
            return ""

    #return matched words updated for phrases
    def return_matchedwords(self, text):
        try:
            text = str(stem(text))
            w=""
            
            for sent in sent_tokenize(text):
                #stem a sentence then join back together
                sentList = []
                wordtokenize = word_tokenize(sent)
                
                for word_to_stem in wordtokenize:
                    word_lower = word_to_stem.lower() #lower case
                    sentList.append(stem(word_lower)) #stem and add to a list
                    
                stemmedSentence = str(" ".join(sentList)) #join back toegther for regexing       
            
                for word in self.checkwords:
                        rePattern = re.compile(r"\b(%s)\b" %str(word[1]))
                        if bool(rePattern.search(stemmedSentence.lower().strip())) == True:
                            w = w + "|" + word[0]
                            
            return w + "|"
        except:
            return ""

    #return matched sentences
    def return_matchedsentences(self, text):
        try:
            text = str(text)
            w=""
            
            for sent in sent_tokenize(text):
                i = 0  #this is to make sure if there are multiple words we are looking for in the same sentence dont pull that sentence out multiple times
                
                #stem a sentence then join back together
                sentList = []
                for word_to_stem in word_tokenize(sent):
                    word_lower = word_to_stem.lower() #lower case
                    sentList.append(stem(word_lower)) #stem and add to a list
                
                stemmedSentence = str(" ".join(sentList)) #join back toegther for regexing
                
                for word in self.checkwords:
                    rePattern = re.compile(r"\b(%s)\b" %str(word[1]))
                    if bool(rePattern.search(stemmedSentence)) == True and i !=1:
                        w = w + "|" + sent   
                        i = 1 #flag to change if one word is found
            return w + "|"
        except:
            return ""
        
        
