import time
import random
import string
from DrissionPage import ChromiumPage
from DrissionPage import ChromiumPage, ChromiumOptions
# path = '/usr/bin/google-chrome'  # 请改为你电脑内Chrome可执行文件路径
# ChromiumOptions().set_browser_path(path).save()
from DrissionPage.common import Actions
def hk_yzm(keyword):
    co = ChromiumOptions().headless()
    # co = ChromiumOptions().auto_port(True).no_imgs(True).set_argument('--no-sandbox').headless(True)
    page = ChromiumPage(co)
    ac = Actions(page)
    cookies = {'name': 'token',
               'value': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJnbGFkLXVzZXIiLCJpYXQiOjE3MDQ3ODQ2NTcsImV4cCI6MTcxMjU2MDY1NywiaWQiOiIxNzE5NjQ1MzE2OTU1OTgzODc0IiwidXNlckluZm8iOiJ7XCJjcmVEYXRlXCI6XCIyMDIzLTExLTAxVDE3OjE5OjI3XCIsXCJjcmVVc2VyXCI6MCxcInVwZERhdGVcIjpcIjIwMjMtMTEtMDFUMTc6MTk6MjdcIixcInVwZFVzZXJcIjowLFwidXNlckF2YXRhclVybFwiOlwiaHR0cHM6Ly9jZG4ucmVzb3VyY2UueDMxNS5jbi9jbXMvaW1hZ2VzL3d4L3VzZXJQaWMucG5nXCIsXCJ1c2VyQXdhcmRDb3VudFwiOjAsXCJ1c2VySWRcIjoxNzE5NjQ1MzE2OTU1OTgzODc0LFwidXNlckltYWdlXCI6XCJkZWZhdWx0LmpwZ1wiLFwidXNlcktleVwiOlwiU0xaU0FcIixcInVzZXJMb2dpbkNvdW50XCI6NyxcInVzZXJMb2dpbkRhdGVcIjpcIjIwMjQtMDEtMDRUMTA6NDg6MTZcIixcInVzZXJOYW1lXCI6XCIxOTkqKioqOTY0M1wiLFwidXNlck5pY2tOYW1lXCI6XCIqKipcIixcInVzZXJQaG9uZVwiOlwiMTk5MjM3Mjk2NDNcIixcInVzZXJQd2RcIjpcIiQyYSQxMCRmZWVTMmtwZTY1Q1RraTF2aGRSRjV1aEJsM0o4ak1sM0ovS2pqWmw1eHFLbVRERzR1WWF0MlwiLFwidXNlclNvdXJjZVwiOjAsXCJ1c2VyU3RhdHVzXCI6MH0ifQ.2Gsp9ojB94QBsVo9k7TBv5e8uAxOjFQfgcavBAMsayk',
               'domain': '.x315.cn'
               }
    page.set.cookies(cookies)
    url = f'https://www.x315.cn/searchworld/search?keyword={keyword}&countryStr=%E6%96%B0%E5%8A%A0%E5%9D%A1&countryCode=SG'
    page.get(url)
    time.sleep(3)
    # page.refresh()
    # time.sleep(3)
    try:
        ele = page.ele('css:#nc_1_n1z')
        res = ele.attr('aria-label')
        print(res)
        # ac.move_to(ele_or_loc=ele)
        # ac.move(300,0,1)
        ac.hold(ele)
        ac.move(random.randint(400,500),0,random.uniform(2.7,4.9))
        time.sleep(2)
        # ele = page.ele('css:#nc_1_n1z')
        # res = ele.attr('aria-label')
    except Exception as e:
        print(e)
        res = e
    print('验证验证是否通过')
    ele = page.ele('css:#nc_1_n1z')
    res = ele.attr('aria-label')
    page.quit()
    return res
def generate_random_string():
    # 从 a 到 z 生成一个字母列表
    letters = list(string.ascii_lowercase)
    # 随机选择拼接的字母数量，范围为 4 到 6
    length = random.randint(4, 6)
    # 从字母列表中随机选择 length 个字母
    random_letters = random.sample(letters, length)
    # 将随机选取的字母拼接成字符串
    random_string = ''.join(random_letters)
    return random_string


if __name__ == '__main__':
#     cookies = {'name': 'token',
#                'value': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJnbGFkLXVzZXIiLCJpYXQiOjE3MDQ3ODQ2NTcsImV4cCI6MTcxMjU2MDY1NywiaWQiOiIxNzE5NjQ1MzE2OTU1OTgzODc0IiwidXNlckluZm8iOiJ7XCJjcmVEYXRlXCI6XCIyMDIzLTExLTAxVDE3OjE5OjI3XCIsXCJjcmVVc2VyXCI6MCxcInVwZERhdGVcIjpcIjIwMjMtMTEtMDFUMTc6MTk6MjdcIixcInVwZFVzZXJcIjowLFwidXNlckF2YXRhclVybFwiOlwiaHR0cHM6Ly9jZG4ucmVzb3VyY2UueDMxNS5jbi9jbXMvaW1hZ2VzL3d4L3VzZXJQaWMucG5nXCIsXCJ1c2VyQXdhcmRDb3VudFwiOjAsXCJ1c2VySWRcIjoxNzE5NjQ1MzE2OTU1OTgzODc0LFwidXNlckltYWdlXCI6XCJkZWZhdWx0LmpwZ1wiLFwidXNlcktleVwiOlwiU0xaU0FcIixcInVzZXJMb2dpbkNvdW50XCI6NyxcInVzZXJMb2dpbkRhdGVcIjpcIjIwMjQtMDEtMDRUMTA6NDg6MTZcIixcInVzZXJOYW1lXCI6XCIxOTkqKioqOTY0M1wiLFwidXNlck5pY2tOYW1lXCI6XCIqKipcIixcInVzZXJQaG9uZVwiOlwiMTk5MjM3Mjk2NDNcIixcInVzZXJQd2RcIjpcIiQyYSQxMCRmZWVTMmtwZTY1Q1RraTF2aGRSRjV1aEJsM0o4ak1sM0ovS2pqWmw1eHFLbVRERzR1WWF0MlwiLFwidXNlclNvdXJjZVwiOjAsXCJ1c2VyU3RhdHVzXCI6MH0ifQ.2Gsp9ojB94QBsVo9k7TBv5e8uAxOjFQfgcavBAMsayk',
#                'domain': '.x315.cn'
#                }
    # parse()
    keyword= generate_random_string()
    hk_yzm(keyword)


