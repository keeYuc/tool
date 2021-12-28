import os
import grpc
import time
import random
import pymongo
import threading

#url = 'mongodb://root:8DNsidknweoRGwSbWgDN@localhost:27019'
url = 'mongodb://crawler:hha1layfqyx@gcp-docdb.cluster-cqwt9pwni8mm.ap-southeast-1.docdb.amazonaws.com:27017/?replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false'
database_c = "crawler"
database_content = "content"


class dishes():
    def __init__(self):
        myclient = pymongo.MongoClient(url)
        self.table_address = myclient[database_c]["middleware_store_google_address"]
        self.table_shop = myclient[database_content]["shop"]
        self.table_shop_map = myclient[database_content]["crawler_shop_id_map"]
        self.lock = threading.Lock()

    def start(self):
        self.sum_ = 0
        self.valid = 0
        sum = self.table_shop.count_documents({})
        index = 0
        threads = 10
        thread_list = []
        while index < threads:
            a = threading.Thread(target=self.street_import,
                                 args=(index*(sum/threads), (index+1)*(sum/threads),))
            a.start()
            thread_list.append(a)
            index += 1
        self.street_import((threads-1)*(sum/threads), sum)
        for item in thread_list:
            item.join()

    def street_import(self, skip, limit):
        for i in self.table_shop.find({}, {'_id': False, 'location': True, 'shop_id': True}).skip(int(skip)).limit(int(limit)):
            self.lock.acquire()
            self.sum_ += 1
            self.lock.release()
            print(self.sum_, "   ", self.valid)
            if 'location' not in i.keys():
                continue
            if 'street' not in i['location'].keys():
                print(i['shop_id'])
                for j in self.table_shop_map.find({'merchant_shop_id': i['shop_id']}, {'_id': False, 'crawler_shop_id': True, 'merchant_shop_id': True}):
                    yes = False
                    for k in self.table_address.find({'id': j['crawler_shop_id']}):
                        for l in k['google_address']:
                            for t in l['types']:
                                if t == 'administrative_area_level_4':
                                    for item in l['address_components']:
                                        for t_ in item['types']:
                                            if t_ == 'administrative_area_level_4':
                                                self.table_shop.update_one(
                                                    {'shop_id': i['shop_id']}, {'$set': {'location.street': item['long_name']}})
                                                self.lock.acquire()
                                                self.valid += 1
                                                self.lock.release()
                                                yes = True
                                                break
                    if not yes:
                        print(i['shop_id'])
        print("update fin sum:", self.sum_, "   valid :", self.valid)


if __name__ == '__main__':
    dishes().start()
