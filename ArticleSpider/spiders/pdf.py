# -*- coding: utf-8 -*-
import scrapy
import json
import re
from ArticleSpider.items import SESSItem,SZSEItem,PDFItem,ArticleItemLoader

class PDFSpider(scrapy.Spider):
    name = 'pdf'
    allowed_domains = ['szse.cn','reportdocs.static.szse.cn']
    start_urls=["http://www.szse.cn/api/report/ShowReport/data?CATALOGID=main_wxhj&TABKEY=tab1&PAGENO=1"]
    headers={
                "Host": "www.szse.cn",
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
             }

    def parse(self, response):
        res_json = json.loads(response.text)[0]["data"]
        item_loader = ArticleItemLoader(item=PDFItem(), response=response)
        url_list=["http://reportdocs.static.szse.cn/UpFiles/fxklwxhj/CDD00079356200.pdf"]
        item_loader.add_value("file_urls", url_list)
        pdf_item = item_loader.load_item()
        yield pdf_item



