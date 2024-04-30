import time
import datetime

from settings import MongoDB
import requests
from parsel import Selector

def parse(page):
    _t = int(time.time() * 100)
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
        'X-CSRF-Token': '816iHR68SUl0TSv8JAawg0u5KTj04NRCFNRl8JdpTTHRs82noU+TBoOHESWKrbuFfIJ17s8qvOGfOatwafdMqyff+6W9qrIxP/fMG8zk51+pPo4sFbw5USXHzVFJGMCH1mggEwp4PQ85M6Ee0Zf49MquOpRT9ugQSHnLOpITu8LBhxCqdUQrHihDjOGit7FsbwsUZS6Jo6I9XPxEJQK6m0Us0/a21CUBSQQHuYM7pqub7D3BC6D526OHrI3NywJP',
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
        'Country': '199',
        'State': '',
        'Industry': '',
        'JobType': '',
        'PageNumber': page,
        'PageSize': 10,
        'WorkMode': '',
        'SearchText': '',
        'CDId': 0,
        'PostDays': 0,
        'SortBy': 'Relevance',
        'customtimestamp': _t,
    }
    try:
        response = requests.post(
            'https://livejobslahjobrequest.azurewebsites.net/api/JobSearch/GetAllJobs',
            headers=headers,
            json=json_data,
        )
        response = response.json()
    except Exception as e:
        print(e)
        return parse(page)
    Data = response.get('StatusObject',{}).get('Data')
    for da in Data:
        # print(da)
        CDId = da.get('CDId')
        parse_detail(CDId)
    return
    # print(response.text)
    # print(response)


def parse_detail(CDId):
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
        'X-CSRF-Token': 'df8EF3sU6TfIo+K5c+1EmstAaJRbWkwWLLIl8iLhAxYcp3VcNiUbNcXSlX6wMToNh63tVY03sX5M/sCkkLVrTBWOd86fTWR4ek74rAdJcWbw/3YErjU9fhdKphvaFojKrptq5VY1H9LRtzYbvlQ19f+wYhdw+QiZ96BQ2xNE/CeaoT6R/ekVEgt67GLXdBDNN6zErqGDykBCPeCwmQ7OSAnWqYbRk3fxhm7P7PGAPi+TlD3CCY97rZSgYfXlATF8',
        'device': 'browser',
        'isssr': 'false',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sourcetype': 'JobPortal',
        'uniqueID': '',
    }

    json_data = {
        'CDID': CDId,
        'RLID': 0,
        'Flag': 'WithoutPaths',
        'customtimestamp': int(time.time() * 100),
    }
    try:
        response = requests.post(
            'https://livejobslahauthguard.azurewebsites.net/api/CompanyProfile/GetCompanyProfile',
            headers=headers,
            json=json_data,
        )
        # print(response.text)
        # print(response)
        data = response.json().get('StatusObject')
    except Exception as e:
        print(e)
        return parse_detail(CDId)
    name = data.get('Name')
    phone = data.get('ContactNo')
    email = data.get('Email')
    website = data.get('WebSite')
    logo = data.get('LogoData')
    address = data.get('Address')
    industry = data.get('Industry')
    companysize = data.get('CompanySize')
    Benefits = data.get('Benefits')
    if Benefits:
        Benefits = Selector(text=Benefits)
        benefits = Benefits.xpath('string(.)').get()
    else:
        benefits = None

    save_data = {
        'name':name,
        'phone':phone,
        'email':email,
        'website':website,
        'logo':logo,
        'address':address,
        'industry':industry,
        'companysize':companysize,
        'benefits':benefits,
        'date': datetime.date.today().strftime("%Y-%m-%d")
    }
    print(save_data)
    return mdb.insert_one('jobslah_sg',save_data)




if __name__ == '__main__':
    mdb = MongoDB()
    for page in range(11,15):
        print(f'第{page}页')
        parse(page)
    # parse_detail(881)
    # parse(1)