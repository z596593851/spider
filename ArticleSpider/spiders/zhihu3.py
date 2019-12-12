# -*- coding: utf-8 -*-
import scrapy
import json
import os
import re
# from selenium.webdriver.chrome.options import Options
from urllib import parse
from os import path


OSCHINA_PHONE='596593851@qq.com'
OSCHINA_PASSWORD='Hh19950818'

class ZhihuSpider(scrapy.Spider):
    name = 'oschina'
    allowed_domains = ['www.oschina.net']
    start_urls = ['https://www.oschina.net/']
    headers = {
        "HOST": "www.oschina.net",
        "Referer": "https://www.oschina.net",
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/68.0.3440.106 Safari/537.36"
    }
    custom_settings = {
        "COOKIES_ENABLED": True,
        #"DOWNLOAD_DELAY": 1.5,
    }

    def parse(self, response):
        print(response.text)
        all_urls = response.css("a::attr(href)").extract()
        all_urls = [parse.urljoin(response.url, url) for url in all_urls]
        # 使用lambda函数对于每一个url进行过滤，如果是true放回列表，返回false去除。
        all_urls = filter(lambda x: True if x.startswith("https") else False, all_urls)
        for url in all_urls:
            # 具体问题以及具体答案的url我们都要提取出来，或关系
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", url)
            if match_obj:
                # 如果提取到question相关的页面则下载后交由提取函数进行提取
                request_url = match_obj.group(1)
                print(request_url)
                # yield scrapy.Request(request_url, headers=self.headers, callback=self.parse_question)
            else:
                # 注释这里方便调试
                pass
                # 如果不是question页面则直接进一步跟踪
                #yield scrapy.Request(url, headers=self.headers, callback=self.parse)


    def start_requests(self):
        from selenium import webdriver
        import time
        browser = webdriver.PhantomJS()
        # chrome_options = Options()
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--disable-gpu')
        # browser = webdriver.Chrome(options=chrome_options)
        browser.get("https://www.oschina.net/home/login?")
        browser.find_element_by_css_selector("input#userMail").send_keys(OSCHINA_PHONE)
        time.sleep(1)
        browser.find_element_by_css_selector("input#userPassword").send_keys(OSCHINA_PASSWORD)
        time.sleep(2)
        browser.find_element_by_css_selector("button.btn-login").click()
        time.sleep(3)
        browser.get("https://www.oschina.net/")
        time.sleep(4)
        zhihu_cookies = browser.get_cookies()
        #print('zhihu_cookies:')
        print(zhihu_cookies)
        cookie_dict = {}
        import pickle
        for cookie in zhihu_cookies:
            # base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            # f = open(path.join(base_path,cookie['name']+'.txt'), 'wb')
            # pickle.dump(cookie, f)
            # f.close()
            cookie_dict[cookie['name']] = cookie['value']
        print('cookie_dict:')
        print(cookie_dict)
        #browser.close()
        return [scrapy.Request(url=self.start_urls[0], dont_filter=True, cookies=cookie_dict, headers=self.headers)]
        # return [scrapy.Request(url=self.start_urls[0], dont_filter=True, cookies=cookie_dict)]