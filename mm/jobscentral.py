import re

from settings import MongoDB
import requests
from parsel import Selector

def parse(page):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    params = {
        'page': f'{page}',
        'limit': '20',
    }

    response = requests.get(
        'https://jobscentral.com.sg/_next/data/Z4SZRclgKL2Blifa3c_fS/en/jobs.json',
        params=params,
        headers=headers,
    )
    print(response)
    data = response.json()
    pageProps = data['pageProps']
    jobs = pageProps['jobs']
    items = jobs['items']
    if items:
        for item in items:
            category = item['category']
            id = item['id']
            url = f'https://jobscentral.com.sg/jobs/{category.lower()}-jobs/{id}'
            company = item['company']['name']
            parse_detail(url,company)


def parse_detail(url,company):
    print(url)
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    response = requests.get(url=url, headers=headers)
    html_content = response.text
    html_content = bytes(html_content, "utf-8").decode("unicode_escape")
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    # phone_pattern = re.compile(r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b')

    # 在文本中查找匹配项
    emails = email_pattern.findall(html_content)
    # phones = phone_pattern.findall(html_content)

    # 打印结果
    emails = list(set(emails))
    if 'example@email.xyz' in emails:
        emails.remove('example@email.xyz')
    # print('company:',company)
    # print("Emails:", emails)
    # print("Phones:", set(phones))
    if emails:
        for email in emails:
            res = mdb.insert_one('email_jobscentral',{'company':company,'email':email})
            print(res)
if __name__ == '__main__':
    mdb = MongoDB()
    for p in range(1,141):
        print(f'第{p}页')
        parse(p)
    # parse(3)

