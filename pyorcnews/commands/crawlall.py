# -*- coding: utf-8 -*-

from scrapy.commands import ScrapyCommand


class Command(ScrapyCommand):

    requires_project = True

    def syntax(self):
        return '[options]'

    def short_desc(self):
        return 'Runs all of the spiders'

    def run(self, args, opts):
        for spider_name in self.crawler_process.spiders.list():
            self.crawler_process.crawl(spider_name)
        print self.crawler_process.start()