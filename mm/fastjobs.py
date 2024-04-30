import re
import time

from settings import MongoDB
# import requests
from parsel import Selector
import cloudscraper
def get_list(page):
    headers = {
        "authority": "www.fastjobs.sg",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "referer": "https://www.fastjobs.sg/singapore-jobs/en/all-categories-jobs/page-",
        "sec-ch-ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"macOS\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    cookies = {
        "_csrf": "c442ffdcebd35199cdefc53937267f49d65c904b3e56ec698a5f848c023f522ba%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22-m2Gd-bbgHKgi7xYarc6MxG1yDP3ZSca%22%3B%7D",
        "gr_reco": "18dab89613f-bfad6f19212b1d21",
        "jobsTmstamp": "fbca58beea274a78a404be66a7d24f9ae3523b6cee521c282e098a3a650d4082a%3A2%3A%7Bi%3A0%3Bs%3A11%3A%22jobsTmstamp%22%3Bi%3A1%3Bi%3A1708502699%3B%7D"
    }
    response = requests.get(
        f'https://www.fastjobs.sg/singapore-jobs/en/all-categories-jobs/page-{page}/',
        # cookies=cookies,
        headers=headers,
    )
    if response.status_code == 202:
        print('等待180s')
        time.sleep(180)
        return get_list(page)
    text = Selector(text=response.text)
    url_list = text.xpath('//div[@id="jobslist"]/a')
    for u in url_list:
        name = u.xpath('div[contains(@class,"job-post")]//span[@class="visible-xs"]/strong/text()').get()
        url = u.xpath('@href').get()
        get_detail(name,url)
    # for url in url_list:
    #     # print(url)
    #     get_detail(url)
    return


def get_detail(name,url):
    print(name,url)
    headers = {
        "authority": "www.fastjobs.sg",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "referer": "https://www.fastjobs.sg/singapore-job-ad/1970853/contract-accounts-executive-near-tai/tempteam-pte-ltd/?offset=23&source=web-jobfeed",
        "sec-ch-ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"macOS\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    cookies = {
        "_csrf": "c442ffdcebd35199cdefc53937267f49d65c904b3e56ec698a5f848c023f522ba%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22-m2Gd-bbgHKgi7xYarc6MxG1yDP3ZSca%22%3B%7D",
        "gr_reco": "18dab89613f-bfad6f19212b1d21",
        "jobsTmstamp": "fbca58beea274a78a404be66a7d24f9ae3523b6cee521c282e098a3a650d4082a%3A2%3A%7Bi%3A0%3Bs%3A11%3A%22jobsTmstamp%22%3Bi%3A1%3Bi%3A1708502699%3B%7D",
        "ck-st": "e186c56244ca1cdd8e067856b26ebc714d86cd3aac192e4c728053108b221b4da%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22ck-st%22%3Bi%3A1%3Bs%3A2%3A%22en%22%3B%7D",
        "aws-waf-token": "85531e96-962b-4e39-aece-f44110970739:AQoAvIw3weiWAAAA:ldUGc9EtfKDPI/IiCPinL+aqFmG7cSZQ9MRMPSSI92oiB4BnLm2XXpW1XvFBW8K2T8thrB77GLYyrJDRomoLEdBTB3HMVLWFqFI/80wblcjTMwZvGl2bTuoL8SiZKnTt8sbmB/LEXwtMaNeTScIFV3F61JVgRs8dH6FnisYeTEIf/zXUq4WqNN5WoJbNtTqMOnVGxGtvphi4wpXwIhZJ16dhyTMMQBTyv3mWMl8f1GeZgv+iLXtZRQ=="
    }
    response = requests.get(url,headers=headers,
                            # cookies=cookies
                            )
    if response.status_code == 202:
        print('等待180s')
        time.sleep(180)
        return get_detail(name,url)
    text = Selector(text=response.text)
    content = text.xpath('//div[@class="job-desc rtf-content"]').xpath('string(.)').get()
    # print(content)
    phone_pattern = r'\b(?:\+65\s*[\d\-]+|65\s*[\d\-]+|6\d{7}|8\d{7}|9\d{7})\b'
    singapore_phones = re.findall(phone_pattern, content)
    phone = ','.join(singapore_phones)
    # print(singapore_phones)
    telegram_pattern = r'(?<!\w)@[\w\d_]+'
    telegram_contacts = re.findall(telegram_pattern, content)
    telegram = ','.join(telegram_contacts)
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    emails = re.findall(email_pattern, content)
    email = ','.join(emails)
    print(name,singapore_phones,telegram_contacts,emails)
    res = mdb.insert_one('email_fastjobs',{'name':name,'email':email,'phones':phone,'telegram':telegram})
    print(res)


if __name__ == '__main__':
    mdb = MongoDB()
    requests = cloudscraper.create_scraper()
    # get_list(1)
    # get_detail('hh','https://www.fastjobs.sg/singapore-job-ad/1964260/bartender-fulltimeparttime-immediate-vacancy/fourgather-pte-ltd/')
    for p in range(1,285):
        get_list(p)