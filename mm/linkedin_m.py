import time

import requests
def parse_list():
    # 获取工作列表页
    cookies = {
        'JSESSIONID': 'ajax:4583201108015297503',
        'li_at': 'AQEDAUvMiPgBFwoUAAABjcqmi-0AAAGO39J2qk4AcaYmosCxy5gHzrpd6elapq3U7JHryleLNqurJmZvUzgg4wg5AFKN7JkF45cIPMixIMYmRXOC4JReA9cM5ZmMpTr2hiuTCf8F-3WxOKfo3UAhhaO3',
        }

    headers = {
        'csrf-token': 'ajax:4583201108015297503',
        'referer': 'https://www.linkedin.com/',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    }

    response = requests.get(
        'https://www.linkedin.com/voyager/api/voyagerJobsDashJobCards?decorationId=com.linkedin.voyager.dash.deco.jobs.search.JobSearchCardsCollection-203&count=25&q=jobSearch&query=(origin:JOB_SEARCH_PAGE_JOB_FILTER,locationUnion:(geoId:101355337),selectedFilters:(timePostedRange:List(r86400),workplaceType:List(1)),spellCorrectionEnabled:true)&start=25',
        # 'https://www.linkedin.com/voyager/api/voyagerJobsDashJobCards?decorationId=com.linkedin.voyager.dash.deco.jobs.search.JobSearchCardsCollection-199&count=100&q=jobSearch&query=(origin:JOB_SEARCH_PAGE_JOB_FILTER,selectedFilters:(workplaceType:List(2)),spellCorrectionEnabled:true)&start=0',
        cookies=cookies,
        headers=headers,
    )
    if response.status_code != 200:
        return print('获取工作list失败')
    data = response.json()
    print(response.text)
    data = data['elements']
    for da in data:
        preDashNormalizedJobPostingUrn = da['jobCardUnion']['jobPostingCard']['preDashNormalizedJobPostingUrn']
        job_id = preDashNormalizedJobPostingUrn.split(":")[-1]
        try:
            company_linkedin_url = da['jobCardUnion']['jobPostingCard']['logo']['actionTarget'].replace('/life', '')
        except:
            company_linkedin_url = None
        print(job_id,company_linkedin_url)
        # parse_recruiter(job_id)

def parse_recruiter(job_id):
    cookies = {
        'JSESSIONID': '"ajax:4583201108015297503"',
        'li_at': 'AQEDAUvMiPgBFwoUAAABjcqmi-0AAAGOp7LFuE4AAhjUAXQNtvyWg_Gbc6UqLWFNXLg7jnCyOuZyfnVjrr3d9Sn9K01SaQAh4lnmCc7nUIZ2MCy3ZvS8DsIRXWFEaWCiLrqYN1UtuLNM_6N9av8iffe8',
        }

    headers = {
        'csrf-token': 'ajax:4583201108015297503',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        }

    response = requests.get(
        f'https://www.linkedin.com/voyager/api/graphql?variables=(cardSectionTypes:List(HIRING_TEAM_CARD),jobPostingUrn:urn%3Ali%3Afsd_jobPosting%3A{job_id},includeSecondaryActionsV2:true)&queryId=voyagerJobsDashJobPostingDetailSections.0a2eefbfd33e3ff566b3fbe31312c8ed',
        cookies=cookies,
        headers=headers,
    )
    data = response.json()
    try:
        name = data['data']["jobsDashJobPostingDetailSectionsByCardSectionTypes"]["elements"][0]["jobPostingDetailSection"][0]["hiringTeamCard"]["title"]["text"]
        contact_url = data["data"]["jobsDashJobPostingDetailSectionsByCardSectionTypes"]["elements"][0]["jobPostingDetailSection"][0]["hiringTeamCard"]["navigationUrl"]
    except:
        # print(e)
        name,contact_url = None,None
    print(name,contact_url)
    # parse_apollo_contact(name,contact_url)

def parse_apollo_contact(name,contact_url):
    _t = int(time.time() * 1000)
    url = 'https://app.apollo.io/api/v1/linkedin_chrome_extension/parse_profile_page'
    if contact_url:
        params = {
            "url": contact_url,
            "html": f"<section class=\"artdeco-card \" data-member-id=\"\"><h1 class=\"text-heading-xlarge \">{name}</h1></section><section class=\"artdeco-card \"  data-view-name=\"profile-card\"><div id=\"experience\" class=\"pv-profile-card__anchor\"> </div><div class=\"pvs-list__outer-container\"><ul class=\"pvs-list \"><li class=\"artdeco-list__item \"><div data-view-name=\"profile-component-entity\"></div></li></ul></div></section>",
            "cacheKey": _t
        }
        cookies = {
            'remember_token_leadgenie_v2': 'eyJfcmFpbHMiOnsibWVzc2FnZSI6IklqWTBPR0ZqTVRrelltWmtaamd6TURCa1lqRTNPRFF5WlY4d1l6TmtaRGcyT1dFelpqTmlaR1U1Tm1FNU5EZzNZV1E1WXpGbU1qWTROaUk9IiwiZXhwIjoiMjAyNC0wNS0wOVQwOToxNDoxMi4wNDVaIiwicHVyIjoiY29va2llLnJlbWVtYmVyX3Rva2VuX2xlYWRnZW5pZV92MiJ9fQ%3D%3D--9d12ed3688f0a0e1db700fde4775b0b5f347cd7e',
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            'Content-Type': 'application/json',
            'origin': 'chrome-extension://alhgpfoeiimagjlnfekdhkjlkiomcapa',
        }
        try:
            response = requests.post(url=url,
                                     json=params,
                                     headers=headers,
                                     cookies=cookies
                                     )
        except Exception as e:
            print(e)
            return
        person_id = response.json()['contact']['person_id']
        print(person_id)
        url = 'https://app.apollo.io/api/v1/contacts'
        params = {
            "person_id": person_id,
            "source": "chrome_extension_linkedin",
            "email_true_status": "Unavailable",
            "updated_email_true_status": True,
        }
        try:
            response2 = requests.post(url=url, headers=headers, cookies=cookies, json=params)
        except Exception as e:
            print(e)
            return
        print(response2.json())
        # people_name = response2.json()['contact']['name']
        # people_title = response2.json()['contact']['title']
        # people_company_email = response2.json()['contact']['email']
        # try:
        #     company_phone = response2.json()['contact']['phone_numbers'][0]['raw_number']
        #     if company_phone:
        #         pass
        #     else:
        #         company_phone = response2.json()['contact']['sanitized_phone']
        # except Exception as e:
        #     company_phone = response2.json()['contact']['sanitized_phone']
        # try:
        #     people_contact_email = response2.json()['contact']['contact_emails'][0]['email']
        # except Exception as e:
        #     pass


if __name__ == '__main__':
    parse_list()
    # parse_recruiter('3846205134')
    # parse_apollo_contact('Mayra Gonzalez','https://www.linkedin.com/in/mayra-gonzalez-mshr-719361225/')