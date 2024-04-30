import csv

import pymongo

from settings import MongoDB
import requests
from parsel import Selector


def get_data(collection):
    data = list(mdb.find(collection,{},{'_id':0}).limit(7000).sort("name", pymongo.ASCENDING))
    print(len(data))
    email_phone_list = []
    no_list = []
    for da in data:
        email = da.get('email')
        phone = da.get('phone')
        # print(email)
        # print(phone)
        if email or phone:
            email_phone_list.append(da)
        else:
            no_list.append(da)
    print(len(email_phone_list))
    csv_file = "./data/joblum_my_email_phone.csv"
    # 将查询结果写入CSV文件
    with open(csv_file, "w", newline="") as csvfile:
        fieldnames = data[0].keys()  # 获取字段名作为CSV的header
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()  # 写入CSV文件的header
        # 逐行写入数据
        for document in email_phone_list:
            writer.writerow(document)


if __name__ == '__main__':
    mdb = MongoDB()
    collection = 'joblum_my'
    get_data(collection)