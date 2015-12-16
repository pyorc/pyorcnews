# -*- coding: utf-8 -*-

# Scrapy settings for pyorcnews project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

import sys

sys.path.append('/home/zmy/wangpanjun/pyorc')

import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'pyorc.settings'

DOWNLOAD_HANDLERS = {
    's3': None,
}
LOG_LEVEL = 'INFO'
BOT_NAME = 'pyorcnews'
LOG_STDOUT = True

SPIDER_MODULES = ['pyorcnews.spiders']
NEWSPIDER_MODULE = 'pyorcnews.spiders'


ITEM_PIPELINES = {
    'pyorcnews.pipelines.PyorcNewsPipeline': 303,
    'scrapy.pipelines.images.ImagesPipeline': 301
}
DOWNLOAD_DELAY = 0.25

DOWNLOAD_TIMEOUT = 5

COOKIES_ENABLED = True
# LOG_FILE = '/var/log/pyorc/scrapy/ten_spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'pyorcnews (+http://www.yourdomain.com)'

# IMAGES_THUMBS = {
#     'small': (300, 300),
#     'big': (500, 500),
# }
CONCURRENT_REQUESTS_PER_DOMAIN = 10
IMAGES_STORE = '/home/zmy/pyorcnews'
DOWNLOADER_MIDDLEWARES = {
    # 'pyorcnews.misc.middleware.CustomHttpProxyMiddleware': 400,
    'pyorcnews.misc.middleware.CustomUserAgentMiddleware': 401,
}
DEPTH_LIMIT = 5
# DNSCACHE_ENABLED = False
# COMMANDS_MODULE = 'pyorcnews.commands'
