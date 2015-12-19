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
import re
class LeiphoneSpider(CrawlSpider):
    name = 'leiphonespider'
    start_urls = [
        # 'http://www.leiphone.com/',
        'http://www.leiphone.com/news/201512/BfKL8DFWiRfg2eju.html'
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
        elements = content.xpath("h2|p").extract()
        content = "".join(elements)
        match = re.findall('src="(http://\S*)"', content)
        images = []
        for match in match:
            images.append(match)
            content = content.replace(match, hashlib.sha1(match).hexdigest() + ".jpg")
        if images:
            item.add_value('image_url', hashlib.sha1(images[0]).hexdigest() + ".jpg")
        item.add_value('image_urls', images)
        item.add_value('content', content)
        item.add_value('original_link', response.url)
        yield item.load_item()