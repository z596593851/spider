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
try:
    import cookielib
except:
    import http.cookiejar as cookielib


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu1'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    captcha_url = 'https://www.zhihu.com/api/v3/oauth/captcha?lang=en'
    login_url = 'https://www.zhihu.com/api/v3/oauth/sign_in'
    check_url ='https://www.zhihu.com/inbox'
    session = requests.session()
    session.headers = {
        'Connection':'keep-alive',
        'Host': 'www.zhihu.com',
        'Referer': 'https://www.zhihu.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        #'User-Agent':'Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0'
    }
    login_data = {
        'client_id': 'c3cef7c66a1843f8b3a9e6a1e3160e20',
        'grant_type': 'password',
        'source': 'com.zhihu.web',
        'username': '596593851@qq.com',
        'password':'Hh19950818',
        # 传入'cn'是倒立汉字验证码
        'lang': 'en',
        'ref_source': 'homepage',
    }

    def parse(self, response):
        pass

    def start_requests(self):
        print("start_request")
        headers = self.session.headers.copy()
        headers.update({
            'xsrftoken': self.get_xsrf(),
            'x-zse-83': '3_1.1'
        })
        # self.session.headers=headers['x-udid']=self.get_udid(headers)
        self.session.headers = headers['x-udid'] = self.get_udid(headers)
        self.login_data.update({
            # 'username': "596593851@qq.com",
            # 'password': "Hh19950818",
            'captcha_lang': 'en'
        })
        timestamp = str(int(time.time() * 1000))
        self.login_data.update({
            'captcha': self.get_captcha(headers),
            'timestamp': timestamp,
            'signature': self.get_signature(timestamp)
        })
        post_data = json.dumps(self.login_data)
        print(post_data)
        return [scrapy.FormRequest(self.login_url,method='POST', formdata=self.login_data,headers=headers,callback=self.check_login)]
        #return [scrapy.Request(self.login_url,body=post_data,headers=headers,callback=self.check_login)]

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

    # def zhihu_login(self,response):
    #     print('into zhihu_login')
    #     headers = self.session.headers.copy()
    #     headers.update({
    #         'xsrftoken': self.get_xsrf(),
    #         'x-zse-83': '3_1.1'
    #     })
    #     # self.session.headers=headers['x-udid']=self.get_udid(headers)
    #     self.session.headers = headers['x-udid'] = self.get_udid(headers)
    #     self.login_data.update({
    #         'username': "596593851@qq.com",
    #         'password': "Hh19950818",
    #         'captcha_lang': 'en'
    #     })
    #     timestamp = str(int(time.time()*1000))
    #     self.login_data.update({
    #         'captcha': self.get_captcha(headers),
    #         'timestamp': timestamp,
    #         'signature': self.get_signature(timestamp)
    #     })
    #     post_data = json.dumps(self.login_data)
    #     print(post_data)
    #     #return [scrapy.FormRequest(self.login_url,formdata=self.login_data,headers=headers,callback=self.check_login)]
    #     yield scrapy.Request(self.login_url,body=post_data,headers=headers,callback=self.check_login)


    # def load_cookies(self):
    #     try:
    #         self.session.cookies.load(ignore_discard=True)
    #         return True
    #     except FileNotFoundError:
    #         return False

    def get_xsrf(self):
        resp = self.session.get('https://www.zhihu.com/', allow_redirects=False)
        xsrf = resp.cookies['_xsrf']
        return xsrf

    def get_signature(self,time_str):
        h = hmac.new(key='d1b964811afb40118a12068ff74a12f4'.encode('utf-8'), digestmod=sha1)
        grant_type = 'password'
        client_id = 'c3cef7c66a1843f8b3a9e6a1e3160e20'
        source = 'com.zhihu.web'
        h.update((grant_type + client_id + source + time_str).encode('utf-8'))
        return h.hexdigest()

    def get_udid(self,headers):
        resp = self.session.post('https://www.zhihu.com/udid', headers=headers)
        udid = re.search(r'[\w=\-]+', resp.cookies['d_c0'])[0]
        print('udid:',udid)
        return udid

    def get_captcha(self,headers):
        captcha_url = 'https://www.zhihu.com/api/v3/oauth/captcha?lang=en'
        #response = session.get(captcha_url, headers=header)
        resp = self.session.get(captcha_url, headers=headers)
        show_captcha = re.search(r'true', resp.text)
        print(resp.text)
        if show_captcha:
            print("需要输入验证码！")
            response = self.session.put('https://www.zhihu.com/api/v3/oauth/captcha?lang=en', headers=headers)
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

            return captcha
        else:
            return ''

