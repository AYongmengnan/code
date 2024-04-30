import csv

from settings import MongoDB
import requests
from parsel import Selector
import pymongo

def get_data(collection,query,filter):
    data = list(mdb.find(collection, query, filter).skip(21))   #.sort("name", pymongo.ASCENDING))
    csv_file = f"./data/{collection}.csv"
    # 将查询结果写入CSV文件
    with open(csv_file, "w", newline="") as csvfile:
        fieldnames = data[0].keys()  # 获取字段名作为CSV的header
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()  # 写入CSV文件的header
        # 逐行写入数据
        for document in data:
            writer.writerow(document)
if __name__ == '__main__':
    mdb = MongoDB()
    collection = 'email_jobslah'
    query = {'date':'2024-03-2'}
    filter = {'_id':0}
    get_data(collection,query,filter)



"""
import csv

from settings import MongoDB
import requests
from parsel import Selector
import pymongo

def get_data(collection,query,filter):
    data = list(mdb.find(collection, query, filter).sort("name", pymongo.ASCENDING))
    with open(csv_file, "w", newline="") as csvfile:
        fieldnames = data[0].keys()  # 获取字段名作为CSV的header
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()  # 写入CSV文件的header
        # 逐行写入数据
        for document in data:
            writer.writerow(document)
if __name__ == '__main__':
    mdb = MongoDB()
    collection = 'fastjobs'
    # query = {'date':'2024-02-22'}
    # filter = {'_id':0}
    # get_data(collection,query,filter)
    query = {
        "$or": [
            {"email": {"$exists": True, "$ne": ""}},
            {"phone": {"$exists": True, "$ne": ""}}
        ]
    }
    data = mdb.find(collection,query,{'_id':0,'date':0}).limit(200)
    csv_file = f"./data/{collection}.csv"
    with open(csv_file, "w", newline="") as csvfile:
        fieldnames = data[0].keys()  # 获取字段名作为CSV的header
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()  # 写入CSV文件的header
        # 逐行写入数据
        for document in data:
            writer.writerow(document)
"""