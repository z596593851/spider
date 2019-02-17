# -*- coding: utf-8 -*-
import scrapy
import json
import re
from ArticleSpider.items import DouBanItem,ArticleItemLoader

class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['douban.com']
    #start_urls = ['http://https://www.douban.com/']
    start_urls="https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%BB%8F%E5%85%B8&sort=rank&page_limit=20&page_start=0"
    json_urls="https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%BB%8F%E5%85%B8&sort=rank&page_limit=20&page_start={0}"
    headers={"Host":"movie.douban.com",
             "Referer":"https://movie.douban.com/explore",
             "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
             "X-Requested-With":"XMLHttpRequest"
             }
    count = 0
    info_rule = "((^[\u4e00-\u9fa5]|[A-Za-z]).*)"
    time_rule="^[(](.*)[)]$"

    def start_requests(self):
        return [scrapy.Request(self.start_urls, headers=self.headers, callback=self.parse)]

    def parse(self, response):
        movies_json=json.loads(response.text)["subjects"]

        for movie_json in movies_json:
            movie_url=movie_json["url"]
            print(movie_url)
            yield scrapy.Request(movie_url,headers=self.headers,callback=self.parse_content)
        self.count+=20
        yield scrapy.Request(self.json_urls.format(self.count), headers=self.headers, callback=self.parse)

    def parse_content(self,response):
        item_loader = ArticleItemLoader(item=DouBanItem(), response=response)
        item_loader.add_value("url",response.url)
        item_loader.add_xpath("title","//div[@id='content']/h1/span[1]/text()")
        #item_loader.add_xpath("time","//div[@id='content']/h1/span[2]/text()")
        item_loader.add_xpath("director","//div[@id='info']/span[1]/span[2]/a/text()")
        #item_loader.add_xpath("area","//*[@id='info']/text()[8]")
        #item_loader.add_xpath("language","//*[@id='info']/text()[10]")
        item_loader.add_css("score","div.rating_self strong::text")
        item_loader.add_xpath("introduction","//span[@property='v:summary']/text()")
        item_loader.add_xpath("front_image_url","//*[@id='mainpic']/a/img/@src")
        infos=response.xpath("//*[@id='info']/text()").extract()
        info_list=[]
        for info in infos:
            match_re = re.match(self.info_rule, info.strip())
            if match_re:
                info_list.append(match_re.group(1))
        time=response.xpath("//div[@id='content']/h1/span[2]/text()").extract()[0]
        match_re = re.match(self.time_rule, time)
        if match_re:
            item_loader.add_value("time",match_re.group(1))
        item_loader.add_value("area",info_list[0])
        item_loader.add_value("language",info_list[1])
        item_loader.add_value("nickname",info_list[2])

        douban_item = item_loader.load_item()
        yield douban_item

