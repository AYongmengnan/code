from settings import MongoDB
import datetime
from urllib.parse import urljoin
import requests
from parsel import Selector
import re

def parse():
    headers = {
        'content-type': 'application/json',
        'origin': 'https://www.ease.jobs',
        'referer': 'https://www.ease.jobs/',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    }

    json_data = {
        'pageNumber': 1,
        'pageSize': 1000,
        'jobPostingSortOrder': 1,
    }
    response = requests.post('https://api.ease.jobs/api/JobPosting/JobPostings', headers=headers, json=json_data)

    # print(response.text)
    print(response)
    data = response.json()
    result = data.get('result')
    if result:
        for res in result:
            company = res.get('company',{})
            companyName = company.get('companyName')
            jobPostingId = res.get('jobPostingId')
            url = urljoin('https://www.ease.jobs/jobs/',jobPostingId)
            jobDesc = res.get('jobDesc')
            jobRequirements = res.get('jobRequirements')
            contacts = extract_text(jobDesc,jobRequirements)
            if contacts:
                save_data = {
                    'name':companyName,
                    "phones": ','.join(contacts.get('phone_numbers')),
                    "emails": ','.join(contacts.get('emails')),
                    "telegrams": ','.join(contacts.get('telegram_usernames')),
                    "whatsapps": ','.join(contacts.get('whatsapp_numbers')),
                    'url':url,
                    'date':datetime.datetime.now().strftime("%Y-%m-%d")
                }
                print(save_data)
                print('*' * 50)
                res = mdb.insert_one('ease',save_data)
                print(res)
    return

def extract_text(desc,requirements):
    desc_ = Selector(text=desc)
    requirements_ = Selector(text=requirements)
    desc_text = desc_.xpath('string(.)').get()
    requirements_text = requirements_.xpath('string(.)').get()
    text = desc_text + ' ' + requirements_text
    # return text
    if text:
        return extract_contacts(text)
    return
    

def extract_contacts(text):
    # 匹配电话号码的正则表达式
    # phone_pattern = r'\b(?:\+?65\s*[\d\-]+|6\d{7}|8\d{7}|9\d{7}|\d{4}[\s\-]?\d{4}|\d{8}|\d{4}\^\d{4}|\d{4}\*\d{4}|\+\d{6,10})\b'
    phone_pattern = r'\b(?:\+?65\s*\d{4}\s*\d{4}|\+?65\s*\d{8}|6\d{7}|8\d{7}|9\d{7})\b'
    # 匹配电子邮件地址的正则表达式
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    # 匹配Telegram的正则表达式
    telegram_pattern =  r'(?<!\w)@[\w\d_]+'

    # 匹配WhatsApp的正则表达式
    whatsapp_pattern = r'Wa\.me\/(\d+)'

    # 查找匹配的电话号码
    phone_numbers = re.findall(phone_pattern, text)

    # 查找匹配的电子邮件地址
    emails = re.findall(email_pattern, text)

    # 查找匹配的Telegram用户名
    telegram_usernames = re.findall(telegram_pattern, text)

    # 查找匹配的WhatsApp号码
    whatsapp_numbers = re.findall(whatsapp_pattern, text)
    if phone_numbers or emails or telegram_usernames or whatsapp_numbers:
        return {
            "phone_numbers": phone_numbers,
            "emails": emails,
            "telegram_usernames": telegram_usernames,
            "whatsapp_numbers": whatsapp_numbers
        }
    return
if __name__ == '__main__':
    mdb = MongoDB()
    parse()
#     desc = """<p>Support in HR admin duties, Data entry, other duties as assigned</p>
# <p>&nbsp;</p>
# <p>Interested applicants may email resume to cheryl.lee@recruitexpress.com.sg</p>
# <p>Cheryl Lee Shi Le (CEI Registration No: R1434624)<br>Recruit Express Pte Ltd (EA: 99C4599)</p>"""
#     req = "<p>able to commit long tmer</p>"
#     text = extract_text(desc,req)
#     print(text)
