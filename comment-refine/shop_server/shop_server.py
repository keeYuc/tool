import os
import grpc
import time
import random
import pymongo
import threading
import json
if __name__ == '__main__':
    url = 'mongodb://root:8DNsidknweoRGwSbWgDN@localhost:27019'
    database = "content"
    database_crawler = "crawler"
    myclient = pymongo.MongoClient(url)
    table_shop_map = myclient[database]["crawler_shop_id_map"]
    table_shop = myclient[database]["shop"]
    table_data_zom = myclient[database_crawler]['middleware_store_zomato']
    table_data_trip = myclient[database_crawler]['middleware_store_ta']

    shop_ids = []
    shop_id_map = {}
    for i in table_shop_map.find(
            {}, {'crawler_shop_id': True, 'merchant_shop_id': True}):
        shop_ids.append(i['crawler_shop_id'])
        shop_id_map[i['crawler_shop_id']] = i['merchant_shop_id']
    print('load fin len :', len(shop_ids))

    for crawler_shop_id in shop_ids:
        data = table_data_zom.find_one({'id': crawler_shop_id})
        service = []
        if data != None:
            for i in data['page_data']['sections']['SECTION_RES_DETAILS']['HIGHLIGHTS']['highlights']:
                if i['type'] == 'AVAILABLE':
                    service.append(i['text'])
        else:
            data = table_data_trip.find_one({'id': crawler_shop_id})
            if data != None:
                org = data['original_detail']
                js = json.loads(org)
                print(js)
                break
        table_shop.update_one(
            {'shop_id': shop_id_map[crawler_shop_id]}, {"$set": {'service': service}})
