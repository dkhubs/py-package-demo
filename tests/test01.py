import time
from selenium import webdriver

def test_yoyo_01(browser):
    browser.get('https://www.cnblogs.com/yoyoketang/')
    time.sleep(3)
    t = browser.title
    assert t == '上海-悠悠'