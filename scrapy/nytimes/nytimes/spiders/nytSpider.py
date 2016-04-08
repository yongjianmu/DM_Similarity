import scrapy
from scrapy.loader import ItemLoader
from nytimes.items import NytimesItem
import json
import datetime

class nytSpider(scrapy.Spider):
    name = 'nyt'
    start_urls = ['http://www.nytimes.com']


    def parse(self,response):
        l = ItemLoader(item = NytimesItem(),response = response)
        l.add_xpath('topnews','//*[contains(@id,"topnews-100")]/h2/a/text()')
        l.add_xpath('sectionnews','//h3[contains(@class,"story-heading")]/text()')
        #print(type(l.load_item()))
        x = l.load_item()
        #print(len(x['date']),len(x['topnews']),len(x['sectionnews']))
        nytdict = dict()
        datelist = []
        datalist = datetime.date.today()
        topnewslist = []
        sectionnewslist = []
        nytdict['date'] = str(datalist)

        for t in x['topnews']:
            topnewslist.append(str(t.encode('ascii','ignore')))
        nytdict['topnews']=topnewslist

        for t in x['sectionnews']:
            sectionnewslist.append(str(t.encode('ascii','ignore')).strip())
        nytdict['sectionnews']=sectionnewslist

        filename = datetime.date.today()
        f=open('{}.json'.format(filename),'w')
        json.dump(nytdict,f)
        return l.load_item()
