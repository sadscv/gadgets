# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

class ScrapyDemoPipeline(object):
    unique_key = set()

    def process_item(self, item, example):
        for key in item:
            self.unique_key.add(key)
        return item

    def close_spider(self, example):
        print('#################', self.unique_key)
