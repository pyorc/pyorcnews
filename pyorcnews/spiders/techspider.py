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


class NewsSpider(CrawlSpider):
    name = 'techspider'

    start_urls = [
        'http://tech.qq.com'
    ]

    rules = [
        Rule(LinkExtractor(allow='^http://tech.qq.com/a/(\d)*/(\d*).htm$'),
             callback='parse_item', follow=False),
    ]

    def parse_item(self, response):
        logging.info(u"正在爬取网站--->" + response.url)
        item = ItemLoader(item=NewsItem(), response=response)
        sel = Selector(response)
        content = sel.xpath('//div[@id="Cnt-Main-Article-QQ"]/p')
        images = []
        pubTime = content.xpath('//span[@class="pubTime"]/text()').extract()
        if not pubTime:
            logging.warn(u"日期不存在,过滤网站--->" + response.url)
            return
        date_time = pubTime[0]
        date_time = time.strptime(date_time, u"%Y年%m月%d日%H:%M")
        # if datetime(*date_time[:5]) < datetime.today()-timedelta(minutes=60):
        #     return

        item.add_value('date_time', date_time)
        item.add_xpath('title', '//div[@class="hd"]/h1/text()')
        item.add_xpath('reading_number', '//em[@id="top_count"]/text()')
        item.add_xpath('author', '//span[@class="auth"]/text()')
        item.add_value('original_link', response.url)

        nodes = []
        for element in content[0:-2]:
            node = {}
            img = element.xpath('img/@src').extract()
            if img:
                node['type'] = 'img'
                images.append(img[0])
                node['content'] = hashlib.sha1(img[0]).hexdigest() + ".jpg"
                nodes.append(node)
                continue
            title = element.xpath('strong/text()').extract()
            if title:
                node['type'] = 'title'
                node['content'] = title[0]
                nodes.append(node)
                continue
            p = element.xpath('text()').extract()
            if p:
                node['type'] = 'content'
                node['content'] = p[0]
                nodes.append(node)
        if images:
            item.add_value('image_url', hashlib.sha1(images[0]).hexdigest() + ".jpg")
        item.add_value('content', json.dumps(nodes, ensure_ascii=False))
        item.add_value('image_urls', images)
        item.add_value('source', u'腾讯科技')
        yield item.load_item()
