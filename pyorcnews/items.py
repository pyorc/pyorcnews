# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy_djangoitem import DjangoItem
# noinspection PyUnresolvedReferences
from news.models import NewsModel
from scrapy.item import Field


class NewsItem(DjangoItem):
    django_model = NewsModel
    image_urls =Field()