
# -*- encoding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from tse_scrapy.items import TSEItem

class TSESpider(CrawlSpider):

    name = "TSESpider"
    start_urls = ["http://www.tse.jus.br/hotSites/pesquisas-eleitorais/index.html"]
    handle_httpstatus_list = [404]

    rules = (
        Rule(LinkExtractor(allow=('\.html', )), follow=True),
        Rule(LinkExtractor(allow=('\.zip', ), deny=('buweb'), deny_extensions=[]), callback='parse_zip'),
        )

    def parse_zip(self, response):

        zip = TSEItem(file_urls=[response.url], content_types=[response.headers['Content-Type']])

        yield zip