import scrapy
from scrapy.contrib.loader import ItemLoader
from nytimes.items import NytimesItem
import json

class nytSpider(scrapy.Spider):
    name = 'nyt'
    start_urls = ['http://www.nytimes.com']


    def parse(self,response):
        l = ItemLoader(item = NytimesItem(),response = response)
        l.add_xpath('date', '//*[@id="masthead"]/div[4]/ul/li[1]/text()')
        l.add_xpath('topnews','//*[contains(@id,"topnews-100")]/h2/a/text()')
        l.add_xpath('sectionnews','//h3[contains(@class,"story-heading")]/text()')
        print('----------------------------')
        #print(type(l.load_item()))
        x = l.load_item()
        #print(len(x['date']),len(x['topnews']),len(x['sectionnews']))
        nytdict = dict()
        datelist = []
        topnewslist = []
        sectionnewslist = []
        for t in x['date']:
            nytdict['date'] = str(t)

        for t in x['topnews']:
            topnewslist.append(str(t.encode('ascii','ignore')))
        nytdict['topnews']=topnewslist

        for t in x['sectionnews']:
            sectionnewslist.append(str(t.encode('ascii','ignore')).strip())
        nytdict['sectionnews']=sectionnewslist
        print(nytdict)
        f =  open('nytimes.json','w')
        json.dump(nytdict,f)
        return l.load_item()
