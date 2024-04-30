from datetime import datetime
from re import findall
from copy import deepcopy
from requests import get, post, session
from time import time
from settings import MongoDB

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://www.linkedin.com/',
    'csrf-token': 'ajax:0915331479475711581'
}

headers2 = {
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Origin': 'chrome-extension://alhgpfoeiimagjlnfekdhkjlkiomcapa'
}

cookies = {
    'li_at': 'AQEDAUT5fJIF87mAAAABjengeR0AAAGODez9HVYAbgTlJljhtfF8YEuD_a9JIE6wBe3UZSeUV8ZWbEk3rC-I8T1cEEdyPKFgWfpugmZbbqszzxi9QFPlhnJCUu8bmXLnBDlErjqkuRR5lgywELQ9H19I',
    'JSESSIONID': '"ajax:0915331479475711581"',
}

cookies2 = {
    'remember_token_leadgenie_v2': 'eyJfcmFpbHMiOnsibWVzc2FnZSI6IklqWTFOalppTWpsak5qQmpOVFF4TURCaE16ZGtNekZsWVY4eE1XWXhNMlF5TWpFek4yVmxaVFE0TkRsaE16QXlOelJsWVRkbVptRm1OU0k9IiwiZXhwIjoiMjAyNC0wMy0xOFQwMjo0MjowNC43MzNaIiwicHVyIjoiY29va2llLnJlbWVtYmVyX3Rva2VuX2xlYWRnZW5pZV92MiJ9fQ%3D%3D--b706ffc66f9db6b6dd093553f1a6d4c2ed9ef736'
}

proxies = {
    'http': 'http://brd-customer-hl_ed3b84ed-zone-lin2:m199wtih9gt6@brd.superproxy.io:22225',
    'https': 'http://brd-customer-hl_ed3b84ed-zone-lin2:m199wtih9gt6@brd.superproxy.io:22225'
}

md = MongoDB()
session = session()
session.headers = headers
session.cookies.update(cookies)

# 获取当前时间
current_time = datetime.now()
time1 = current_time.strftime('%Y-%m-%d')
data_dict = {
    'job_id': '',
    'job_title': '',
    'job_url': '',
    'job_post_time': time1,
    'jog_address': '',
    'people_name': '',
    'people_title': '',
    'people_id': '',
    'people_linkedin_url': '',
    'people_company_email': '',
    'people_contact_email': '',
    'company_name': '',
    'company_phone': '',
    'company_id': '',
    'company_linkedin_url': ''
}


def get_lists():
    # url = "https://www.linkedin.com/voyager/api/voyagerJobsDashJobCards?decorationId=com.linkedin.voyager.dash.deco.jobs.search.JobSearchCardsCollectionLite-62&count=100&q=jobSearch&query=(origin:JOB_SEARCH_PAGE_JOB_FILTER,locationUnion:(geoId:102890883),selectedFilters:(timePostedRange:List(r86400),workplaceType:List(2)),spellCorrectionEnabled:true)&servedEventEnabled=false&start=0"
    url = "https://www.linkedin.com/voyager/api/voyagerJobsDashJobCards?decorationId=com.linkedin.voyager.dash.deco.jobs.search.JobSearchCardsCollection-195&count=25&q=jobSearch&query=(origin:JOB_SEARCH_PAGE_JOB_FILTER,locationUnion:(geoId:106808692),selectedFilters:(workplaceType:List(2)),spellCorrectionEnabled:true)&start=0"
    response = session.get(url=url)
    print('获取工作列表完成')
    with open('./data/linkedin/1.json', 'w', encoding='utf-8') as file:
        file.write(response.text)
    datas = []
    for i in response.json()['elements']:
        dict_1 = deepcopy(data_dict)
        job_id = findall('\d+', i['jobCardUnion']['jobPostingCard']['jobPostingUrn'])[0]
        try:
            company_linkedin_url = i['jobCardUnion']['jobPostingCard']['logo']['actionTarget'].replace('/life', '')
        except Exception as e:
            company_linkedin_url = None
        job_title = i['jobCardUnion']['jobPostingCard']['jobPostingTitle']
        job_url = 'https://www.linkedin.com/jobs/view/' + job_id
        company_name = i['jobCardUnion']['jobPostingCard']['primaryDescription']['text']
        jog_address = i['jobCardUnion']['jobPostingCard']['secondaryDescription']['text']
        dict_1['job_id'] = job_id
        dict_1['job_title'] = job_title
        dict_1['jog_address'] = jog_address
        dict_1['job_url'] = job_url
        dict_1['company_name'] = company_name
        dict_1['company_linkedin_url'] = company_linkedin_url
        datas.append(dict_1)
    return datas


def get_datas(datas):
    for i in datas:
        people_url, people_name = get_people(i['job_id'])
        if people_url:
            print('有招聘人员信息')
            url = 'https://app.apollo.io/api/v1/linkedin_chrome_extension/parse_profile_page'
            params = {
                "url": people_url,
                "html": f"""<section  data-member-id/> <h1 class=text-heading-xlarge>{people_name}</h1><div id=experience></div> <div class=pvs-list__outer-container> <div class=pvs-entity--padded>""",
                "cacheKey": time()
            }
            try:
                response = post(url=url, headers=headers2, cookies=cookies2, json=params)
            except:
                response = post(url=url, headers=headers2, cookies=cookies2, json=params)
            i['people_id'] = response.json()['contact']['person_id']
            url = 'https://app.apollo.io/api/v1/contacts'
            params = {
                "person_id": i['people_id'],
                "source": "chrome_extension_linkedin",
                "email_true_status": "Unavailable",
                "updated_email_true_status": True,
            }
            try:
                response2 = post(url=url, headers=headers2, cookies=cookies2, json=params)
            except:
                response2 = post(url=url, headers=headers2, cookies=cookies2, json=params)

            i['people_linkedin_url'] = people_url
            i['people_name'] = response2.json()['contact']['name']
            i['people_title'] = response2.json()['contact']['title']
            i['people_company_email'] = response2.json()['contact']['email']
            try:
                i['company_phone'] = response2.json()['contact']['phone_numbers'][0]['raw_number']
                if i['company_phone']:
                    pass
                else:
                    i['company_phone'] = response2.json()['contact']['sanitized_phone']
            except Exception as e:
                i['company_phone'] = response2.json()['contact']['sanitized_phone']
            try:
                i['people_contact_email'] = response2.json()['contact']['contact_emails'][0]['email']
            except Exception as e:
                pass
            md.insert_one('remote_apollo_jobs', i)
            print()
            continue
        print('没有招聘人员信息, 从网上搜索中')
        if i['company_linkedin_url']:
            url = 'https://app.apollo.io/api/v1/linkedin_chrome_extension/parse_company_page'
            params = {
                "url": i['company_linkedin_url'],
                "html": f"""
                    <div class=\"org-top-card__primary-content org-top-card-primary-content--zero-height-logo
                         org-top-card__improved-primary-content--ia\">
                    <h1 id=\"ember28\" class=\"ember-view org-top-card-summary__title text-display-medium-bold
                        full-width\" title=\"{i['company_name']}\">{i['company_name']}
                    </h1>
                    </div>
                """,
                "cacheKey": time()
            }
            try:
                response = post(url=url, headers=headers2, cookies=cookies2, json=params)
            except:
                response = post(url=url, headers=headers2, cookies=cookies2, json=params, proxies=proxies)
            try:
                data_json = response.json()['organization']
            except:
                print('。。。。。。')
                continue
            i['company_phone'] = data_json['phone']
            md.insert_one('remote_apollo_companies', data_json)
        print()
        md.insert_one('remote_apollo_jobs', i)


def get_people(job_id):
    url = f"https://www.linkedin.com/voyager/api/graphql?variables=(cardSectionTypes:List(HIRING_TEAM_CARD),jobPostingUrn:urn%3Ali%3Afsd_jobPosting%3A{job_id},includeSecondaryActionsV2:true)&queryId=voyagerJobsDashJobPostingDetailSections.baf7357904fcbe463380decd22a03604"
    try:
        response = session.get(url=url, headers=headers2, cookies=cookies2)
    except:
        response = session.get(url=url, headers=headers2, cookies=cookies2)
    with open('./data/linkedin/3.json', 'w', encoding='utf-8') as file:
        file.write(response.text)
    try:
        people_url = response.json()['data']['jobsDashJobPostingDetailSectionsByCardSectionTypes']['elements'][0][
            'jobPostingDetailSection'][0]['hiringTeamCard']['navigationUrl']
        people_name = response.json()['data']['jobsDashJobPostingDetailSectionsByCardSectionTypes']['elements'][0][
            'jobPostingDetailSection'][0]['hiringTeamCard']['title']['text']
        return people_url, people_name
    except Exception as e:
        return False, False


def main():
    datas = get_lists()
    get_datas(datas)
    with open('./data/linkedin/2.json', 'w', encoding='utf-8') as file:
        file.write(str(datas))


if __name__ == '__main__':
    main()
