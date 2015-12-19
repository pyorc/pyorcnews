# -*- coding: utf-8 -*-



import hashlib

from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule

from pyorcnews.items import NewsItem
import logging
from pyorcnews.config.config import CATEGORY
from pyorcnews.utils.helper import compare_time,translate_content


class TcehSpider(CrawlSpider):
    name = 'techspider'
    start_urls = [
        'http://tech.qq.com'
    ]

    rules = [
        Rule(LinkExtractor(allow='^http://tech.qq.com/a/(\d)*/(\d*).htm$'),
             callback='parse_item', follow=False),
    ]

    def parse_item(self, response):
        logging.info(u"start crawl  --->  " + response.url)
        item = ItemLoader(item=NewsItem(), response=response)
        sel = Selector(response)
        content = sel.xpath('//div[@id="Cnt-Main-Article-QQ"]/p')
        article_time = content.xpath('//span[@class="pubTime"]/text()').extract()
        date_time = compare_time(article_time, u"%Y年%m月%d日%H:%M")
        if not date_time:
            return
        item.add_xpath('keywords', "//head/meta[@name='keywords']/@content")
        item.add_value('date_time', date_time)
        item.add_xpath('title', '//div[@class="hd"]/h1/text()')
        item.add_xpath('reading_number', '//em[@id="top_count"]/text()')
        item.add_xpath('author', '//span[@class="auth"]/text()')
        item.add_value('original_link', response.url)
        elements = sel.xpath('//div[@id="Cnt-Main-Article-QQ"]/p').extract()
        images, content = translate_content(elements)
        if images:
            item.add_value('image_url', hashlib.sha1(images[0]).hexdigest() + ".jpg")
        item.add_value('content', content)
        item.add_value('image_urls', images)
        item.add_value('source', u'腾讯科技')
        item.add_value('category', CATEGORY.TECHNOLOGY)
        logging.info(u"finished crawl  --->  " + response.url)
        yield item.load_item()
