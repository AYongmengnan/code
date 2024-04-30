import csv
import datetime
import html
import re
from urllib.parse import urljoin

from settings import MongoDB
import requests
from parsel import Selector

def parse(page):
    params = {
        'p': f'{page}',
    }
    try:
        response = requests.get('https://sg.joblum.com/jobs', params=params, headers=headers)
        print(response.status_code)
        resp = Selector(text=response.text)
        d_url = resp.xpath('//div[@class="content-card card-has-jobs"]/div/div[1]/a/@href').getall()
        for d in d_url:
            d_u = urljoin('https://sg.joblum.com/', d)
            parse_detail(d_u)
    except Exception as e:
        print(e)

def parse_detail(url):
    print('详情页',url)
    response = requests.get(url=url,headers=headers)
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

def export_data():
    result = list(mdb.find('joblum_sg',{},{'_id':0}).limit(100))
    print(result)
    csv_file = './data/joblum_sg.csv'
    with open(csv_file, 'w', newline='',encoding='utf-8') as csvfile:
        fieldnames = list(result[0].keys())  # 获取字段名
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # 写入字段名
        writer.writeheader()

        # 写入查询结果
        for document in result:
            writer.writerow(document)

if __name__ == '__main__':
    mdb = MongoDB()
    headers = {
        'Referer': 'https://sg.joblum.com/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }
    url = 'https://sg.joblum.com/job/dishwasher/3384181'
    # parse_detail(url)
    # for page in range(1,100):
    #     parse(page)
    export_data()