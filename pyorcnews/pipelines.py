# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging


class PyorcNewsPipeline(object):
    def open_spider(self, spider):
        logging.info(u"～～～Spider START～～～")

    def process_item(self, item, spider):
        for key, value in item.items():
            item[key] = value[0]
        item.save()

    def close_spider(self, spider):
        logging.info(u"～～～Spider END～～～")


