import hashlib
import json
import os
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
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9223")
    # 初始化 WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
    driver.switch_to.new_window('tab')  # 打开一个新的窗口并切换到这个窗口输入网址
    # driver.switch_to.window(driver.window_handles[-1])
    driver.get(url)
    get_data(driver)

def get_data(driver):

    # driver.maximize_window()
    sleep(5)
    # 模拟向下滚动鼠标滚轮
    # 使用WebDriverWait等待页面加载完成
    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located((By.XPATH, '//a[contains(text(), "Company Profile")]')))

    # 点击包含文本"Company Profile"的链接
    company_profile_link = driver.find_element(By.XPATH, '//a[contains(text(), "Company Profile")]')
    # 滚动到要点击的元素位置
    driver.execute_script("arguments[0].scrollIntoView();", company_profile_link)

    # company_profile_link.click()
    # 使用JavaScript进行点击
    driver.execute_script("arguments[0].click();", company_profile_link)

    # 使用WebDriverWait等待页面加载完成
    wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="col"]/h4')))

    # 获取所有匹配的h4元素
    h4_elements = driver.find_elements(By.XPATH, '//div[@class="col"]/h4')
    n = 0
    # 依次点击h4元素并查看内容
    # 循环点击h4元素
    for h4_element in h4_elements:
        driver.execute_script("arguments[0].click();", h4_element)
        # 等待一段时间，以便内容加载（根据实际情况调整等待时间）
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//h3[@class="font-ave m-3 d-none d-md-block"]')))

        # 获取公司名称
        company = driver.find_element(By.XPATH, '//h3[@class="font-ave m-3 d-none d-md-block"]').text
        email,phone = None,None
        # 获取链接文本
        link_texts = driver.find_elements(By.XPATH, '//div[@class="p-2"]/div/div/div/div/div/a')
        if len(link_texts) == 3:
            email = link_texts[0].text
            phone = link_texts[1].text

        if len(link_texts) == 2:
            if '@' in link_texts[0]:
                email = link_texts[0].text
                phone = link_texts[1].text
            else:
                phone = link_texts[0].text
        data = {'company':company,'email':email,'phone':phone,'date':datetime.date.today().strftime("%Y-%m-%d")}
        print(data)
        if email or phone:
            res = mdb.insert_one('email_jobslah',data)
            print(res)
        sleep(3)
    next_page = driver.find_element(By.XPATH,'//ul[@class="pagination justify-content-end custom-pagination"]/li[6]/a')
    print(next_page)
    driver.execute_script("arguments[0].click();", next_page)
    return get_data(driver)


if __name__ == '__main__':
    # r = con_redis(2,0)
    # mdb = MongoDB()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9223")
    chrome_options.add_argument("--disable-application-cache")
    # 初始化 WebDriver
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    mdb = MongoDB()
    url = 'https://www.jobslah.com/jobsearch'
    main(url)




