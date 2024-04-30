import time
from urllib.parse import urljoin
from parsel import Selector
import requests
import re
import redis

def get_categore():
    url = 'https://www.solarbio.com/index.php'
    
    response = requests.get(url=url,headers=headers)
    html = Selector(text=response.text)
    categore_list = html.xpath('//div[@id="listLay"]/div/div[@class="navOpen"]/a/@href').getall()
    # return categore_list
    for categore in categore_list:
        url = urljoin('https://www.solarbio.com/',categore)
        get_list(url)
    return
def get_list(url):
    response = requests.get(url=url,headers=headers)
    html = Selector(text=response.text)
    end = html.xpath('//a[@class="last"]/@href').get()
    # print(end)
    if end:
        # end_url = urljoin('https://www.solarbio.com/',end)
        # return get_list_url(end_url)
        pass
    else:
        detail_u = html.xpath('//div[@class="content_right_product"]/div/div[@class="content_right_product_name"]/div[@class="content_right_product_name_num"]/a/@href').getall()
        detail_url_list = []
        for d_u in detail_u:
            detail_url = urljoin('https://www.solarbio.com/',d_u)
            detail_url_list.append(detail_url)
        return r.sadd('detail_url',*detail_url_list)

def get_list_url(url):
    print(url)
    # url = 'category-13-b0-min0-max0-attr0-157-sort_order-DESC.html'
    # 使用正则表达式提取页数
    page_number_match = re.findall(r'attr0-(.*?)-sort_order-DESC.html', url)
    if page_number_match:
        page_number = int(page_number_match[0])
        # 生成所有页码的 URL
        page_urls = [re.sub(r'attr0-(.*?)-sort_order-DESC.html', f'attr0-{page}-sort_order-DESC.html', url) for page in range(1, page_number + 1)]
        r.sadd('list_url',*page_urls)

        # 打印结果
        # print(f'Total Pages: {page_number}')
        # print('Page URLs:')
        # for page_url in page_urls:
        #     print(page_url)
    else:
        print('Page number not found in the URL.')
    return

def get_detail_url():
    list_urls = r.smembers('list_url')
    print(len(list_urls),type(list_urls))
    for li_url in list_urls:
        print(li_url)
        url_exists = r.sismember('list_url_is_save', li_url)
        # print(url_exists)
        if url_exists == 0:
            time.sleep(2)
            response = requests.get(url=li_url,verify=False,timeout=10)
            print('响应状态',response.status_code)
            html = Selector(text=response.text)
            detail_urls = html.xpath('//div[@class="content_right_product"]/div/div[@class="content_right_product_name"]/div[@class="content_right_product_name_num"]/a/@href').getall()
            print(detail_urls)
            detail_url_list = []
            for d_u in detail_urls:
                d_url = urljoin('https://www.solarbio.com/',d_u)
                detail_url_list.append(d_url)
            res = r.sadd('detail_url',*detail_url_list)
            print(res)
            r.sadd('list_url_is_save',li_url)
    return
if __name__ == "__main__":
    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }
    redis_url = "redis://:zhanglin@127.0.0.1:6379/10"
    r = redis.StrictRedis.from_url(redis_url, decode_responses=True)
    # get_categore()
    # get_detail_url()
    get_categore()

 