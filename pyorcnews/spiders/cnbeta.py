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
from pyorcnews.config.config import CATEGORY


class NewsSpider(CrawlSpider):
    name = 'cnbetaspider'

    start_urls = [
        'http://www.cnbeta.com/'
        # 'http://www.cnbeta.com/articles/458539.htm'
    ]

    rules = [
        Rule(LinkExtractor(allow='/articles/(\d*).htm$'),
             callback='parse_item', follow=False),
    ]

    def parse_item(self, response):
        item = ItemLoader(item=NewsItem(), response=response)
        sel = Selector(response)
        article_time = sel.xpath('//span[@class="date"]/text()').extract()
        if not article_time:
            return
        date_time = time.strptime(article_time[0], u"%Y-%m-%d %H:%M:%S")

        # # if datetime(*date_time[:5]) < datetime.today()-timedelta(minutes=60):
        # #     return
        #
        item.add_xpath('keywords', "//head/meta[@name='keywords']/@content")
        item.add_value('date_time', date_time)
        item.add_xpath('title', '//h2[@id="news_title"]/text()')
        item.add_value('original_link', response.url)
        elements = sel.xpath('//div[@class="content"]/p').extract()
        content = "".join(elements)
        match = re.findall('src="(http://\S*)"', content)
        images = []
        for match in match:
            images.append(match)
            content = content.replace(match, hashlib.sha1(match).hexdigest() + ".jpg")
        if images:
            item.add_value('image_url', hashlib.sha1(images[0]).hexdigest() + ".jpg")
        item.add_value('content', content)
        item.add_value('image_urls', images)
        item.add_value('source', u'cnBeta')
        item.add_value('category', CATEGORY.TECHNOLOGY)
        #
        yield item.load_item()
