# -*- coding: utf-8 -*-



import hashlib
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from pyorcnews.items import NewsItem
import logging
from pyorcnews.config.config import CATEGORY
from pyorcnews.utils.helper import compare_time, translate_content


class NewsSpider(CrawlSpider):
    name = 'cnbetaspider'

    start_urls = [
        'http://www.cnbeta.com/'
    ]

    rules = [
        Rule(LinkExtractor(allow='/articles/(\d*).htm$'),
             callback='parse_item', follow=False),
    ]

    def parse_item(self, response):
        logging.info(u"start crawl  --->  " + response.url)
        item = ItemLoader(item=NewsItem(), response=response)
        sel = Selector(response)
        article_time = sel.xpath('//span[@class="date"]/text()').extract()
        date_time = compare_time(article_time)
        if not date_time:
            return
        item.add_xpath('keywords', "//head/meta[@name='keywords']/@content")
        item.add_value('date_time', date_time)
        item.add_xpath('title', '//h2[@id="news_title"]/text()')
        item.add_value('original_link', response.url)
        elements = sel.xpath('//div[@class="content"]/p').extract()
        images, content = translate_content(elements)
        if images:
            item.add_value('image_url', hashlib.sha1(images[0]).hexdigest() + ".jpg")
        item.add_value('content', content)
        item.add_value('image_urls', images)
        item.add_value('source', u'cnBeta')
        item.add_value('category', CATEGORY.TECHNOLOGY)
        logging.info(u"finished crawl  --->  " + response.url)
        yield item.load_item()
