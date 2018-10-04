from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Selector
from dailycaller.items import DailycallerItem

class MySpider(Spider):
    name = "dc"
    allowed_domains = ["dailycaller.com"]
    start_urls = ["http://dailycaller.com/"]

    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[@class="button next"]',)), callback="parse_items", follow= True),
    )

    def parse(self, response):
        hxs = Selector(response)
        titles = hxs.xpath("///article") 
        items = []
        for title in titles:
            print(title.xpath("./a"))
            item = DailycallerItem()
            item ["title"] = title.xpath("./a/h3/text()").extract()
            item ["link"] = title.xpath("./a/@href").extract()
            items.append(item)
        print("hxs", hxs)
        return items

#convert to Jupyter
#append link to DataFrame
#crawl DF links