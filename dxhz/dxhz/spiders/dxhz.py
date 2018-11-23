import scrapy,re
from bs4 import BeautifulSoup
from scrapy.http import Request
from qsbk.items import QsbkItem
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
class Myspider(CrawlSpider):
    name = 'dxhz'
    #allowed_domains = ["qiushibaike.com"]
    start_urls = ['https://www.hao123.com']
    rules = [
        Rule(LinkExtractor(allow=r'https://www.qiushibaike.com/hot/.*?'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'https://www.qiushibaike.com/8hr/.*?'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'https://www.qiushibaike.com/history/.*?'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'https://www.qiushibaike.com/text/.*?'), callback='parse_item', follow=True),
    ]

    def parse_item(self,response):
        divs = BeautifulSoup(response.text,'lxml').find_all('div',{"class":re.compile('article block untagged mb15.*?')})
        for div in divs:
            item = QsbkItem()
            a=div.find('h2').get_text()
            c=div.find('div',class_='content').find('span').get_text()
            t=re.split('/',response.url)[-4]
            thumb='https:'
            item['thumb']=''
            if div.find('div',class_='thumb'):
                item['thumb']=thumb+str(div.find('div',class_='thumb').find('img')['src'])
                print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            else:
                print('no thumb')
            item['author']=str(a)
            item['content']=str(c)
            item['qs_type']=str(t)
            item['l']=str(response.url)
               
            yield item