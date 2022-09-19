from gc import callbacks
from urllib import response
import scrapy

from baodautu.items import BaodautuItem

class BaoDauTuSpider(scrapy.Spider):
    name = "baodautu_spider"
    allowed_domains = ['baodautu.vn']
    start_urls = ['https://baodautu.vn/thoi-su-d1/']
    def parse(self, response):
        for link in response.css('.main_content a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_content)

    def parse_content(self, response):
        item = BaodautuItem()
        item['title'] = response.xpath('.//div[@class="title-detail"]/text()').get(),
        item['date'] = response.xpath('.//span[@class="post-time"]/text()').get(),
        item['content'] = response.xpath('.//div[@id="content_detail_news"]/p/text()').getall(),
        item['url'] = response.request.url
        yield item

