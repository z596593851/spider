# -*- coding: utf-8 -*-
import scrapy
import re
import time
import hmac
from hashlib import sha1
import json
import base64
import requests
import PIL.Image as Image
from http import cookiejar
from scrapy.http import Request
from bs4 import BeautifulSoup
try:
    import cookielib
except:
    import http.cookiejar as cookielib


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu2'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    captcha_url = 'https://www.zhihu.com/api/v3/oauth/captcha?lang=en'
    login_url = 'https://www.zhihu.com/api/v3/oauth/sign_in'
    check_url ='https://www.zhihu.com/inbox'
    headers = {
        'Connection':'keep-alive',
        'Host': 'www.zhihu.com',
        'Referer': 'https://www.zhihu.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'grant_type': 'password'
        #'User-Agent':'Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0'
    }
    login_data = {
        'client_id': 'c3cef7c66a1843f8b3a9e6a1e3160e20',
        'grant_type': 'password',
        'source': 'com.zhihu.web',
        'username': '596593851@qq.com',
        'password': 'Hh19950818',
        # 传入'cn'是倒立汉字验证码
        'lang': 'en',
        'ref_source': 'homepage',
    }
    xsrf=''
    udid=''
    captcha=''

    def parse(self, response):
        pass

    def start_requests(self):
        return [scrapy.Request('https://www.zhihu.com/',headers=self.headers,callback=self.get_xsrf)]

    def zhihu_login(self,response):
        print("zhihu_login")
        self.login_data.update({
            'username': '596593851@qq.com',
            'password': 'Hh19950818'
        })

        yield scrapy.FormRequest(self.login_url, formdata=self.login_data, headers=self.headers,
                                   callback=self.check_login)
        # return [scrapy.Request(self.login_url,body=post_data,headers=headers,callback=self.check_login)]
    def check_login(self,response):
        # resp = self.session.get(self.check_url, allow_redirects=False)
        # if resp.status_code == 200:
        #     self.session.cookies.save()
        #     print("登陆成功")
        # print("登陆失败")
        print("into check_login")
        text_json = json.loads(response.text)
        if "msg" in text_json:
            print(text_json["msg"])



    def get_xsrf(self,response):
        cookie = response.request.headers.getlist('Cookie')
        #print(Cookie[0])
        self.xsrf=str(cookie[0]).split(' ')[2][6:-1]
        print(self.xsrf)
        self.headers.update({
            'x-xsrftoken': self.xsrf,
            'x-zse-83': '3_1.1'
        })
        #print(self.headers)
        yield scrapy.Request('https://www.zhihu.com/udid',method='POST',headers=self.headers,callback=self.get_udid)
        # html = response.text
        # BS = BeautifulSoup(html, 'html.parser')
        # xsrf_input = BS.find(attrs={'name': '_xsrf'})
        # pattern = r'value=\"(.*?)\"'
        # self.xsrf = re.findall(pattern, str(xsrf_input))[0]
        # print("获取到xsrf:" + str(self.xsrf))

    def get_udid(self,response):
        #self.udid = re.search(r'[\w=\-]+', response.cookies['d_c0'])[0]
        cookie=response.headers.getlist('Set-Cookie')
        self.udid=str(cookie[0]).split(' ')[0].split('|')[0][8:]
        print('udid:',self.udid)
        timestamp = str(int(time.time() * 1000))
        self.headers.update({
            "x-udid":self.udid
        })
        self.login_data.update({
            'captcha_lang': 'en',
            'timestamp': timestamp,
            'signature': self.get_signature(timestamp)

        })
        yield scrapy.Request('https://www.zhihu.com/api/v3/oauth/captcha?lang=en',
                             headers=self.headers,callback=self.get_captcha)
    def get_signature(self,time_str):
        h = hmac.new(key='d1b964811afb40118a12068ff74a12f4'.encode('utf-8'), digestmod=sha1)
        grant_type = 'password'
        client_id = 'c3cef7c66a1843f8b3a9e6a1e3160e20'
        source = 'com.zhihu.web'
        h.update((grant_type + client_id + source + time_str).encode('utf-8'))
        return h.hexdigest()

    def get_captcha(self,response):

        show_captcha = re.search(r'true', response.text)
        #print(response.text)
        if show_captcha:
            print("需要输入验证码！")
            show_captcha = json.loads(response.text)['img_base64']
            with open('captcha.jpg', 'wb') as f:
                f.write(base64.b64decode(show_captcha))
            try:
                im = Image.open('captcha.jpg')
                im.show()
                im.close()
            except:
                print("打开文件失败！")

            captcha = input('输入验证码:')
            self.captcha=captcha
        else:
            print("不需要验证码")
        self.login_data.update({
            'captcha': self.captcha
        })

        #yield scrapy.Request(self.login_url,headers=self.headers,callback=self.zhihu_login)
        post_data = json.dumps(self.login_data)
        print(self.login_data)
        yield scrapy.FormRequest(self.login_url, method='POST',formdata=self.login_data, headers=self.headers,callback=self.check_login)



