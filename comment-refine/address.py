import os
import time
import random
import config
import pymongo
import threading
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED

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
        with ThreadPoolExecutor(max_workers=20) as t:
            wait_list = []
            for shop_id in config.shop_ids:
                wait_list.append(t.submit(self.street_import, shop_id))
            wait(wait_list, return_when=ALL_COMPLETED)

    def street_import(self, shop_id):
        i = self.table_shop.find_one(
            {'shop_id': shop_id}, {'_id': False, 'location': True, 'shop_id': True})
        self.lock.acquire()
        self.sum_ += 1
        self.lock.release()
        print(self.sum_, "   ", self.valid)
        if 'location' not in i.keys():
            return
        if 'street' not in i['location'].keys():
            print(i['shop_id'])
            for j in self.table_shop_map.find({'merchant_shop_id': i['shop_id']},
                                              {'_id': False, 'crawler_shop_id': True, 'merchant_shop_id': True}):
                yes = False
                for k in self.table_address.find({'id': j['crawler_shop_id']}):
                    for l in k['google_address']:
                        for t in l['types']:
                            if t == 'administrative_area_level_4':
                                for item in l['address_components']:
                                    for t_ in item['types']:
                                        if t_ == 'administrative_area_level_4':
                                            self.table_shop.update_one(
                                                {'shop_id': i['shop_id']},
                                                {'$set': {'location.street': item['long_name']}})
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
