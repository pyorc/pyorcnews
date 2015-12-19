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
    name = 'huxiuspider'

    start_urls = [
        'http://www.huxiu.com'
    ]


    rules = [
        Rule(LinkExtractor(allow='/article/(\d)*/1.htm'),
             callback='parse_item', follow=False),
    ]

    def parse_item(self, response):
        logging.info(u"正在爬取网站--->" + response.url)
        item = ItemLoader(item=NewsItem(), response=response)
        images = []
        sel = Selector(response)

        if sel.xpath('//div[@class="neirong-shouquan"]'):
            return
        item.add_xpath('title', '//div[@class="article-wrap"]/h1/text()')
        item.add_xpath('author', '//span[@class="author-name"]/text()')
        item.add_value('source', u'虎嗅网')
        item.add_value('original_link', response.url)
        item.add_value('category', CATEGORY.TECHNOLOGY)
        article_time = sel.xpath('//span[@class="article-time"]/text()').extract()
        if not article_time:
            return
        article_time = time.strptime(article_time[0], u"%Y-%m-%d %H:%M")
        item.add_value('date_time', article_time)
        image_url = sel.xpath('//div[@class="article-img-box"]/img/@src').extract()[0]
        images.append(image_url)
        elements = sel.xpath('//div[@id="article_content"]/p').extract()
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
