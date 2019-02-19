# -*- coding: utf-8 -*-
import scrapy
import re
import random
import time
from scrapy.http import Request
from urllib import parse
from ArticleSpider.items import ArticleItemLoader,V2exQuItem,V2exCoItem
from scrapy.loader import ItemLoader
from ArticleSpider.utils.common import get_md5

class JobboleSpider(scrapy.Spider):
    name = 'v2ex'
    allowed_domains = ['v2ex.com']
    headers = {
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
               }
    start_urls = 'https://www.v2ex.com/go/create?p=1'
    next_urls='https://www.v2ex.com/go/create?p={0}'
    count = 0
    content_rule = ".*?>(.*)<"
    comment_rule=".*?([0-9]*)"

    def start_requests(self):
        return [scrapy.Request(self.start_urls, headers=self.headers, callback=self.parse)]

    def parse(self,response):
        urls = response.xpath("//span[@class='item_title']/a/@href").extract()
        for url in urls:
            #yield Request(url=parse.urljoin(response.url, url),headers=self.headers, callback=self.parse_detail)
            yield Request(url=parse.urljoin(response.url, url), headers=self.headers, callback=self.parse_question)
        self.count+=1
        yield Request(url=self.next_urls.format(self.count), headers=self.headers, callback=self.parse)

    def parse_question(self, response):
        question_loader = ArticleItemLoader(item=V2exQuItem(), response=response)
        question_loader.add_xpath("title", "//div[@class='header']/h1/text()")
        content=""
        mar_content = response.xpath("//div[@class='markdown_body']").extract()
        if len(mar_content)==0:
            content="".join(response.xpath("//div[@class='topic_content']").extract()).replace("\n","")
        else:
            content="".join(mar_content).replace("\n","")
        match_re1 = re.match(self.content_rule, content)
        if match_re1:
            question_loader.add_value("content",match_re1.group(1))

        comment_count=response.xpath("//div[@class='cell']/span[@class='gray']/text()").extract()
        if len(comment_count)==0:
            question_loader.add_value("comment_count",0)
        else:
            match_re2 = re.match(self.comment_rule, comment_count[0])
            if match_re2:
                question_loader.add_value("comment_count", match_re2.group(1))
        question_loader.add_value("user_id",random.randint(2,14))
        question_loader.add_value("created_date",time.time())
        question_item=question_loader.load_item()
        yield question_item

        pass




