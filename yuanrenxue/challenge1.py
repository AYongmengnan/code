import requests
import hashlib
import base64
import time
def parse(page):
    cookies = {
        'no-alert': 'true',
        'sessionid': 'kz9g3v9i6a7rkylafajbsszu0oflwzzk',
    }
    token,timestamp = generate_tokens()
    headers = {
        # 'accept': 'application/json, text/javascript, */*; q=0.01',
        # 'accept-language': 'zh-CN,zh;q=0.9',
        # 'cache-control': 'no-cache',
        # 'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'cookie': 'no-alert=true; sessionid=kz9g3v9i6a7rkylafajbsszu0oflwzzk',
        # 'origin': 'https://www.python-spider.com',
        # 'pragma': 'no-cache',
        'referer': 'https://www.python-spider.com/challenge/1',
        'safe': token,
        # 'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        # 'sec-ch-ua-mobile': '?0',
        # 'sec-ch-ua-platform': '"macOS"',
        # 'sec-fetch-dest': 'empty',
        # 'sec-fetch-mode': 'cors',
        # 'sec-fetch-site': 'same-origin',
        'timestamp': timestamp,
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        # 'x-requested-with': 'XMLHttpRequest',
    }

    data = {
        'page': f'{page}',
    }

    response = requests.post('https://www.python-spider.com/api/challenge1', cookies=cookies, headers=headers, data=data)
    data = response.json()
    # print(data)
    data = data['data']
    sum = 0
    for da in data:
        value = int(da['value'])
        sum += value
    return sum
    
def generate_tokens():
    # 计算当前时间的 UNIX 时间戳
    timestamp = str(int(time.time()))
    # 将字符串a和时间戳拼接起来
    concatenated_str = '9622' + timestamp
    base_str = base64.b64encode(concatenated_str.encode()).decode()
    # 计算MD5哈希值
    tokens = hashlib.md5(base_str.encode()).hexdigest()
    return tokens,timestamp

if __name__ == '__main__':
    total = 0
    for page in range(1,101):
        res = parse(page)
        total += res
    print(total)