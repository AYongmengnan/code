import urllib.parse
from config import MongoDB
import requests
from parsel import Selector

def parse(page):

    headers = {
        'authority': 'jawatankosong.com',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    params = {
        'page': str(page),
    }

    response = requests.get('https://jawatankosong.com/User/Job/SearchJobs',
                            params=params,
                            # cookies=cookies,
                            headers=headers
                            )
    print(response.status_code)
    html = Selector(text=response.text)
    list = html.xpath('//div[@class="content"]/h4/a/@href').getall()
    if list:
        for li in list:
            d_url = urllib.parse.urljoin('https://jawatankosong.com/',li)
            parse_detail(d_url)
    return
def parse_detail(url):

    headers = {
        'authority': 'jawatankosong.com',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    response = requests.get(url, headers=headers)
    # print(response)
    print(response.status_code)
    html = Selector(text=response.text)
    name = html.xpath('//h5[@class="company-name"]/text()').get()
    name = name.strip() if name else None
    phone = html.xpath('//ul[@class="company-info"]/li[contains(text(),"Phone")]/span/a/text()').get()
    phone = phone.strip() if phone else None
    email = html.xpath('//ul[@class="company-info"]/li[contains(text(),"Email")]/span/a/text()').get()
    email = email.strip() if email else None
    social = html.xpath('//ul[@class="company-info"]/li/div[@class="social-links"]/a/@href').get()
    title = html.xpath('//div[@class="content"]/h4/text()').get()
    title = title.strip() if title else None
    website = html.xpath('//div[@class="widget-content"]/div[@class="btn-box"]/a/@href').get()
    # print(name,phone,email,website,social,title,url)
    save_data = {'name':name,'phone':phone,'email':email,'website':website,'social':social,'title':title,'url':url}
    # print(save_data)
    mdb.insert_one('jawatankosong',save_data)
    return
if __name__ == '__main__':
    mdb = MongoDB()
    for p in range(1,46):
        parse(p)
    # parse_detail()


