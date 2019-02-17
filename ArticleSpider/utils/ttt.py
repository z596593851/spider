import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
ZHIHU_PHONE='596593851@qq.com'
ZHIHU_PASSWORD='Hh19950818'
if __name__ == '__main__':

    #browser = webdriver.PhantomJS()
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
