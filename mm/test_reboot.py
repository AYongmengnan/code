import requests
def parse():
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://www.jobslah.com',
        'Referer': 'https://www.jobslah.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'X-CSRF-Token': '4leEx/JGL0xhuM1BNdH14SB5cMwmP/vH9IUmZ00BMTeuLh0rVjS7hHyg6eE7FockuEpPs73SlxuzCpKO0j9/Ywlq7VuZTvgHjtxR885je8NReAuRzm06enVNEeW3iTdqeuAi9xuATJG1rE2DTZJZlLJMss3h9S+5tofkyLOxtwu7rbjGhH16p2J5o1RRajdqrn/M1hzKtpJKgJmvJDuDEMvBx+hrxElkCWTC9/azva5byDn1LOcEf41cePHVMzVF',
        'device': 'browser',
        'isssr': 'false',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sourcetype': 'JobPortal',
        'uniqueID': '',
    }

    json_data = {
        'CarrierLevel': '',
        'Country': '',
        'State': '',
        'Industry': '',
        'JobType': '',
        'PageNumber': 13,
        'PageSize': 10,
        'WorkMode': '',
        'SearchText': '',
        'CDId': 0,
        'PostDays': 0,
        'SortBy': 'Relevance',
        'customtimestamp': 1711611670546,
    }

    response = requests.post(
        'https://livejobslahjobrequest.azurewebsites.net/api/JobSearch/GetAllJobs',
        headers=headers,
        json=json_data,
    )
    print(response)
    # Note: json_data will not be serialized by requests
    # exactly as it was in the original request.
    # data = '{"CarrierLevel":"","Country":"","State":"","Industry":"","JobType":"","PageNumber":13,"PageSize":10,"WorkMode":"","SearchText":"","CDId":0,"PostDays":0,"SortBy":"Relevance","customtimestamp":1711611670546}'
    # response = requests.post('https://livejobslahjobrequest.azurewebsites.net/api/JobSearch/GetAllJobs', headers=headers, data=data)
if __name__ == '__main__':
    while True:
        parse()
