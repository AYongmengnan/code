import datetime
import sys
import time
import pymysql
import requests
import redis
from urllib.parse import urljoin
from parsel import Selector


def parse_detail(url):
    url_exists = r.sismember('detail_url_is_save', url)
    if url_exists:
        return
    try:
        response = requests.get(url=url,headers=headers,verify=False,timeout=10)
    except Exception as e:
        print('*' * 20)
        print('获取详情错误',e)
        time.sleep(10)
        # return parse_detail(url)
        return
    html = Selector(text=response.text)
    head_dict = {}
    cates = html.xpath('//div[@class="Navigation"]').xpath('string(.)').get()
    head_dict['FACTORY_CATE'] = cates.replace(' ','').replace('当前位置:','') if cates else None
    print(head_dict['FACTORY_CATE'])
    head_dict['CNAME'] = html.xpath('//div[@class="right-name"]/@title').get() # 中文名
    head_dict['BRAND_ID'] = html.xpath('//div[contains(text(),"品牌")]/following-sibling::div/text()').get() # 品牌
    img1 = html.xpath('//div[@class="container-left"]/div[@class="left-right"]/div/img/@src').get()
    head_dict['IMAGELINK1_1'] = urljoin('https://www.solarbio.com/',img1) if img1 else None
    img2 = html.xpath('//div[@class="xgcp-deta"]/a/img/@src').get()
    head_dict['IMAGELINK1_2'] = urljoin('https://www.solarbio.com/',img2) if img2 else None
    download = html.xpath('//div[@class="downLoad"]/div/a/@href').get()
    head_dict['COA'] = urljoin('https://www.solarbio.com/',download) if download else None
    head_dict['TASK_NAME'] = '索莱宝' + datetime.datetime.today().strftime('%Y-%m-%d')
    head_dict['PAGE_LINK'] = url

    sku_ids = html.xpath('//tbody[@class="right-tables"]/tr/td[1]/text()').getall() # 全部货号c
    prices = html.xpath('//select[@id="attr_id"]/option/text()').getall() # 价格/规格
    sku_data = []
    for sku in sku_ids:
        sku = ''.join(sku.split())
        gg1 = sku.split('-')[-1]
        for pri in prices:
            pri = ''.join(pri.split())
            price = pri.split('/')[0].replace('￥','')
            gg2 = pri.split('/')[-1]
            if gg1 == gg2:
                sku_data.append({'SKU_ID':sku,'LIST_PRICE':price,'PACKING_UNIT':gg1})

    # print(sku_data)
    data = html.xpath('//div[@class="relatedDistTop"]/div//tr')
    da_dict = {}
    if data:
        da_dict = {}
        for da in data:
            k = da.xpath('td[1]/text()').get()
            v = da.xpath('td[2]/text()').get()
            if k and v:
                fields = key_data.get(k.strip())
                if fields:
                    da_dict[fields] = v.strip()
    # print(da_dict)
    save_data = []
    if sku_data:
        for sku_da in sku_data:
            end_data = head_dict | sku_da | da_dict
            save_data.append(end_data)
    # else:
    #     save_data.append(head_dict | da_dict)
    # print(save_data)
    # save_sql(save_data)
    if save_data:
        save_sql(save_data)
    r.sadd('detail_url_is_save',url)
    return


def save_sql(data_list):
    try:
        for my_dict in data_list:
            keys_list = list(my_dict.keys())
            values_list = list(my_dict.values())
            sql = f"INSERT INTO pre_items_solarbio ({', '.join(keys_list)}) VALUES ({', '.join(['%s'] * len(values_list))})"
            result = cursor.execute(sql, values_list)
            print('插入结果：',result)
        # all_columns = set().union(*(d.keys() for d in data_list))

        # # 生成 SQL 插入语句
        # sql_inserts = []
        # # for data_dict in data_list:
        # #     # 将每个字典的键值对映射到列和值
        # #     columns = ', '.join(all_columns)
        # #     placeholders = ', '.join(['%s'] * len(all_columns))
        # #     values = [data_dict.get(column, '') for column in all_columns]
        # #     sql_insert = f"INSERT INTO pre_items_solarbio ({columns}) VALUES ({placeholders});"
        # for data_dict in data_list:
        #     # 将每个字典的键值对映射到列和值
        #     columns = ', '.join(all_columns)
        #     values = ', '.join(f"'{data_dict.get(column, '')}'" for column in all_columns)

        #     # 生成 SQL 插入语句
        #     sql_insert = f"INSERT INTO pre_items_solarbio ({columns}) VALUES ({values});"
        #     sql_inserts.append(sql_insert)
        #     # 执行 SQL 插入语句
        # for sql_insert in sql_inserts:
        #     result = cursor.execute(sql_insert)
        #     print('插入结果：',result)
        # 提交事务
        db.commit()
    except Exception as e:
        print(e)
    # finally:
    #     # 关闭游标和连接
    #     cursor.close()
    #     # db.close()
    return

if __name__ == "__main__":
    db = pymysql.connect(
        host="47.102.145.175",
        user="user_momobei",
        password="ad5kf2d9sd!r3#e",
        database="momobei",
        port=3306,
    )
    cursor = db.cursor()
    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }
    key_data = {
                '序列号': 'SEQ_NUM',
                '任务号': 'TASK_NAME',
                '货号': 'SKU_ID',
                'CAS': 'CAS_ID',
                '品牌ID': 'BRAND_ID',
                '厂家类目': 'FACTORY_CATE',
                '中文名称': 'CNAME',
                '英文名称': 'ENAME',
                '中文别名': 'CALIAS',
                '英文别名': 'EALIAS',
                '目录价格': 'LIST_PRICE',
                '规格总计': 'PACKING_TOTAL',
                '规格数量': 'PACKING_NUM',
                '规格单位': 'PACKING_UNIT',
                '纯度规格': 'PURITY',
                '纯度': 'PURITY',
                '库存类型': 'STORAGE_TYPE',
                '发货时效': 'DELIVER_DURATION',
                'MSDS': 'MSDS',
                '规格说明书': 'COA',
                '厂家商品页链接': 'PAGE_LINK',
                '运输类型': 'SHIPPING_TYPE',
                '分子式': 'Mole_Formula',
                '结构式': 'Stru_Formula',
                '分子量': 'Mole_Weight',
                '熔点': 'MP',
                '沸点': 'BP',
                '密度': 'Density',
                '储存条件': 'Storage',
                'MDL号': 'MDL',
                'PubChem_CID': 'PubChem_CID',
                'Beilstein编号': 'Beilstein',
                'EINECS编号': 'EINECS',
                'IUPAC_Name': 'IUPAC_Name',
                'INCHI': 'INCHI',
                'Inchi_Key': 'Inchi_Key',
                'MDL': 'MDL',
                'PubChem': 'PubChem_CID',
                'Beilstein': 'Beilstein',
                'EINECS': 'EINECS',
                'IUPAC': 'IUPAC_Name',
                '危化品等级': 'DANGE_CLASS',
                '是否危化品': 'IS_SAFETY',
                '图片链接1': 'IMAGELINK1_1',
                '图片链接2': 'IMAGELINK1_2',
                '图片链接3': 'IMAGELINK1_3'
            }

    redis_url = "redis://:zhanglin@127.0.0.1:6379/10"
    r = redis.StrictRedis.from_url(redis_url, decode_responses=True)
    # data_set = set()
    # categore_list = get_categore()
    # for categore in categore_list:
    #     url = urljoin('https://www.solarbio.com/',categore)
    #     detail_urls = parse_list(url)
    #     for d_u in detail_urls:
    #         d_url = urljoin('https://www.solarbio.com/',d_u)
    #         parse_detail(d_url)
    # get_categore()
    list_urls = r.smembers('detail_url')
    for d_url in list_urls:
        print(d_url)
        parse_detail(d_url)
    # parse_detail('https://www.solarbio.com/goods-46771.html')