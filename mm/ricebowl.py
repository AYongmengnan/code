import json
import time

from config import MongoDB, con_redis, Mysql
import requests
from parsel import Selector
import string






def get_list(upper):

    headers = {
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://www.ricebowl.my/company/all?c=A',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'sec-ch-ua-platform': '"macOS"',
    }

    params = {
        'platformId': '1',
        'term': upper,
    }
    try:
        response = requests.get('https://www.ricebowl.my/v3mkapi/seo/all/company', params=params, headers=headers)
    except Exception as e:
        print(e)
        time.sleep(5)
        return get_list(upper)
    print(response.status_code)
    if response.status_code == 200:
        s_data = []
        for resp in response.json():
            emp_profile_id = resp.get('emp_profile_id')
            seo_link = resp.get('seo_link')
            company_name = resp.get('company_name')
            d_url = f'https://www.ricebowl.my/company/{emp_profile_id}-{seo_link}'
            data = {'company_name':company_name,'url':d_url}
            s_data.append(json.dumps(data))
            # res = r.sadd('m:ricebowl',json.dumps(data))
            # print(res)
        res = r.sadd('m:ricebowl',*s_data)
        print(res)
    else:
        print('请求失败')
    return
def get_detail(da):
    info = json.loads(da)
    print(info)
    res1 = r.sismember('m:ricebowl_url',info['url'])
    if res1 == 0:
        headers = {
            'Referer': 'https://www.ricebowl.my/company/all?c=B',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
        }

        try:
            response = requests.get(url=info['url'],
                                    headers=headers,
                                    # proxies=proxies,
                                    timeout=5,
                                    verify=False
                                    )
        except Exception as e:
            print(e)
            time.sleep(20)
            # return get_detail(da)
            return
        html = Selector(text=response.text)
        webset = html.xpath('//div[contains(*,"Company Website")]/p/span/text()').get()
        if webset:
            data = {'company_name':info['company_name'],'website':webset}
            res = mdb.insert_one('remote_ricebowl',data)
            print(res)
            if res:
                r.sadd('m:ricebowl_url',info['url'])
                r.srem('m:ricebowl',da)
    else:
        r.sadd('m:ricebowl_url', info['url'])
        r.srem('m:ricebowl', da)
    return

def start():
    """获取所有详情链接"""
    # 获取大写字母 A 到 Z
    # uppercase_letters = string.ascii_uppercase
    # for upper in uppercase_letters:
    #     print('公司首字母',upper)
    #     get_list(upper)
    """获取公司website"""
    data = r.smembers('m:ricebowl')
    for da in data:
        get_detail(da)
    return



if __name__ == '__main__':
    mdb = MongoDB()
    r = con_redis(2,12)
    # get_list('D')
    proxies = {
        'http': 'http://brd-customer-hl_ed3b84ed-zone-isp_proxy2:ra6ayol2boc8@brd.superproxy.io:22225',
        'https': 'http://brd-customer-hl_ed3b84ed-zone-isp_proxy2:ra6ayol2boc8@brd.superproxy.io:22225'
    }
    start()
    # get_detail(121794,'nz-training-management')