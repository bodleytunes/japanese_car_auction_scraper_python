'''
Created on 27 Feb 2012

@author: jon
'''
#!/usr/bin/env python
# encoding=utf-8

from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.http import FormRequest
from scrapy.selector import HtmlXPathSelector
from scrapy import log
import sys
### Kludge to set default encoding to utf-8
reload(sys)
sys.setdefaultencoding('utf-8')

class MTQInfraSpider(BaseSpider):
    name = "issold"
    allowed_domains = ["www.mtq.gouv.qc.ca"]
    start_urls = [
        "http://www.mtq.gouv.qc.ca/pls/apex/f?p=102:56:::NO:RP::"
    ]

    def parse(self, response):
        pass







