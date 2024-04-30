import hashlib
import json
import os
import re
import time

from settings import MongoDB
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep
from parsel import Selector
import datetime
def main(url):
    # 使用命令打开单独的浏览器
    '/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9223 --user-data-dir=/Users/mark/code/chrome/9223'
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9223")
    # # 初始化 WebDriver
    # chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
    # driver.switch_to.new_window('tab')  # 打开一个新的窗口并切换到这个窗口输入网址
    # driver.switch_to.window(driver.window_handles[-1])
    driver.get(url)
    get_data(driver)

def get_data(driver):
    sleep(5)
    # driver.maximize_window()
    # sleep(5)
    # 模拟向下滚动鼠标滚轮
    # 使用WebDriverWait等待页面加载完成
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class,"job-post")]/a')))

    html = driver.page_source
    text = Selector(text=html)
    # url_elements = driver.find_elements(By.XPATH, '//div[@id="jobslist"]/a')
    # driver.switch_to.new_window('tab')
    # urls = [u.get_attribute('href') for u in url_elements]
    # for u in urls:
    urls = text.xpath('//div[contains(@class,"job-post")]/a')
    for u in urls:

        url = u.xpath('@href').get()
        name = u.xpath('div//span[@class="visible-xs"]/strong/text()').get().strip()
        # driver.switch_to.new_window('tab')
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        sleep(5)
        wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="job-desc rtf-content"]')))
        html = driver.page_source
        text = Selector(text=html)
        # name = text.xpath('//div[@class="panel panel-default job-action-panel"]//h2/text()').get()
        content = text.xpath('//div[@class="job-desc rtf-content"]').xpath('string(.)').get()
        # phone_pattern = r'\b(?:\+65\s*[\d\-]+|65\s*[\d\-]+|6\d{7}|8\d{7}|9\d{7})\b'
        # phone_pattern = r'\b(?:\+?65\s*[\d\-]+|6\d{7}|8\d{7}|9\d{7})\b'
        # phone_pattern = r'\b(?:\+?65\s*[\d\-]+|6\d{7}|8\d{7}|9\d{7}|\d{4}-\d{4})\b'
        # phone_pattern = r'\b(?:\+?65\s*[\d\-]+|6\d{7}|8\d{7}|9\d{7}|\d{4}[\s\-]?\d{4})\b'
        # phone_pattern = r'\b(?:\+?65\s*[\d\-]+|6\d{7}|8\d{7}|9\d{7}|\d{4}[\s\-]?\d{4}|\d{8}|\d{4}\^\d{4}|\d{4}\*\d{4})\b'
        phone_pattern = r'\b(?:\+?65\s*[\d\-]+|6\d{7}|8\d{7}|9\d{7}|\d{4}[\s\-]?\d{4}|\d{8}|\d{4}\^\d{4}|\d{4}\*\d{4}|\+\d{6,10})\b'

        singapore_phones = re.findall(phone_pattern, content)
        cleaned_phone_numbers = [re.sub(r'\D', '', phone_number) for phone_number in singapore_phones]
        phone = ','.join(list(set(cleaned_phone_numbers)))
        # print(singapore_phones)
        telegram_pattern = r'(?<!\w)@[\w\d_]+'
        telegram_contacts = re.findall(telegram_pattern, content)
        telegram = ','.join(list(set(telegram_contacts)))
        email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        emails = re.findall(email_pattern, content)
        email = ','.join(list(set(emails)))
        print(url)
        print({'name':name,'email':email,'phone':phone,'telegram':telegram,'date':datetime.date.today().strftime("%Y-%m-%d"),'url':url})
        res = mdb.insert_one('fastjobs2',{'name':name,'email':email,'phone':phone,'telegram':telegram,'date':datetime.date.today().strftime("%Y-%m-%d"),'url':url})
        # print(name, singapore_phones, telegram_contacts, emails)
        print(res)
        # driver.close()
        # driver.switch_to.window(driver.window_handles[-1])
    driver.delete_all_cookies()
    # driver.close()
    return sleep(2)

if __name__ == '__main__':
    # r = con_redis(2,0)
    # mdb = MongoDB()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9223")
    chrome_options.add_argument("--disable-application-cache")

    # 初始化 WebDriver
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    mdb = MongoDB()

    for p in range(27,50):
        print(f'获取第{p}页')
        url = f'https://www.fastjobs.sg/singapore-jobs/en/all-categories-jobs/page-{p}/'
        main(url)
        sleep(10)
