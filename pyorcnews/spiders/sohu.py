# -*- coding: utf-8 -*-



import hashlib

from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule

from pyorcnews.items import NewsItem
# noinspection PyUnresolvedReferences
from datetime import datetime, timedelta
import time
import logging
from pyorcnews.config.config import CATEGORY
import re
class NewsSpider(CrawlSpider):
    name = 'sohuspider'

    start_urls = [
        'http://it.sohu.com/internet_2014.shtml'
        # 'http://it.sohu.com/20151218/n431776975.shtml'
    ]


    rules = [
        Rule(LinkExtractor(allow='^http://it.sohu.com/(\d*)/(\w*).shtml$'),
             callback='parse_item', follow=False),
    ]

    def parse_item(self, response):
        item = ItemLoader(item=NewsItem(), response=response)
        images = []
        sel = Selector(response)

        item.add_xpath('title', '//div[@class="news-title"]/h1/text()')
        item.add_xpath('author', '//span[@class="writer"]/a/text()')
        item.add_value('source', u'搜狐网')
        item.add_value('original_link', response.url)
        item.add_value('category', CATEGORY.TECHNOLOGY)
        article_time = sel.xpath('//span[@id="pubtime_baidu"]/text()').extract()
        if not article_time:
            return
        article_time = time.strptime(article_time[0], u"%Y-%m-%d %H:%M:%S")
        item.add_value('date_time', article_time)
        elements = sel.xpath('//div[@id="contentText"]/p').extract()
        content = "".join(elements)
        match = re.findall('src="(http://\S*)"', content)
        for match in match:
            images.append(match)
            content = content.replace(match, hashlib.sha1(match).hexdigest() + ".jpg")
        if images:
            item.add_value('image_url', hashlib.sha1(images[0]).hexdigest() + ".jpg")
        item.add_value('image_urls', images)
        item.add_value('content', content)
        yield item.load_item()
