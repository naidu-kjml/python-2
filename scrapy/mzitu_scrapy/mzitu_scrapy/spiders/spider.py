from scrapy import Request
from scrapy.spider import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from mzitu_scrapy.items import MzituScrapyItem


class Spider(CrawlSpider):
    name = 'mzitu'
    allowed_domains = ['51cto.com']
    start_urls = ['http://blog.51cto.com/xqtesting/']
    img_urls = []
    rules = (
        Rule(LinkExtractor(allow=('http://blog.51cto.com/xqtesting/\d{1,7}',), deny=('http://www.mzitu.com/\d{1,6}/\d{1,6}')),
             callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        print(response.url)