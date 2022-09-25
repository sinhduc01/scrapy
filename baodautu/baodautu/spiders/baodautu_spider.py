from gc import callbacks
from urllib import response
import scrapy

from baodautu.items import BaodautuItem

class BaoDauTuSpider(scrapy.Spider):
    name = "baodautu_spider"
    allowed_domains = ['baodautu.vn']
    start_urls = ['https://baodautu.vn/']
    def parse(self, response):
        for link in response.css('.main_content a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_content)

    def parse_content(self, response):
        item = BaodautuItem()
        posts = response.css('.div.col630')
        for post in posts:
            item['title'] = post.css('div.title-detail::text').get().strip(),
            item['date'] = post.css('span.post-time::text').get().strip(),
            item['content'] = post.css('#content_detail_news p::text').getall().strip(),
            item['category'] = post.css('div.fs16 a::text').get(),
            item['url'] = post.css.url,
        yield item

