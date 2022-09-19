# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from typing_extensions import Self
from itemadapter import ItemAdapter
import mysql.connector

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
            title text,
            date text,
            content text,
            url text,
            PRIMARY KEY (id)
        )
        """)



    def process_item(self, item, spider):

        ## Define insert statement
        self.cur.execute(""" insert into baodautu (title, date, content, url) values (%s,%s,%s,%s)""", (
            str(item["title"]),
            str(item["date"]),
            str(item["content"]),
            str(item["url"])
        ))

        ## Execute insert of data into database
        self.conn.commit()

    
    def close_spider(self, spider):

        ## Close cursor & connection to database 
        self.cur.close()
        self.conn.close()

class BaodautuNoDuplicatesPipeline:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = '',
            database = 'baodautudb',
        )

        self.cur = self.conn.cursor()

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS baodautu(
            id int NOT NULL auto_increment, 
            title text,
            date text,
            content text,
            url text,
            PRIMARY KEY (id)
        )
        """)

    def process_item(self, item, spider):
        self.cur.execute("select * from baodautu where title = %s", (item['title'],))
        result = self.cur.fetchone()
        if result:
            spider.logger.warn("Item already in database: %s" % item['title'])
        else:

            ## Define insert statement
            self.cur.execute(""" insert into baodautu (title, date, content, url) values (%s,%s,%s,%s)""", (
                item["title"],
                item["date"],
                item["content"],
                item["url"]
            ))


            self.conn.commit()
        return item

    def close_spider(self, spider):

        self.cur.close()
        self.conn.close()


