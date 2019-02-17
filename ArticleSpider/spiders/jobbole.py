# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from urllib import parse
from ArticleSpider.items import JobBoleArticleItem,ArticleItemLoader
from scrapy.loader import ItemLoader
from ArticleSpider.utils.common import get_md5

class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts']
    def parse(self, response):
        post_nodes=response.css("#archive .floated-thumb .post-thumb a")
        for post_node in post_nodes:
            image_url=post_node.css("img::attr(src)").extract_first("")
            post_url=post_node.css("::attr(href)").extract_first("")
            yield Request(url=parse.urljoin(response.url,post_url),meta={"front_image_url":image_url},callback=self.parse_detail)
        next_url=response.css(".next.page-numbers::attr(href)").extract_first("")
        if next_url:
            yield Request(url=parse.urljoin(response.url,next_url),callback=self.parse)
    def parse_detail(self,response):
        # article_item=JobBoleArticleItem()
        # front_image_url=response.meta.get("front_image_url","")
        # title=response.css('.entry-header h1::text').extract()
        # date=response.css("p.entry-meta-hide-on-mobile::text").extract()[0].strip()
        # content=response.css("div.entry").extract()[0]
        # # match_obj= re.match(".*项目",title)
        # # if match_obj:
        # #     print(match_obj.group(0))
        # article_item["url_object_id"]=get_md5(response.url)
        # article_item["title"]=title
        # article_item["url"]=response.url
        # article_item["date"]=date
        # article_item["front_image_url"]=[front_image_url]
        # article_item["content"]=content
        front_image_url=response.meta.get("front_image_url","")
        item_loader=ArticleItemLoader(item=JobBoleArticleItem(),response=response)
        item_loader.add_css("title",".entry-header h1::text")
        item_loader.add_css("date","p.entry-meta-hide-on-mobile::text")
        item_loader.add_css("content","div.entry")
        item_loader.add_value("url_object_id",get_md5(response.url))
        item_loader.add_value("url",response.url)
        item_loader.add_value("front_image_url",[front_image_url])

        article_item=item_loader.load_item()

        yield article_item

