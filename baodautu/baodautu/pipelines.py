# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from typing_extensions import Self
from itemadapter import ItemAdapter
import mysql.connector
import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline

class CustomImagePipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        request.url.split('/')[-1]



class MyImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        adapter = ItemAdapter(item)
        adapter['image_paths'] = image_paths
        return item



class BaodautuPipeline:

    def __init__(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = '',
            database = 'baodautudb',
        )

        ## Create cursor, used to execute commands
        self.cur = self.conn.cursor()
        
        ## Create quotes table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS baodautu(
            id int NOT NULL auto_increment, 
            title TEXT,
            date TEXT,
            content TEXT,
            url TEXT,
            category TEXT,
            image TEXT,
            PRIMARY KEY (id)
        )
        """)



    def process_item(self, item, spider):

        ## Define insert statement
        self.cur.execute(""" insert into baodautu (title, date, content, category, url, image) values (%s,%s,%s,%s,%s,%s) """, (
            item["title"],
            str(item["date"]),
            item["content"],
            item["category"],
            item["url"],
            item["image"]
        ))

        ## Execute insert of data into database
        self.conn.commit()

    
    def close_spider(self, spider):

        ## Close cursor & connection to database 
        self.cur.close()
        self.conn.close()

class BaodautuWPPipeline:

    def __init__(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = '',
            database = 'bitnami_wordpress',
        )

        ## Create cursor, used to execute commands
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):

        ## Define insert statement
        self.cur.execute(""" insert into wp_posts (post_title, post_content) values (%s,%s) """, (
            item["title"],
            item["content"],
        ))

        ## Execute insert of data into database
        self.conn.commit()

    
    def close_spider(self, spider):

        ## Close cursor & connection to database 
        self.cur.close()
        self.conn.close()


