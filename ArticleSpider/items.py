# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose,TakeFirst
from .models.es_types import Douban

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





