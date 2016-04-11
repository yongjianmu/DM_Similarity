import scrapy
from scrapy.contrib.loader import ItemLoader
from timecom.items import timeItem
import json
import datetime

class tcSpider(scrapy.Spider):
    name = 'tc'
    start_urls = ['http://www.time.com']
    filename = datetime.date.today()
    def parse(self,response):
        l = ItemLoader(item = timeItem(),response = response)
        #l.add_xpath('topnews','//*[@id="article-container"]/div/div[1]/section/div/article[*]/div/p/text()')
        l.add_xpath('topnews','//*[@id="article-container"]/div/div[1]/section/div/article[*]/div/h2/a/text()')
        l.add_xpath('topnews','//*[@id="article-container"]/div/div[1]/section/div/article[1]/div/div/div[2]/div[*]/h3/a/text()')
        l.add_xpath('sectionnews','//a[contains(@class,"home-columnists-title")]/text()')
        l.add_xpath('sectionnews','//a[contains(@data-event,"hp-news")]/text()')
        x = l.load_item()

        nytdict = dict()
        datelist = []
        datalist = datetime.date.today()
        topnewslist = []
        sectionnewslist = []
        nytdict['date'] = str(datalist)

        for t in x['topnews']:
            topnewslist.append(str(t.encode('ascii','ignore')).strip())
        nytdict['topnews']=topnewslist

        for t in x['sectionnews']:
            sectionnewslist.append(str(t.encode('ascii','ignore')).strip())
        nytdict['sectionnews']=sectionnewslist

        filename = datetime.date.today()
        f=open('{}.json'.format(filename),'w')
        json.dump(nytdict,f)
        return l.load_item()
