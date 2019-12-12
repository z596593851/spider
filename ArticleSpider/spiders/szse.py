# -*- coding: utf-8 -*-
import scrapy
import json
import re
from ArticleSpider.items import SESSItem,SZSEItem,ArticleItemLoader

class SZSESpider(scrapy.Spider):
    name = 'szse'
    allowed_domains = ['szse.cn','reportdocs.static.szse.cn']
    start_urls=[]
    json_urls="http://www.szse.cn/api/report/ShowReport/data?CATALOGID=main_wxhj&TABKEY=tab3&PAGENO={0}"
    for i in range(1,87):
        start_urls.append(json_urls.format(i))
    headers={
        "Host":"www.szse.cn",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
             }
    ck_rule=".*?(/.*)'"

    def parse(self, response):
        res_json = json.loads(response.text)[2]["data"]
        for data in res_json:
            item_loader = ArticleItemLoader(item=SZSEItem(), response=response)
            item_loader.add_value("gsdm", data["gsdm"])
            item_loader.add_value("gsjc", data["gsjc"])
            item_loader.add_value("fhrq", data["fhrq"])
            item_loader.add_value("hjlb", data["hjlb"])
            # item_loader.add_value("ck_url", data["ck"])
            url_list = []
            url_list.append("http://reportdocs.static.szse.cn" + re.match(self.ck_rule, data["ck"]).group(1))
            item_loader.add_value("file_urls", url_list)
            szse_item = item_loader.load_item()
            yield szse_item
        # yield scrapy.Request(response.url, headers=self.headers, callback=self.parse_content)
    #
    # def parse_content(self,response):
    #     res_json = json.loads(response.text)[0]["data"]
    #     for data in res_json:
    #         item_loader = ArticleItemLoader(item=SZSEItem(), response=response)
    #         item_loader.add_value("gsdm", data["gsdm"])
    #         item_loader.add_value("gsjc", data["gsjc"])
    #         item_loader.add_value("fhrq", data["fhrq"])
    #         item_loader.add_value("hjlb", data["hjlb"])
    #         # item_loader.add_value("ck_url", data["ck"])
    #         url_list=[]
    #         url_list.append("http://reportdocs.static.szse.cn"+re.match(self.ck_rule,data["ck"]).group(1))
    #         item_loader.add_value("file_urls", url_list)
    #         szse_item = item_loader.load_item()
    #         yield szse_item



