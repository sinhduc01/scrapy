import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from baodautu.items import BaodautuItem
import re
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo

wp = Client('http://localhost/wordpress/xmlrpc.php', 'user', 'mfOd Ol6M rLFS QLYK Y7JL KoTA')
wp.call(GetPosts())
wp.call(GetUserInfo())

def strip_value(value):
    m = re.search("http[^\s]+(\s)*h?(http[^\s>]+)(\s)*", value)
    if m:
        return m.group(2)
    else:
        return value

class BaoDauTuSpider(CrawlSpider):
    name = "baodautu"
    allowed_domains = ['baodautu.vn']
    start_urls = [
            'https://baodautu.vn/doanh-nghiep-d3/',
            'https://baodautu.vn/quoc-te-d54/',
            'https://baodautu.vn/thoi-su-d1/',
            'https://baodautu.vn/doanh-nhan-d4/',
            'https://baodautu.vn/ngan-hang-d5/'
    ]       
    rules = (

        Rule(LinkExtractor(allow='',
                           deny=['/abc/'],
                           process_value=strip_value,
                           restrict_xpaths=["//nav[@class='d-flex pagation align-items-center']"]), follow=True, process_links=None),
        Rule(LinkExtractor(allow='',
                           deny=['/abc/'],
                           process_value=strip_value,
                           restrict_xpaths=["//a[@class='fs22 fbold'] | //a[@class='fs32 fbold'] | //a[@class='fs18 fbold'] | //a[@class='title_thumb_square fs16']"]), follow=False, callback='parse_item', process_links=None)
    )
    def parse_item(self, response):
        item = BaodautuItem()
        item['category'] = response.xpath("//div[@class='fs16 text-uppercase ']/a/text()").get().strip()
        item['title'] = response.xpath("//div[@class='title-detail']/text()").get().strip() 
        item['image'] = response.xpath("//div[@id='content_detail_news']//img/@src").get()
        item['image_urls'] = {response.xpath("//div[@id='content_detail_news']//img/@src").get()}
        list_p = response.xpath("//div[@id='content_detail_news']//p//text()").getall()
        item['content'] = str(list_p)
        item['date'] = response.xpath("//span[@class='post-time']/text()").get().strip().replace("-", "")
        item['url'] = response.request.url
        post = WordPressPost()
        post.title = item['title']
        post.content = item['content']
        post.post_status = 'publish'
        post.terms_names = {
            'post_tag': [item['category'], 'baodautu'],
            'category': item['category']
        }
        wp.call(NewPost(post))
        return item


