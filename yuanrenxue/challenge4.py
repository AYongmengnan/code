import requests


def get_proxy():
    # targetURL = "https://myip.top"
    # proxyAddr = "tunnels.qg.net:19357"
    # authKey = "5C757113"
    # password = "21C455842BD4"
    # # 账密模式
    # proxyUrl = "http://%(user)s:%(password)s@%(server)s" % {
    #     "user": authKey,
    #     "password": password,
    #     "server": proxyAddr,
    # }
    # proxies = {
    #     "http": proxyUrl,
    #     "https": proxyUrl,
    # }
    # resp = requests.get(targetURL, proxies=proxies)
    # data = resp.json()
    # print(data)
    # ip = data['ip']
    # return ip
    proxyUrl = "http://%(user)s:%(password)s@%(server)s" % {
    "user": '5C757113',
    "password": '21C455842BD4',
    "server": 'tunnels.qg.net:19357',
    }
    return proxyUrl

def parse(page):
    data = {
        'page': f'{page}',
    }
    # proxies = {
    #     'http': 'http://brd-customer-hl_ed3b84ed-zone-isp_proxy2:ra6ayol2boc8@brd.superproxy.io:22225',
    #     'https': 'http://brd-customer-hl_ed3b84ed-zone-isp_proxy2:ra6ayol2boc8@brd.superproxy.io:22225'}
    proxies = {
        'http': get_proxy(),
        'https': get_proxy()}
    # print(proxies)
    try:
        response = requests.post('https://www.python-spider.com/api/challenge4', 
                                cookies=cookies, 
                                headers=headers, 
                                data=data,
                                proxies=proxies,
                                timeout=5,
                                )
        data = response.json()
        data = data['data']
        sum = 0
        for da in data:
            value = int(da['value'])
            sum += value
        return sum
    except Exception as e:
        print(e)
        return parse(page)
    # print(response.text)
    


if __name__ == "__main__":
    cookies = {
        'no-alert': 'true',
        'sessionid': 'kz9g3v9i6a7rkylafajbsszu0oflwzzk',
        'sign': 'zetfsxrbuy',
    }
    headers = {
        # 'accept': 'application/json, text/javascript, */*; q=0.01',
        # 'accept-language': 'zh-CN,zh;q=0.9',
        # 'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'cookie': 'no-alert=true; sessionid=kz9g3v9i6a7rkylafajbsszu0oflwzzk; sign=zetfsxrbuy',
        'origin': 'https://www.python-spider.com',
        # 'pragma': 'no-cache',
        'referer': 'https://www.python-spider.com/challenge/6',
        # 'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        # 'sec-ch-ua-mobile': '?0',
        # 'sec-ch-ua-platform': '"macOS"',
        # 'sec-fetch-dest': 'empty',
        # 'sec-fetch-mode': 'cors',
        # 'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        # 'x-requested-with': 'XMLHttpRequest',
    }
    session = requests.session()
    session.headers = headers
    session.cookies.update(cookies)
    total = 0
    for page in range(1,101):
        print(page)
        res = parse(page)
        total += res
    print(total)
    
    # a = parse(1)
    # print(a)

    # print(get_proxy())

    
    # print(proxyUrl)

    # resp = requests.get('https://ipinfo.io/ip')
    # print(resp.text)

