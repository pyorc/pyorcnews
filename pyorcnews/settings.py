# -*- coding: utf-8 -*-

# Scrapy settings for pyorcnews project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

# 将django项目添加到path中,并把模块配置到环境变量中(DjangoItem)
import sys
sys.path.append('/home/zmy/wangpanjun/pyorc')
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'pyorc.settings'

# 取消s3方式
DOWNLOAD_HANDLERS = {
    's3': None,
}

BOT_NAME = 'pyorcnews'

SPIDER_MODULES = ['pyorcnews.spiders']
NEWSPIDER_MODULE = 'pyorcnews.spiders'

# 中间组件
ITEM_PIPELINES = {
    'pyorcnews.pipelines.PyorcNewsPipeline': 303,  # 存储通道
    'scrapy.pipelines.images.ImagesPipeline': 301  # 激活图片组件
}

# 爬取间隔时间(防止爬出网站的服务器压力过大)
DOWNLOAD_DELAY = 0.25

COOKIES_ENABLED = True

# 超时时间
DOWNLOAD_TIMEOUT = 5

# 日志级别(包含及其以上)
LOG_LEVEL = 'INFO'

# 日志存放位置
# LOG_STDOUT = True 表示标准输出打印到日志中
LOG_FILE = '/var/log/pyorcnews/spiders.log'

# 图片存放位置(需要激活图片组件)
# IMAGES_STORE = '/home/zmy/wangpanjun/pyorcnews'
# IMAGES_THUMBS = {
#     'small': (300, 300),
#     'big': (500, 500),
# }

# 最大并发量(缓解服务器压力)
CONCURRENT_REQUESTS_PER_DOMAIN = 10

# 开启代理
DOWNLOADER_MIDDLEWARES = {
    # 'pyorcnews.misc.middleware.CustomHttpProxyMiddleware': 400,
    'pyorcnews.misc.middleware.CustomUserAgentMiddleware': 401,
}
# 爬取的最大深度
DEPTH_LIMIT = 2
# DNSCACHE_ENABLED = False
# COMMANDS_MODULE = 'pyorcnews.commands'
