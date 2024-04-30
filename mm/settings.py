import pymongo
from pymongo.errors import DuplicateKeyError, BulkWriteError
class MongoDB():
    def __init__(self):
        self.db_url = 'mongodb://naxida:aJ2%2BmA4%7CsW1%2FfD6~@imdiona.com:8017'
        self.client = pymongo.MongoClient(self.db_url)
        self.db = self.client['mmmm']


    def insert_one(self, collection_name, document):
        """
        :param collection_name: 集合名
        :param document: json数据
        :return:
        """
        collection = self.db[collection_name]
        try:
            result = collection.insert_one(document)
            return result.inserted_id
        except DuplicateKeyError as e:
            print(e)
            return False

    def insert_many(self, collection_name, documents):
        """
        :param collection_name: 集合名
        :param documents: 数组中为json数据
        :return:
        """
        collection = self.db[collection_name]
        try:
            result = collection.insert_many(
                documents)  # 设置 ordered 选项为 False，以在出现重复键错误时继续插入其他文档。但请注意，这不会跳过错误文档，而是在发生错误后继续插入操作。
            return result.inserted_ids
        except BulkWriteError as e:
            print(e)

    def find_one(self, collection_name, query):
        collection = self.db[collection_name]
        return collection.find_one(query)

    def find_many(self, collection_name, query):
        collection = self.db[collection_name]
        return list(collection.find(query))

    def find_all(self, collection_name):
        collection = self.db[collection_name]
        return collection.find()

    def find(self, collection_name, query, filter):
        collection = self.db[collection_name]
        results = collection.find(query, filter)
        return results

    def update_one(self, collection_name, query, update):
        """
        传递了 upsert=True 选项，以便在数据不存在时执行插入操作
        :param collection_name:
        :param query: 条件
        :param update: 更新已有字段：{'b': 22}，增加新字段：{'$set':{'age': 22}}
        :return:
        """
        collection = self.db[collection_name]
        result = collection.update_one(query, {'$set': update}, upsert=True)
        return result.modified_count

    def update_many(self, collection_name, update):
        collection = self.db[collection_name]
        result = collection.update_many({}, {'$set': update}, upsert=True)
        return result.modified_count

    def delete_one(self, collection_name, query):
        collection = self.db[collection_name]
        result = collection.delete_one(query)
        return result.deleted_count

    def delete_many(self, collection_name):
        collection = self.db[collection_name]
        result = collection.delete_many({})
        return result.deleted_count

    def create_index(self, collection_name, fields):
        """
        创建唯一索引
        :param collection_name:
        :param fields: list data
        :return:
        """
        collection = self.db[collection_name]
        for field in fields:
            collection.create_index([(field, pymongo.ASCENDING)], unique=True,
                                    partialFilterExpression={field: {"$exists": True}})
            print('已创建', field, '唯一索引')
        return True

    def create_indexs(self, collection_name, fields):
        """
        创建组合索引
        :param collection_name:
        :param fields: list
        :return:
        """
        collection = self.db[collection_name]
        indexs = []
        for field in fields:
            indexs.append((field, pymongo.ASCENDING))
        collection.create_index(indexs, unique=True)
        return print('组合索引已创建')

    def rename(self, collection_name, new_collection_name):
        collection = self.db[collection_name]
        try:
            collection.rename(new_collection_name, dropTarget=False)
            return print("Collection renamed successfully.")
        except Exception as e:
            return print(e)

    def copy_data(self, collection_name, new_collection_name):
        source_collection = self.db[collection_name]  # 替换为源集合名称
        target_collection = self.db[new_collection_name]  # 替换为目标集合名称
        pipeline = [
            {
                "$match": {}  # 筛选所有文档
            },
            {
                "$out": new_collection_name  # 输出到目标集合
            }
        ]
        source_collection.aggregate(pipeline)

    def query(self, collection_name, pipeline):
        """
        聚合查询
        :param collection_name:
        :return:
        """
        collection = self.db[collection_name]
        try:
            return list(collection.aggregate(pipeline))
        except Exception as e:
            print('聚合查询失败：', e)
            return None

if __name__ == '__main__':
    mdb = MongoDB()
    mdb.create_indexs('ease',['name','phones','emails','whatsapps','telegrams'])