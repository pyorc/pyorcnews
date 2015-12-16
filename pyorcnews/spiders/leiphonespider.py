# -*- coding: utf-8 -*-

import json

from scrapy.linkextractors import LinkExtractor

from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from pyorcnews.items import NewsItem
import hashlib
# noinspection PyUnresolvedReferences
from datetime import datetime, timedelta
import time
import logging
class LeiphoneSpider(CrawlSpider):
    name = 'leiphonespider'
    start_urls = [
        # 'http://www.leiphone.com/',
        'http://www.leiphone.com/news/201512/rmKU2Xf9m4cJZCOM.html'
    ]
# http://www.leiphone.com/news/201512/GuTyT6y60UcHt1BX.html
#     rules = [
#         Rule(LinkExtractor(allow='^http://www.leiphone.com/news/(\d*)/(\w*).html$'),
#              callback='parse_item', follow=False),
#     ]

    def parse(self, response):
        item = ItemLoader(item=NewsItem(), response=response)
        sel = Selector(response)
        item.add_xpath('title', '//div[@class="pageTop"]/h1/text()')
        item.add_xpath('author', '//div[@class="pi-author"]/a/text()')
        date_time = " ".join(sel.xpath('//div[@class="pi-author"]/span/text()').extract())
        date_time = time.strptime(date_time, u"%Y-%m-%d %H:%M")
        item.add_value('date_time', date_time)
        content = sel.xpath("//div[@class='pageCont lph-article-comView ']")
        elements = content.xpath("h2")
        for element in elements:
            print element.extract()
        # print(len(content))
        # print(elements[len(elements)-2].extract())
        # print(response.url)
        yield item.load_item()