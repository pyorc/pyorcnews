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


class LeiphoneSpider(CrawlSpider):
    name = 'leiphonespider'
    start_urls = [
        'http://www.leiphone.com/',
    ]
    rules = [
        Rule(LinkExtractor(allow='http://www.leiphone.com/news/(\d*)/(\w*).html'),
             callback='parse_item', follow=False),
    ]

    def parse_item(self, response):
        logging.info(u"start crawl  --->  " + response.url)
        item = ItemLoader(item=NewsItem(), response=response)
        sel = Selector(response)
        item.add_xpath('keywords', "//head/meta[@name='keywords']/@content")
        item.add_xpath('title', '//div[@class="pageTop"]/h1/text()')
        item.add_xpath('author', '//div[@class="pi-author"]/a/text()')
        article_time = " ".join(sel.xpath('//div[@class="pi-author"]/span/text()').extract())
        date_time = compare_time([article_time], "%Y-%m-%d %H:%M")
        if not date_time:
            return
        item.add_value('date_time', date_time)
        content = sel.xpath("//div[@class='pageCont lph-article-comView ']")
        elements = content.xpath("h2|p").extract()
        images, content = translate_content(elements)
        if images:
            item.add_value('image_url', hashlib.sha1(images[0]).hexdigest() + ".jpg")
        item.add_value('image_urls', images)
        item.add_value('content', content)
        item.add_value('original_link', response.url)
        item.add_value('category', CATEGORY.TECHNOLOGY)
        item.add_value('source', u'雷锋网')
        logging.info(u"finished crawl  --->  " + response.url)
        yield item.load_item()
