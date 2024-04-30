import datetime
import pymysql
import requests
import redis
from urllib.parse import urljoin
from parsel import Selector
def get_categore():
    url = 'https://www.solarbio.com/index.php'
    
    response = requests.get(url=url,headers=headers)
    html = Selector(text=response.text)
    categore_list = html.xpath('//div[@id="listLay"]/div/div[@class="navOpen"]/a/@href').getall()
    # return categore_list
    for categore in categore_list:
        url = urljoin('https://www.solarbio.com/',categore)
        parse_list(url)
    return

def parse_list(url):
    print(url)
    url_exists = r.sismember('list_url', url)
    if url_exists == 0:
        response = requests.get(url=url,headers=headers)
        html = Selector(text=response.text)
        # if url_exists == 0:
        detail_urls = html.xpath('//div[@class="content_right_product"]/div/div[@class="content_right_product_name"]/div[@class="content_right_product_name_num"]/a/@href').getall()
        for d_u in detail_urls:
            d_url = urljoin('https://www.solarbio.com/',d_u)
            res = r.sadd('url',d_url)
            print(res)
        res = r.sadd('list_url',url)
        next_page = html.xpath('//a[@class="next"]/@href').get()
        if next_page:
            next_url = urljoin('https://www.solarbio.com/',next_page)
            return parse_list(next_url)
    return 

    

if __name__ == "__main__":
    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }
    
    redis_url = "redis://:zhanglin@127.0.0.1:6379/10"
    r = redis.StrictRedis.from_url(redis_url, decode_responses=True)
    get_categore()