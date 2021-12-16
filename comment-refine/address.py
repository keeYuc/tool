import os
import grpc
import time
import random
import pymongo
import dishes_config
from protocol.file_center import file_center_service_pb2_grpc
from protocol.file_center import image_pb2
from protocol.seo import seo_service_pb2_grpc
from protocol.seo import data_pb2

# rpc_url_fct = 'localhost:9007'
# rpc_url_seo = 'localhost:9007'
url = 'mongodb://root:8DNsidknweoRGwSbWgDN@localhost:27019'
database_c = "crawler"
database_content = "content"


class dishes():
    def __init__(self):
        myclient = pymongo.MongoClient(url)
        self.table_address = myclient[database_c]["middleware_store_google_address"]
        self.table_shop = myclient[database_content]["shop"]
        self.table_shop_map = myclient[database_content]["crawler_shop_id_map"]

    def street_import(self):
        sum_ = 0
        valid = 0
        for i in self.table_shop.find({}, {'_id': False, 'shop_id': True}):
            sum_ += 1
            print(sum_, "   ", valid)
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
                                            valid += 1
                                            yes = True
                                            break
                if not yes:
                    print(i['shop_id'])
        print("update fin sum:", sum_, "   valid :", valid)


if __name__ == '__main__':
    dishes().street_import()
