import re
import datetime
from time import sleep

from settings import MongoDB
import requests
from parsel import Selector
import phonenumbers
def get_list(p):
    params = {
        'limit': '20',
        'page': f'{p}'}
    json_data = {
        'sessionId': '',
        'postingCompany': []}
    try:
        response = requests.post('https://api.mycareersfuture.gov.sg/v2/search', params=params, headers=headers,
                                 json=json_data)
        results = response.json()['results']
    except Exception as e:
        print('list错误')
        print(e)
        return
    for res in results:
        uuid = res['uuid']
        print(uuid)
        get_detail(uuid)


def get_detail(uuid):
    sleep(1)
    params = {
        'updateApplicationCount': 'true',
    }
    try:
        response1 = requests.get(
            f'https://api.mycareersfuture.gov.sg/v2/jobs/{uuid}',
            params=params,
            headers=headers,
        )
        text = response1.json()['description']
    except Exception as e:
        print('detail错误')
        print(e)
        return
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    phone_numbers = extract_phone_numbers3(text)
    phone_numbers = [number for number in list(set(phone_numbers)) if len(number) >= 8]
    emails = email_pattern.findall(text)
    emails = list(set(emails))
    if 'example@email.xyz' in emails:
        emails.remove('example@email.xyz')
    # print(phone_numbers)
    # print(emails)
    email = ','.join(emails) if emails else None
    phone = ','.join(phone_numbers) if phone_numbers else None
    postedCompany = response1.json()['postedCompany']
    name = postedCompany['name']
    uen = postedCompany['uen']
    data = {
        'company':name,'uen':uen,'email':email,'phone':phone,'date':datetime.date.today().strftime("%Y-%m-%d")
    }
    res = mdb.insert_one('m_mycareersfuture',data)
    return print(res)


def extract_phone_numbers(text):
    phone_numbers = []
    for match in phonenumbers.PhoneNumberMatcher(text, "ZZ"):
        phone_numbers.append(phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.INTERNATIONAL))
    return phone_numbers

def extract_phone_numbers1(text):
    # 匹配常见的电话号码格式，例如：1234567890、(123) 456-7890、+123 4567-8901
    phone_pattern = re.compile(r'\b(?:\+\d{1,2}\s?)?\(?\d{3}\)?[-.\s]?\d{3,4}[-.\s]?\d{4}\b')

    # 使用正则表达式在文本中查找匹配的电话号码
    phone_numbers = re.findall(phone_pattern, text)

    return phone_numbers

def extract_phone_numbers2(text):
    # 匹配常见的电话号码格式，包括国际区号、分隔符等
    phone_pattern = re.compile(r'''
        (?:\+\d{1,2}\s?)?          # 匹配国际区号，例如：+1 或 +12
        (?:\(\d{1,4}\)\s?)?        # 匹配带括号的区号，例如：(123) 或 (1234)
        \d{1,4}                    # 匹配区号后的数字部分，最长4位
        [-.\s]?                    # 匹配分隔符，例如：-、. 或空格
        \d{1,4}                    # 匹配主体部分，最长4位
        [-.\s]?                    # 匹配分隔符
        \d{1,4}                    # 匹配尾部部分，最长4位
    ''', re.VERBOSE)

    # 使用正则表达式在文本中查找匹配的电话号码
    phone_numbers = re.findall(phone_pattern, text)

    return phone_numbers

def extract_phone_numbers3(text):
    # 匹配常见的电话号码格式，包括国际区号、分隔符等
    phone_pattern = re.compile(r'''
        (?:\+\d{1,2}\s?)?          # 匹配国际区号，例如：+1 或 +12
        (?:\(\d{1,4}\)\s?)?        # 匹配带括号的区号，例如：(123) 或 (1234)
        \d{1,4}                    # 匹配区号后的数字部分，最多4位
        (?:[-.\s]?\d{1,4})?        # 匹配主体部分，最多4位，包括可选的分隔符
        (?:[-.\s]?\d{1,4})?        # 匹配尾部部分，最多4位，包括可选的分隔符
    ''', re.VERBOSE)

    # 使用正则表达式在文本中查找匹配的电话号码
    phone_numbers = re.findall(phone_pattern, text)

    return phone_numbers

if __name__ == '__main__':
    mdb = MongoDB()
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    page = 415
    # get_detail('76452fbaa6c777b64a49fa697f511af7')
    for p in range(5,page):
        print(f'第{p}页')
        sleep(2)
        get_list(p)
