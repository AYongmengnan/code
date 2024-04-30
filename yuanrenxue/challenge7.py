import requests
import hashlib
import base64
import time
def parse(page):

    data = {
        'page': f'{page}',
    }
    parse_city()
    response = requests.post('https://www.python-spider.com/api/challenge7', cookies=cookies, headers=headers, data=data)
    print('响应:',response)
    data = response.json()
    print(data)
    data = data['data']
    sum = 0
    for da in data:
        value = int(da['value'])
        sum += value
    return sum
    
def parse_city():
    cookies = {
        'no-alert': 'true',
        'sessionid': 'kz9g3v9i6a7rkylafajbsszu0oflwzzk',
        'sign': 'mtnfxrouwv',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        # 'content-length': '0',
        # 'cookie': 'no-alert=true; sessionid=kz9g3v9i6a7rkylafajbsszu0oflwzzk; sign=mtnfxrouwv',
        'origin': 'https://www.python-spider.com',
        'pragma': 'no-cache',
        'referer': 'https://www.python-spider.com/challenge/7',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    }
    response = requests.post('https://www.python-spider.com/cityjson', cookies=cookies, headers=headers)
    return print(response)



if __name__ == '__main__':
    cookies = {
        'no-alert': 'true',
        'sessionid': 'kz9g3v9i6a7rkylafajbsszu0oflwzzk',
        'sign': 'mtnfxrouwv',
    }
    headers = {
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'referer': 'https://www.python-spider.com/challenge/',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    }
    total = 0
    for page in range(1,101):
        res = parse(page)
        total += res
    print(total)

    
    # print(parse(1))
    