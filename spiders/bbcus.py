from scrapy.linkextractors import LinkExtractor
from scrapy import Selector
from dailycaller.items import DailycallerItem
from scrapy.spiders import Spider 
from scrapy.crawler import CrawlerProcess 
import scrapy

BASE_URL = 'https://www.bbc.com'

articles = []

class QuotesSpider(scrapy.Spider): 
    name = "bbcus" 
    start_urls = [BASE_URL]

    def parse(self, response):
        article_links = response.xpath('//div/a/@href') #11 divs before the a/href!
        for link in article_links:
            yield scrapy.Request(BASE_URL + link.extract(), callback=self.parse_article)

    def parse_article(self, response):
        title = response.xpath('//div/div/div/div/h1/text()')[0].extract()
        time = response.xpath('//ul/li/div/text()')[0].extract()
        text = '\\n\\n'.join(map(lambda x: x.extract(), response.xpath('//div/div/div/div/div/p/text()')))
        yield {'Title': title, 'Date': time, 'Article':text}
#This scrape is faulty. Some dates not being populated. Includes links to sections as well as articles. No <article> tags!