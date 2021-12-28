import pymongo
import threading
import json
import pandas as pd
import datetime
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED


def count_time(prefix):
    def count_time__(func):
        def int_time(*args, **kwargs):
            start_time = datetime.datetime.now()  # 程序开始时间
            func(*args, **kwargs)
            over_time = datetime.datetime.now()   # 程序结束时间
            total_time = (over_time-start_time).total_seconds()
            print('{} 共计: {}秒'.format(prefix, total_time))
        return int_time
    return count_time__


class ShopServer:
    def __init__(self):
        #url = 'mongodb://root:8DNsidknweoRGwSbWgDN@localhost:27019'
        url = 'mongodb://crawler:hha1layfqyx@gcp-docdb.cluster-cqwt9pwni8mm.ap-southeast-1.docdb.amazonaws.com:27017/?replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false'
        database = "content"
        database_crawler = "crawler"
        myclient = pymongo.MongoClient(url)
        self.table_shop_map = myclient[database]["crawler_shop_id_map"]
        self.table_shop = myclient[database]["shop"]
        self.table_data_zom = myclient[database_crawler]['middleware_store_zomato']
        self.table_data_trip = myclient[database_crawler]['middleware_store_ta']
        self.lock = threading.Lock()
        self.service = []
        self.valid_shops = 0
        self.sum_shops = 0
        self.load_reflect()
        self.load_shop()
        self.import_service()

    @count_time('load_shop')
    def load_shop(self):
        self.shop_ids = []
        self.shop_id_map = {}
        for i in self.table_shop_map.find(
                {}, {'crawler_shop_id': True, 'merchant_shop_id': True}):

            self.shop_ids.append(i['crawler_shop_id'])
            self.shop_id_map[i['crawler_shop_id']] = i['merchant_shop_id']
        print('load fin len :', len(self.shop_ids))

    def load_reflect(self):
        self.service_reflect = {}
        for index, i in pd.read_csv(r'reflect.csv').iterrows():
            self.service_reflect[i['服务']] = str(i['二级'])

    def reflect_service(self, s, list: list):
        if s not in self.service_reflect.keys():
            print('没有这个服务 : ', s)
        else:
            rs = self.service_reflect[s]
            if rs != 'nan':
                list.append(rs)

    def __do_import(self, crawler_shop_id):
        self.lock.acquire()
        self.sum_shops += 1
        self.lock.release()
        service = []
        data = self.table_data_trip.find_one(
            {'id': crawler_shop_id}, {'original_detail': True, '_id': False})
        if data != None:
            print('find in trip')
            org = data['original_detail']
            if type(org) == type(''):
                js = json.loads(org)
                for i in js['redux']['api']['responses']['/data/1.0/restaurant/{}/overview'.format(crawler_shop_id)]['data']['detailCard']['tagTexts']['features']['tags']:
                    self.reflect_service(i['tagValue'], service)
        else:
            data = self.table_data_zom.find_one(
                {'id': crawler_shop_id, 'page_data': True, '_id': False})
            if data != None:
                print('find in zom')
                for i in data['page_data']['sections']['SECTION_RES_DETAILS']['HIGHLIGHTS']['highlights']:
                    if i['type'] == 'AVAILABLE':
                        self.reflect_service(i['text'], service)
            else:
                print(
                    'this id cannot find in database crawler_shop_id: {} shop_id: {}'.format(crawler_shop_id, self.shop_id_map[crawler_shop_id]))
        if len(service) > 0:
            self.table_shop.update_one(
                {'shop_id': self.shop_id_map[crawler_shop_id]}, {"$set": {'service': list(set(service))}})
            self.lock.acquire()
            print(self.shop_id_map[crawler_shop_id])
            self.valid_shops += 1
            self.lock.release()
        print('valid shops :{} sum: {}'.format(
            self.valid_shops, self.sum_shops))

    @ count_time('import_service')
    def import_service(self):
        with ThreadPoolExecutor(max_workers=10) as t:
            wait_list = []
            for crawler_shop_id in self.shop_ids:
                wait_list.append(t.submit(self.__do_import, crawler_shop_id))
                # wait_list.append(t.submit(self.add_create_at,
                #                          (self.shop_id_map[crawler_shop_id])))
            wait(wait_list, return_when=ALL_COMPLETED)

    def add_create_at(self, shop_id):
        print(shop_id)
        i = self.table_shop.find_one({'shop_id': shop_id}, {
                                     '_id': False, 'update_at': True})
        self.table_shop.update_one({'shop_id': shop_id}, {
            '$set': {'create_at': i['update_at']}})


if __name__ == '__main__':
    ShopServer()
