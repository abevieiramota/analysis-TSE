# -*- encoding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from tse_scrapy.items import TSEItem

class TSESpider(CrawlSpider):

    name = "TSESpider"
    start_urls = ['http://arquivos.portaldatransparencia.gov.br/downloads.asp?a=%(ano)d&m=%(mes)s&d=%(tipo)s&consulta=Servidores' % {'ano': ano, 'mes': str(mes).rjust(2, '0'), 'tipo': tipo} for ano in [2012,2013,2014] for mes in xrange(1,13) for tipo in ['C', 'M']]

    def parse(self, response):

        zip = ServidoresItem(file_urls=[response.url])

        yield zip
