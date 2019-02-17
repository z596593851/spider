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

class ZhihuAccount(object):
    def __init__(self):
        self.login_url = 'https://www.zhihu.com/api/v3/oauth/sign_in'
        self.check_url ='https://www.zhihu.com/inbox'
        self.login_data = {
            'client_id': 'c3cef7c66a1843f8b3a9e6a1e3160e20',
            'grant_type': 'authorization_code',
            'source': 'com.zhihu.web',
            'username': '596593851@qq.com',
            # 'password': 'Hh19950818',
            'password':'Hh19950818',
            # 传入'cn'是倒立汉字验证码
            'lang': 'en',
            'ref_source': 'homepage',
        }
        self.session = requests.session()
        self.session.headers = {
            'Host': 'www.zhihu.com',
            'grant_type': 'password',
            'Referer': 'https://www.zhihu.com/',
            # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
            #               '(KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3538.110 Safari/537.36'
        }
        self.session.cookies = cookiejar.LWPCookieJar(filename='./cookies.txt')

    def check_login(self):
        resp = self.session.get(self.check_url, allow_redirects=False)
        if resp.status_code == 200:
            self.session.cookies.save()
            return True
        return False

    def is_login(self):
        if self.load_cookies():
            if self.check_login():
                print('登录成功')
                return True
        self.zhihu_login("596593851@qq.com", "Hh19950818")

    def zhihu_login(self,account, password):
        headers = self.session.headers.copy()
        headers.update({
            'x-xsrftoken': self.get_xsrf(),
            'x-zse-83': '3_1.1'
        })
        self.session.headers=headers['x-udid']=self.get_udid(headers)
        self.login_data.update({
            'username': account,
            'password': password,
            'captcha_lang': 'en'
        })
        timestamp = str(int(time.time()*1000))
        self.login_data.update({
            'captcha': self.get_captcha(headers),
            'timestamp': timestamp,
            'signature': self.get_signature(timestamp)
        })
        print(self.login_data)
        resp = self.session.post(self.login_url, data=self.login_data, headers=headers)
        if 'error' in resp.text:
            print(json.loads(resp.text)['error']['message'])
        if self.check_login():
            print('登录成功')
            return True
        print('登录失败')
        return False

    def load_cookies(self):
        try:
            self.session.cookies.load(ignore_discard=True)
            return True
        except FileNotFoundError:
            return False

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
if __name__ == '__main__':
    zh=ZhihuAccount()
    zh.is_login()
