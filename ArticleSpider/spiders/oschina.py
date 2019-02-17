
OSCHINA_PHONE='596593851@qq.com'
OSCHINA_PASSWORD='Hh19950818'
if __name__ == '__main__':
    from selenium import webdriver
    import time

    chrome_opt=webdriver.ChromeOptions()
    prefs={"profile.managed_default_content_settings.images":2}
    chrome_opt.add_experimental_option("prefs",prefs)
    browser = webdriver.Chrome(chrome_options=chrome_opt)
    browser.get("https://www.oschina.net/home/login?")
    browser.find_element_by_css_selector("input#userMail").send_keys(OSCHINA_PHONE)
    time.sleep(1)
    browser.find_element_by_css_selector("input#userPassword").send_keys(OSCHINA_PASSWORD)
    time.sleep(2)
    browser.find_element_by_css_selector("button.btn-login").click()