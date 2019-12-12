# -*- coding: utf-8 -*-
import scrapy
import json
import re
from ArticleSpider.items import SESSItem,ArticleItemLoader

class SSESpider(scrapy.Spider):
    name = 'sse'
    allowed_domains = ['sse.com.cn']
    start_urls=[]

    json_urls="http://query.sse.com.cn/commonSoaQuery.do?" \
               "siteId=28&sqlId=BS_KCB_GGLL&channelId=10743%2C10744%2C10012&" \
               "order=createTime%7Cdesc%2Cstockcode%7Casc&isPagination=true&pageHelp.pageSize=15&" \
               "pageHelp.pageNo={0}&pageHelp.beginPage={0}"
    for i in range(1,117):
        start_urls.append(json_urls.format(i))
    headers={"Host":"query.sse.com.cn",
             "Referer":"http://www.sse.com.cn/disclosure/credibility/supervision/inquiries/",
             "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"
             }
    info_rule = "((^[\u4e00-\u9fa5]|[A-Za-z]).*)"
    time_rule="^[(](.*)[)]$"

    # def start_requests(self):
    #     return [scrapy.Request(self.start_urls, headers=self.headers, callback=self.parse_content)]
    #
    def parse(self, response):
        yield scrapy.Request(response.url, headers=self.headers, callback=self.parse_content)
        # if self.count<self.end:
        #     self.count += 1
        #     yield scrapy.Request(self.json_urls.format(self.count), headers=self.headers, callback=self.parse)
    def parse_content(self,response):
        response=response
        res_json= json.loads(response.text)
        res_json = res_json["pageHelp"]["data"]

        for data in res_json:
            item_loader = ArticleItemLoader(item=SESSItem(), response=response)
            item_loader.add_value("stockcode", data["stockcode"])
            item_loader.add_value("extGSJC", data["extGSJC"])
            item_loader.add_value("cmsOpDate", data["cmsOpDate"])
            item_loader.add_value("extWTFL", data["extWTFL"])
            item_loader.add_value("docTitle", data["docTitle"])
            url_list=[]
            url_list.append("http://"+data["docURL"])
            item_loader.add_value("file_urls", url_list)
            see_item = item_loader.load_item()
            yield see_item



