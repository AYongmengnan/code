import re
import datetime
from urllib.parse import urljoin
import html
from settings import MongoDB
import requests
from parsel import Selector

def parse():
    print('开始启动')
    url = 'https://sg.joblum.com/'
    response = requests.get(url=url,headers=headers,cookies=cookies)
    print(response.status_code)
    resp = Selector(text=response.text)
    url_list = resp.xpath('//div[@class="content-card browse-jobs-card"]/div/div/h3/a/@href').getall()
    for u_li in url_list:
        d_url = urljoin(url,u_li)
        parse_list(d_url)
    return
def parse_list(url):
    print('列表页')
    for p in range(1,100):
        li_url = url + f'?p={p}'
        try:
            response = requests.get(url=li_url,headers=headers,cookies=cookies)
            print(response.status_code)
            resp = Selector(text=response.text)
            d_url = resp.xpath('//div[@class="content-card card-has-jobs"]/div/div[1]/a/@href').getall()
            for d in d_url:
                d_u = urljoin('https://sg.joblum.com/',d)
                parse_detail(d_u)
        except Exception as e:
            print(e)
            continue
    return



def parse_detail(url):
    print('详情页',url)
    response = requests.get(url=url,headers=headers,cookies=cookies)
    print(response.status_code)
    resp = Selector(text=response.text)
    description = resp.xpath('//span[@itemprop="description"]').xpath('string(.)').get()
    phone_pattern = r'\b(?:\(\+?65\)\s*|\+?65\s*[-*^+]?\s*|65\s*[-*^+]?\s*)\d{4}\s*[-*^+]?\s*\d{4}\b'
    # email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    # email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
    cfemail = resp.xpath('//a[@class="__cf_email__"]/@data-cfemail').get()
    cfhref = resp.xpath('//a[@class="__cf_email__"]/@href').get()
    if cfemail and cfhref:
        email = decode_email(cfhref,cfemail)
    else:
        email = None
    phones = re.findall(phone_pattern, description)
    # emails = re.findall(email_pattern, description)
    phones = [ph.strip() for ph in phones] if phones else phones
    phone = ','.join(list(set(phones)))
    name = resp.xpath('//a[@class="job-company-name"]/text()').get()
    save_data = {'name':name,'email':email,'phone':phone,'url':url,'date': datetime.date.today().strftime("%Y-%m-%d")}
    print(save_data)
    res = mdb.insert_one('joblum_sg',save_data)
    print(res)
    return

def decode_email(encoded_path, encoded_email):
    def decode_email_address(encoded_address, key):
        decoded = ''.join(chr(int(encoded_address[i:i+2], 16) ^ key) for i in range(2, len(encoded_address), 2))
        return html.unescape(decoded)

    start_index = encoded_path.find("#") + 1
    key = int(encoded_email[:2], 16)
    return decode_email_address(encoded_email[start_index:], key)
if __name__ == '__main__':
    mdb = MongoDB()
    cookies = {
        'advanced-frontend': 'l099mbc8ro20173qmnfj3el6ru',
        '_csrf-frontend': 'adf24b3b05d93228415609885b67daea823b9c06c82458bf62dfba6d30a0bde2a%3A2%3A%7Bi%3A0%3Bs%3A14%3A%22_csrf-frontend%22%3Bi%3A1%3Bs%3A32%3A%22D7ciqU61J1A9HRUYF-pJbNzY7w5zjR1G%22%3B%7D',
    }

    headers = {
        'authority': 'sg.joblum.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        # 'cookie': 'advanced-frontend=l099mbc8ro20173qmnfj3el6ru; _csrf-frontend=adf24b3b05d93228415609885b67daea823b9c06c82458bf62dfba6d30a0bde2a%3A2%3A%7Bi%3A0%3Bs%3A14%3A%22_csrf-frontend%22%3Bi%3A1%3Bs%3A32%3A%22D7ciqU61J1A9HRUYF-pJbNzY7w5zjR1G%22%3B%7D',
        'pragma': 'no-cache',
        # 'referer': 'https://my.joblum.com/jobs-spec-hospitality-tourism',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    }
    parse()
    # parse_detail('https://sg.joblum.com/job/accountant-fullset-central/3300285')