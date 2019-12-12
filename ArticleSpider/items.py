# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose,TakeFirst
# from .models.es_types import Douban

class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ArticleItemLoader(ItemLoader):
    default_output_processor=TakeFirst()

def return_value(value):
    return value

class JobBoleArticleItem(scrapy.Item):
    title=scrapy.Field(
        input_processor=MapCompose(lambda x:x+"-jobbole")
    )
    url=scrapy.Field()
    url_object_id=scrapy.Field()
    date=scrapy.Field()
    front_image_url=scrapy.Field(
        output_processor=MapCompose(return_value)
    )
    front_image_path=scrapy.Field()
    content=scrapy.Field()

class V2exQuItem(scrapy.Item):
    title=scrapy.Field()
    content=scrapy.Field()
    user_id=scrapy.Field()
    created_date=scrapy.Field()
    comment_count=scrapy.Field()
    def get_insert_sql(self):
        insert_sql = """
                            insert into question(title,content,user_id,created_date,comment_count)
                            VALUES(%s,%s,%s,%s,%s)
                        """
        title = self["title"]
        content = self["content"]
        user_id = self["user_id"]
        created_date = self["created_date"]
        comment_count = self["comment_count"]
        params = (title,content,user_id,created_date,comment_count)
        return insert_sql, params

class V2exCoItem(scrapy.Item):
    content=scrapy.Field()
    user_id=scrapy.Field()
    entity_id=scrapy.Field()
    entity_type=scrapy.Field()
    created_date=scrapy.Field()
    status=scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                            insert into comment(content,user_id,entity_id,entity_type,created_date,status)
                            VALUES(%s,%s,%s,%s,%s,%s)
                        """
        content = self["content"]
        user_id = self["user_id"]
        entity_id = self["entity_id"]
        entity_type = self["entity_type"]
        created_date = self["created_date"]
        status = self["status"]
        params = (content,user_id,entity_id,entity_type,created_date,status)
        return insert_sql, params

class PDFItem(scrapy.Item):
    file_urls = scrapy.Field(
        output_processor=MapCompose(return_value)
    )
    files = scrapy.Field()

class SESSItem(scrapy.Item):
    stockcode=scrapy.Field()
    extGSJC=scrapy.Field()
    cmsOpDate=scrapy.Field()
    extWTFL=scrapy.Field()
    # docURL=scrapy.Field(
    #     output_processor=MapCompose(return_value)
    # )
    docTitle=scrapy.Field()
    file_urls = scrapy.Field(
        output_processor=MapCompose(return_value)
    )
    docPath = scrapy.Field()
    files = scrapy.Field()
    def get_insert_sql(self):
        insert_sql = """
                            insert into sse2(stockcode,extGSJC,cmsOpDate,extWTFL,docTitle,docPath,fileUrls)
                            VALUES(%s,%s,%s,%s,%s,%s,%s)
                        """
        stockcode = self["stockcode"]
        extGSJC = self["extGSJC"]
        cmsOpDate = self["cmsOpDate"]
        extWTFL = self["extWTFL"]
        docTitle = self["docTitle"]
        fileUrls = self["file_urls"]
        docPath = self["docPath"]

        params = (stockcode,extGSJC,cmsOpDate,extWTFL,docTitle,docPath,fileUrls)
        return insert_sql, params

class SZSEItem(scrapy.Item):
    gsdm=scrapy.Field()
    gsjc=scrapy.Field()
    fhrq=scrapy.Field()
    hjlb=scrapy.Field()
    file_urls = scrapy.Field(
        output_processor=MapCompose(return_value)
    )
    docPath = scrapy.Field()
    files = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                            insert into szse(gsdm,gsjc,fhrq,hjlb,fileUrls,docPath,type)
                            VALUES(%s,%s,%s,%s,%s,%s,%s)
                        """
        gsdm = self["gsdm"]
        gsjc = self["gsjc"]
        fhrq = self["fhrq"]
        hjlb = self["hjlb"]
        fileUrls = self["file_urls"]
        docPath = self["docPath"]
        type = "创业板"
        params = (gsdm,gsjc,fhrq,hjlb,fileUrls,docPath,type)
        return insert_sql, params




class DouBanItem(scrapy.Item):
    url=scrapy.Field()
    title=scrapy.Field()
    time=scrapy.Field()
    director=scrapy.Field()
    area=scrapy.Field()
    language=scrapy.Field()
    nickname=scrapy.Field()
    score=scrapy.Field()
    introduction=scrapy.Field()
    front_image_url = scrapy.Field(
        output_processor=MapCompose(return_value)
    )
    front_image_path=scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                    insert into high_score(url,title,time,director,area,language,nickname,score,introduction,front_image_url,front_image_path)
                    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
        url=self["url"]
        title =self["title"]
        time=self["time"]
        director=self["director"]
        area=self["area"]
        language=self["language"]
        nickname=self["nickname"]
        score=self["score"]
        introduction=self["introduction"]
        front_image_url=self["front_image_url"]
        front_image_path=self["front_image_path"]
        params=(url,title,time,director,area,language,nickname,score,introduction,front_image_url,front_image_path)
        return insert_sql, params

    def save_to_es(self):
        douban=Douban()
        douban.url=self['url']
        douban.title =self['title']
        douban.time =self['time']
        douban.director =self['director']
        douban.area =self['area']
        douban.language =self['language']
        douban.nickname =self['nickname']
        douban.score =self['score']
        douban.introduction =self['introduction']
        douban.front_image_url =self['front_image_url']
        douban.front_image_path = self['front_image_path']

        douban.save()
        return





