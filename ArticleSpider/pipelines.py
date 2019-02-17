# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

#pipelines可以拦截item
import codecs
import json
from scrapy.exporters import JsonItemExporter
from scrapy.pipelines.images import ImagesPipeline
from twisted.enterprise import adbapi
from .models.es_types import Douban

import MySQLdb
import MySQLdb.cursors

class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item

class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.file=codecs.open('article.json','w',encoding="utf-8")
    def process_item(self, item, spider):
        lines=json.dumps(dict(item),ensure_ascii=False)+"\n"
        self.file.write(lines)
        return item
    def spider_closed(self,spider):
        self.file.close()

class MysqlTwistedPipline(object):
    def __init__(self,dbpool):
        self.dbpool=dbpool

    @classmethod
    def from_settings(cls,settings):
        dbparms=dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool=adbapi.ConnectionPool("MySQLdb",**dbparms)
        return cls(dbpool)

    def process_item(self,item,spider):
        # insert_sql="""
        #     insert into jobbole_article(title,url,front_image_url,date)
        #     VALUES(%s,%s,%s,%s)
        # """
        # self.cursor.execute(insert_sql,(item["title"],item["url"],item["front_image_url"],item["date"]))
        # self.conn.commit()
        query=self.dbpool.runInteraction(self.do_insert,item)
        query.addErrback(self.handle_error,item, spider)


    def handle_error(self,failure,item, spider):
        print(failure)

    def do_insert(self,cursor,item):
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql,params)

class JsonExpoterPipline(object):
    def __init__(self):
        self.file=open('articleexpot2.json','wb')
        self.exporter=JsonItemExporter(self.file,encoding="utf-8",ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self,spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self,item,spider):
        self.exporter.export_item(item)
        return item

class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        if "front_image_url"in item:
            for ok,value in results:
                image_file_path=value["path"]
            item["front_image_path"]=image_file_path#注意不是front_image_url

        return item

class ElasticsearchPipeline(object):

    def process_item(self,item,spider):
        item.save_to_es()
        return item

