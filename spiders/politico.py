from scrapy.linkextractors import LinkExtractor
from scrapy import Selector
from dailycaller.items import DailycallerItem
from scrapy.spiders import Spider 
from scrapy.crawler import CrawlerProcess 
import scrapy

BASE_URL = 'https://politico.com'

articles = []

class QuotesSpider(scrapy.Spider): 
    name = "politico" 
    start_urls = [BASE_URL]

    def parse(self, response):
        article_links = response.xpath('//div/section/div/h1/a/@href') 
        for link in article_links:
            yield scrapy.Request(link.extract(), callback=self.parse_article)

    def parse_article(self, response):
        title = response.xpath('//header/h1/span/text()')[0].extract()
        time = response.xpath('//footer/p/time/text()')[0].extract()
        text = '\\n\\n'.join(map(lambda x: x.extract(), response.xpath('//div/p/text()')))
        yield {'Title': title, 'Date': time, 'Article':text}
   