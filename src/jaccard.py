import fileinput
import os
import json
import numpy as np


fileDir = os.path.dirname(os.path.realpath('__file__'))
#flist1 = ["scrapy/nytimes/2016-02-29.json","scrapy/timecom/2016-02-29.json","scrapy/nytimes/2016-03-02.json","scrapy/timecom/2016-03-02.json","scrapy/nytimes/2016-03-03.json","scrapy/timecom/2016-03-03.json","scrapy/nytimes/2016-03-04.json","scrapy/timecom/2016-03-04.json","scrapy/nytimes/2016-03-05.json","scrapy/timecom/2016-03-05.json","scrapy/nytimes/2016-03-06.json","scrapy/timecom/2016-03-06.json","scrapy/nytimes/2016-03-07.json","scrapy/timecom/2016-03-07.json","scrapy/nytimes/2016-03-08.json","scrapy/timecom/2016-03-08.json","scrapy/nytimes/2016-03-12.json","scrapy/timecom/2016-03-12.json","scrapy/nytimes/2016-03-13.json","scrapy/timecom/2016-03-13.json"]

def getFileList(p, q):
    p = str(p + q)
    if p == "":
        return [ ]
    if p[-1] != "/":
        p = p + "/"
    a = os.listdir(p)
    b = [q + x for x in a if os.path.splitext(p + x)[1] == ".json"]
    return b

flist1 = getFileList(fileDir + "/", "scrapy/nytimes/")
flist2 = getFileList(os.getcwd() + "/", "scrapy/timecom/")
flist1 += flist2
flist = []

for i in range(len(flist1)):
    flist.append(os.path.join(fileDir,flist1[i]))

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
                    valuelist.append(data.encode('utf-8').strip().replace('/',' ').replace("'",' ').replace(".",' ').replace(",",' ').replace(":"," ").replace("?"," "))
            else:
                for data in y:
                    data = data.lower()
                    valuelist.append(data.encode('utf-8').strip().replace('/',' ').replace("'",' ').replace(".",' ').replace(",",' ').replace(":"," ").replace("?"," "))
        dictfile['news']=" ".join(valuelist)
    return dictfile

#delete those unmeaningful words which length is < 3
#input: dict["news"]
#return a list
def newslist(listx):
    newlist=[]
    listx=listx.split(" ")
    for x in listx:
        if(len(x) > 2):
            newlist.append(x)
    return newlist

#print(dataprep(flist[0]))

def characters(listx):
    return("".join(listx))


def words(listx):
    return(listx)

def kgram(k,filex):
    lst=[]
    for i in range(len(filex)-k+1):
        if(filex[i:i+k] not in lst):
            lst.append(filex[i:i+k])
    return lst

def num_kgram(k,filex):
    w = len(kgram(k,words(filex)))
    c = len(kgram(k,characters(filex)))
    if(k==2):
        print("# of {0}-gram words:      {1}".format(k,w))
        print("# of {0}-gram characters: {1}".format(k,c))
    if(k==3):
        print("# of {0}-gram characters: {1}".format(k,c))


def printnumber(filenamelist):
    for f in flist:
        fname = os.path.basename(f)
        print('-------{0}-------'.format(fname))
        num_kgram(2,newslist(dataprep(f)["news"]))


def k1set(lists):
    lst = []
    for x in lists:
        lst.append(x)
    return set(lst)

def k2set(lists):
    lst = []
    for [i,j] in lists:
        lst.append(i+j)
    return set(lst)

def k3set(lists):
    lst = []
    for [i,j,k] in lists:
        lst.append(i+j+k)
    return set(lst)

def jaccard(set1,set2):
    x = len(set.intersection(set1,set2))
    y = len(set.union(set1,set2))
    return(x*1.0/y*1.0)
'''
set1 = k2set(kgram(2,nynews))
set2= k2set(kgram(2,tcnews))

print(jaccard(set1,set2))

print(set.intersection(set1,set2))
'''
def allwords(list_set):
    list_of_words=[]
    for x in list_set:
        for y in x:
            list_of_words.append(y)
    return(list_of_words)

def allnewswords(filenamelist):
    longlist = []
    for i in range(len(filenamelist)):
        longlist.append(dataprep(filenamelist[i])["news"])
    return " ".join(longlist).split(" ")

def termfrequency(files):
    termdict={}
    for term in files:
        if term not in termdict.keys():
            termdict[term] = 1
        else: termdict[term] = termdict[term] + 1
    listxy = []
    for x,y in termdict.items():
        listxy.append([y,x])
    return sorted(listxy)


#print(allnewswords(flist1))

def origin_stoplist(wordsterm):
    stoplista=[]
    stoplist=[]
    for [x,y] in wordsterm:
        if x == 1:
            stoplista.append([x,y])
    for x in wordsterm[-50:]:
        stoplista.append(x)
    #print ("stoplist",stoplista)
    for [x,y] in stoplista:
        stoplist.append(y)
    return stoplist

def stoplist(stopwords0):
    excep=["abortion","clinton","trump","court","president","police","donald"]
    for items in stopwords0:
        if items in excep:
            stopwords0.remove(items)
    return stopwords0

def remove_stop_words(data_list,stop_list):
    for word in data_list:
        if word in stop_list:
            data_list.remove(word)
    return data_list

def main():
    stopwordslist = origin_stoplist(termfrequency(allnewswords(flist1)))
    stopwords = stoplist(stopwordslist)
    arbilist=["isnt","them","turned","say","good","leads","wednesday","leave","says","blue","access","two","takes","point","great","why","draw","other","when","how","made","hes","under","what","very","all","four","causes","but","did","small","told","never","others","along","appears","should","takes","would","only","them","few","tell","today","effort","high","this","can","didnt","give","end","may","earlier","lease","years","still","weeks","then","now","begin","really","large","reason","could","one","their","too"]

    for x in arbilist:
        stopwords.append(x)

    list_of_all_nytimes_sets=[]
    list_of_all_time_sets=[]
    for x in range(len(flist)/2):
        x=2*x
        list_of_all_time_sets.append(k1set(newslist(dataprep(flist[x+1])["news"])))
        list_of_all_nytimes_sets.append(k1set(newslist(dataprep(flist[x])["news"])))
        #print("----{}-and-{}----same words  k=1-------------------".format(flist1[x],flist1[x+1]))
        #print(set.intersection(k1set(newslist(dataprep(flist[x])["news"])),k1set(newslist(dataprep(flist[x+1])["news"]))))
        #print("jaccard similarity",jaccard(k1set(newslist(dataprep(flist[x])["news"])),k1set(newslist(dataprep(flist[x+1])["news"]))))
        #print("----{}-and-{}----same characters  k=2--------------".format(flist1[x],flist1[x+1]))
        #print(set.intersection(k2set(kgram(2,characters(newslist(dataprep(flist[x])["news"])))),k2set(kgram(2,characters(newslist(dataprep(flist[x+1])["news"]))))))
        #print("jaccard similarity",jaccard(k2set(kgram(2,characters(newslist(dataprep(flist[x])["news"])))),k2set(kgram(2,characters(newslist(dataprep(flist[x+1])["news"]))))))

    list_of_all_nytimes_words=allwords(list_of_all_nytimes_sets)
    list_of_all_time_words=allwords(list_of_all_time_sets)
    #print(len(list_of_all_time_words))
    #print(list_of_all_time_words)
    #print(len(list_of_all_nytimes_words))
    #print(list_of_all_nytimes_words)

    all_common_words = remove_stop_words(list(set.intersection(set(list_of_all_nytimes_words),set(list_of_all_time_words))),stopwords)
    all_words = remove_stop_words(list(set.union(set(list_of_all_nytimes_words),set(list_of_all_time_words))),stopwords)
    print(len(all_common_words),all_common_words)
    print(len(all_common_words)*1.0/len(all_words))
    dict_common_words={}
    dict_all_words={}
    pdallnewswords = remove_stop_words(allnewswords(flist1),stopwords)
    print(len(pdallnewswords))

    for item in pdallnewswords:
        if item in dict_all_words.keys():
            dict_all_words[item]=dict_all_words[item]+1
        else: dict_all_words[item] = 1

    print(dict_all_words)
    print(all_common_words)
    for key,value in dict_all_words.items():
        if key in all_common_words:
            dict_common_words[key]=value
    print(dict_common_words)




if __name__ == "__main__":
    main()
