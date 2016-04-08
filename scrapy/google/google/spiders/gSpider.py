import scrapy
from scrapy.contrib.loader import ItemLoader
from google.items import googleItem
import json
import datetime

class gSpider(scrapy.Spider):
    name = 'google'
    start_urls = ['https://news.google.com/']
    def parse(self,response):
        l = ItemLoader(item = googleItem(),response = response)
        l.add_xpath('news','//span[contains(@class,"titletext")]/text()')
        x = l.load_item()
        #print(len(x['date']),len(x['topnews']),len(x['sectionnews']))
        nytdict = dict()
        datelist = []
        datalist = datetime.date.today()
        newslist = []

        nytdict['date'] = str(datalist)

        for t in x['news']:
            newslist.append(str(t.encode('ascii','ignore')))
        nytdict['news']=newslist

        filename = datetime.date.today()
        f=open('{}.json'.format(filename),'w')
        json.dump(nytdict,f)
        return l.load_item()
