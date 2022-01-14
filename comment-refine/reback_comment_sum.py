import os
import pymongo
import threading
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED

#url = 'mongodb://root:8DNsidknweoRGwSbWgDN@localhost:27019'
url = 'mongodb://crawler:hha1layfqyx@gcp-docdb.cluster-cqwt9pwni8mm.ap-southeast-1.docdb.amazonaws.com:27017/?replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false'
database_content = "content"


class dishes():
    def __init__(self):
        myclient = pymongo.MongoClient(url)
        self.table_shop = myclient[database_content]["shop"]
        self.table_comment = myclient[database_content]["comment"]
        self.lock = threading.Lock()

    def start(self):
        self.sum_ = 0
        self.valid = 0
        with ThreadPoolExecutor(max_workers=20) as t:
            wait_list = []
            for shop in self.table_shop.find({}, {'shop_id': 1}):
                wait_list.append(t.submit(self.shop_clean, shop['shop_id']))
            wait(wait_list, return_when=ALL_COMPLETED)

    def shop_clean(self, shop_id):
        sum = self.table_comment.count_documents({'store_id': shop_id})
        self.table_shop.update_one({'shop_id': shop_id}, {
                                   '$set': {'comment_sum': sum}})
        print('has reback fin id : {} comment_sum : {}'.format(shop_id, sum))


if __name__ == '__main__':
    dishes().start()
