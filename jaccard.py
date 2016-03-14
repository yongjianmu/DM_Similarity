import fileinput
import os
import json 


flist = ["scrapy/nytimes/2016-03-05.json","scrapy/timecome/2016-03-05.json","scrapy/nytimes/2016-03-06.json","scrapy/timecome/2016-03-06.json","scrapy/nytimes/2016-03-07.json","scrapy/timecome/2016-03-07.json","scrapy/nytimes/2016-03-08.json","scrapy/timecome/2016-03-08.json","scrapy/nytimes/2016-03-12.json","scrapy/timecome/2016-03-12.json","scrapy/nytimes/2016-03-13.json","scrapy/timecome/2016-03-13.json"]

wordslist=[]
 

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
                    valuelist.append(data.encode('utf-8').strip().replace('/',' ').replace("'",' ').replace(".",' ').replace(",",' ').replace(":"," "))
            else: 
                for data in y:
                    data = data.lower()
                    valuelist.append(data.encode('utf-8').strip().replace('/',' ').replace("'",' ').replace(".",' ').replace(",",' ').replace(":"," "))
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

def result():
    for x in range(len(flist)/2):
        x=2*x
        print("---------the common words  k=1--------")
        print(set.intersection(k1set(newslist(dataprep(flist[x])["news"])),k1set(newslist(dataprep(flist[x+1])["news"]))))
        print(jaccard(k1set(newslist(dataprep(flist[x])["news"])),k1set(newslist(dataprep(flist[x+1])["news"]))))
        print("---------the common characters  k=2--------")
        print(set.intersection(k2set(kgram(2,characters(newslist(dataprep(flist[x])["news"])))),k2set(kgram(2,characters(newslist(dataprep(flist[x+1])["news"]))))))
        print(jaccard(k2set(kgram(2,characters(newslist(dataprep(flist[x])["news"])))),k2set(kgram(2,characters(newslist(dataprep(flist[x+1])["news"]))))))
        

result()

