from scrapy.linkextractors import LinkExtractor
from scrapy import Selector
from dailycaller.items import DailycallerItem
from scrapy.spiders import Spider 
from scrapy.crawler import CrawlerProcess 
import scrapy

BASE_URL = 'https://dailycaller.com'

articles = []

class QuotesSpider(scrapy.Spider): 
    name = "dailycaller" 
    start_urls = [BASE_URL]

    def parse(self, response):
        article_links = response.xpath('//article/a/@href')
        for link in article_links:
            #TODO: get a better relative link handler
            yield scrapy.Request(BASE_URL + link.extract(), callback=self.parse_article)

    def parse_article(self, response):
        title = response.xpath('//h1/text()')[0].extract()
        time = response.xpath('//time/text()')[0].extract()
        text = '\\n\\n'.join(map(lambda x: x.extract(), response.xpath('//p/text()')))
        yield {'Title': title, 'Date': time, 'Article':text}
