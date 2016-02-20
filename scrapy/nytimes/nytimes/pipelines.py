# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs

class NytimesPipeline(object):
    def process_item(self, item, spider):
        for x in item['sectionnews']:
            item['sectionnews'] =  item['sectionnews'].encode("ascii","ignore")
            print ('--------')
            print x
        return item
