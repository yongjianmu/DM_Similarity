import fileinput
import os
import json 
import numpy as np
import gensim
from nltk.corpus import stopwords
from pprint import pprint
import nltk.corpus as nc
import nltk
from nltk.tag import pos_tag, map_tag

fileDir = os.path.dirname(os.path.realpath('__file__'))
flist = []
flist1 = ["scrapy/nytimes/2016-04-08.json","scrapy/nytimes/2016-04-09.json","scrapy/nytimes/2016-04-10.json"]
flist2 = ["scrapy/timecom/2016-04-08.json","scrapy/timecom/2016-04-09.json","scrapy/timecom/2016-04-10.json"]
flist3 = ["scrapy/google/2016-04-08.json","scrapy/google/2016-04-09.json","scrapy/google/2016-04-10.json"]
flist = flist1+flist2+flist3

#stop_words
stop_words = stopwords.words('english')

#perpare data
#input: one file name
#return: list of string formate titles
def dataprep(filex):
    filename = json.load(open(filex))
    dictfile={'date':'','news':''} 
    for i in range(len(filename)):
        valuelist=[]
        for x,y in filename.iteritems():
            if (x == "date"):
                dictfile["date"] = y.encode('utf-8')
            elif x=="sectionnews":
                for data in y:
                    data = data.lower()
                    valuelist.append(str(data.encode('utf-8').strip().replace('/',' ').replace("'",' ').replace('"',' ').replace(".",' ').replace(",",' ').replace(":"," ").replace("?"," ")))
            else: 
                for data in y:
                    data = data.lower()
                    valuelist.append(str(data.encode('utf-8').strip().replace('/',' ').replace("'",' ').replace('"',' ').replace(".",' ').replace(",",' ').replace(":"," ").replace("?"," ")))
    return valuelist
#example
#dataprep(flist1[0])

#delete stop words
#input listx = dataprep(filename)
#return list = [['adsa','bfdd'],['fsd'],['fds','fd','fd']...]
def titles_no_stopwords(listx):
    title_list = []
    for i in range(len(listx)):
        titles = [] 
        for words in listx[i].split(" "):
            if words not in stop_words:
                if len(words) > 1:
                    titles.append(words) 
        title_list.append(titles)
    return title_list

#change the formate of list of single word list
#input list = [['adsa','bfdd'],['fsd'],['fds','fd','fd']...]
#return list = ['I like you','you likes money','money is a racket'...]
def titles_string(listx):
    title_l = []
    for i in range(len(listx)):
        title_l.append(" ".join(listx[i]))
    return title_l

#extract all noun word in a title
#input: a news list
#return: a tagged dict = {"title1":["noun_key_word","noun_key_word",...], "title2":[...],...}
def noun_verb(one_day_news_list):
    dict_sentence_noun_verb = dict()
    string = titles_string(titles_no_stopwords(dataprep(one_day_news_list)))    
    for i in range(len(dataprep(one_day_news_list))):
        list_sentence_noun_verb = []        
        text = nltk.word_tokenize(string[i])
        posTagged = pos_tag(text)
        simplifiedTags = [(word, map_tag('en-brown', 'universal', tag)) for word, tag in posTagged]
        for (w,t) in simplifiedTags:
            if t.startswith('N'):
                list_sentence_noun_verb.append(w)
            elif t.startswith('V'):
                list_sentence_noun_verb.append(w)                
        dict_sentence_noun_verb[i] = list_sentence_noun_verb
    return dict_sentence_noun_verb
#example
#dict_noun_1 = noun_verb(flist1[2])


#titles just skip stopwords
def general(one_day_news_list):
    dict_sentence_general = dict()
    string = titles_no_stopwords(dataprep(one_day_news_list))
    for i in range(len(dataprep(one_day_news_list))):
        dict_sentence_general[i] = string[i]
    return(dict_sentence_general)
#example
#general(flist1[0])
#noun_verb(flist1[0])

#result of key word extraction!
def print_noun_verb_extract(filename):
    before = dataprep(filename)
    after = noun_verb(filename)
    for i in range(len(before)):
        print(i+1)
        print(before[i])
        if i < len(after):
            print(after[i])
#example        
#print_noun_verb_extract(flist1[2])


#file1 is smaller
def intersection_ratio(file1,file2):
    
    if(len(dataprep(file1))>len(dataprep(file2))):
        x = file2
        file2 = file1
        file1 = x
    
    #only noun and verb count    
    f1 = noun_verb(file1)
    f2 = noun_verb(file2)
    
    #all words without stopword count
    #f1 = general(file1)
    #f2 = general(file2)    
    #0.285714285714
    #0.393939393939
    #0.242424242424
        
    
    #number of k means how many nouns are appear at the same time in both 
    #by change the value of k's range, similarity ratio will also changes.
    #eg: k>0 means once a noun appears, those two title are samilar.
    similar_title = []
    for key1, value1 in f1.items():
        for key2, value2 in f2.items():
            k = 0
            for word in value1:
                if word in value2:
                    k = k + 1
            if k > 1: 
                #print((key1,value1),(key2,value2))
                similar_title.append([key1,key2])   
    
    #detailed similar title content
    '''
    o1 = dataprep(file1)
    o2 = dataprep(file2)
    print("---------similar news----------")
    for i in range(len(similar_title)):
        x = similar_title[i][0]
        y = similar_title[i][1]  
        print("-------------")
        print(x,o1[x])
        print(y,o2[y])
    '''
    l1 = [] 
    for [i,j] in similar_title:
        l1.append(i)
#    print(set(l1))
    similar_title_count = len(set(l1))
    total_count = len(f1)
    print(similar_title_count * total_count**(-1))    

    
def main():

    nyt_words = flist1[2]
    time_words = flist2[2]
    google_words = flist3[2]
    
    intersection_ratio(nyt_words,google_words)
    intersection_ratio(time_words, google_words)
    intersection_ratio(nyt_words, time_words)
    
    
    
if __name__ == "__main__":
    main()
