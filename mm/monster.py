import re

from config import MongoDB, con_redis, Mysql
import requests
from parsel import Selector

def get_list():
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    params = {
        'page': '1',
    }

    response = requests.get('https://www.monster.ca/jobs/q-remote-jobs', params=params,
                            headers=headers)
    # print(response)
    response = Selector(text=response.text)
    detail_url = response.xpath('//section[1]/a/@href').getall()
    # print(detail_url)
    if detail_url:
        for d_u in detail_url:
            get_detail(d_u)



def get_detail(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    response = requests.get(
        url=url,
        headers=headers,
    )
    response = Selector(text=response.text)
    company = response.xpath('//h3[contains(@class,"descriptionstyles__CompanyName")]/text()').get()
    content = response.xpath('//div[contains(@class,"main-layoutstyles")]/section[contains(@class,"cached-bot-fjv-skeletonstyle")]').xpath('string(.)').get()
    email = get_emails(content)
    phone = extract_phone_numbers3(content)
    print(company,email,phone)
    print(url)





def get_emails(text):
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    emails = email_pattern.findall(text)
    emails = list(set(emails))
    email = ','.join(emails) if emails else None
    return email

def extract_phone_numbers3(text):
    # 匹配常见的电话号码格式，包括国际区号、分隔符等
    phone_pattern = re.compile(r'''
        (?:\+\d{1,2}\s?)?          # 匹配国际区号，例如：+1 或 +12
        (?:\(\d{1,4}\)\s?)?        # 匹配带括号的区号，例如：(123) 或 (1234)
        \d{1,4}                    # 匹配区号后的数字部分，最多4位
        (?:[-.\s]?\d{1,4})?        # 匹配主体部分，最多4位，包括可选的分隔符
        (?:[-.\s]?\d{1,4})?        # 匹配尾部部分，最多4位，包括可选的分隔符
    ''', re.VERBOSE)

    # 使用正则表达式在文本中查找匹配的电话号码
    phone_numbers = re.findall(phone_pattern, text)
    phone_numbers = [number for number in list(set(phone_numbers)) if len(number) >= 8]
    phone = ','.join(phone_numbers) if phone_numbers else None
    return phone


if __name__ == '__main__':
    mdb = MongoDB()
    get_list()
