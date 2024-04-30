import re
from urllib.parse import unquote
from config import MongoDB, con_redis, Mysql
import requests
from parsel import Selector


def get_list_url(page):
    response = requests.get(f'https://www.internsg.com/jobs/{page}/',
                            cookies=cookies,
                            headers=headers)
    html = Selector(text=response.text)
    list_url = html.xpath('//div[contains(@class,"ast-row list")]/div[@class="ast-col-lg-3"]/a/@href').getall()
    for url in list_url:
        get_detail(url)
    return
def get_detail(url):
    response = requests.get(
        url=url,
        cookies=cookies,
        headers=headers,
    )
    print(response)
    html1 = Selector(text=response.text)
    # print(response.text)
    company = html1.xpath('//article/div/div/div[1]/div[1]/div[2]/text()').get()
    emails = html1.xpath('//span[contains(@id,"eeb")]/following-sibling::script/text()').getall()
    email_list = []
    for em in emails:
       ema = get_mi_ml_o(em)
       email_list.append(ema)
    # print(email_list)
    # email = ','.join(email_list)
    # print(email)
    if email_list:
        for email in email_list:
            print(email)
            res = mdb.insert_one('test_internsg',{'company':company,'email':email})
            print(res)
    return

def decrypt_string(mi, ml):
    o = ""
    for j in range(len(mi)):
        o += ml[ord(mi[j]) - 48]
    return unquote(o)

def get_mi_ml_o(input_string):
    o = None
    ml_match = re.findall(r'ml="(.*?)"', input_string)
    mi_match = re.findall(r'mi="(.*?)"', input_string)
    o_match = re.findall(r'eval\(decodeURIComponent\("(.*?)"\)', input_string)
    if mi_match and ml_match:
        mi = mi_match[0]
        ml = ml_match[0]
        o = decrypt_string(mi,ml)

    if o_match:
        o = unquote(o_match[0]).replace("'","")

    return o



if __name__ == '__main__':
    mdb = MongoDB()
    cookies = {
        'PHPSESSID': 'fb629242fd7654c037fbe25d83822209',
    }

    headers = {
        'authority': 'www.internsg.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        # 'cookie': 'PHPSESSID=fb629242fd7654c037fbe25d83822209',
        'pragma': 'no-cache',
        'referer': 'https://www.internsg.com/jobs/',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    for p in range(1,39):
        print(f'第{p}页')
        get_list_url(p)
    # url = 'https://www.internsg.com/job/iny-financial-pte-ltd-marketing-and-research-intern/?f_pg=7'
    # get_detail(url)