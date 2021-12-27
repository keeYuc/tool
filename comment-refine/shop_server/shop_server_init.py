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
        # url = 'mongodb://root:8DNsidknweoRGwSbWgDN@localhost:27019'
        url = 'mongodb://crawler:hha1layfqyx@gcp-docdb.cluster-cqwt9pwni8mm.ap-southeast-1.docdb.amazonaws.com:27017/?replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false'
        database = "content"
        database_crawler = "crawler"
        myclient = pymongo.MongoClient(url)
        self.table_data_zom = myclient[database_crawler]['middleware_store_zomato']
        self.table_data_trip = myclient[database_crawler]['middleware_store_ta']
        self.lock = threading.Lock()
        self.service = []
        self.valid_shops = 0
        self.sum_shops = 0
        self.import_service()

    def __do_import(self, t, list):
        sum = 0
        for data in self.table_data_trip.find(
                {}, {'original_detail': True, 'id': True, '_id': False}):
            org = data['original_detail']
            sum += 1
            print(sum, '    ', len(self.service))
            if type(org) == type(''):
                js = json.loads(org)
                for i in js['redux']['api']['responses']['/data/1.0/restaurant/{}/overview'.format(data['id'])]['data']['detailCard']['tagTexts']['features']['tags']:
                    self.service.append(i['tagValue'])
        for data in self.table_data_zom.find(
                {}, {'page_data': True, '_id': False}):
            sum += 1
            print(sum, '    ', len(self.service))
            for i in data['page_data']['sections']['SECTION_RES_DETAILS']['HIGHLIGHTS']['highlights']:
                if i['type'] == 'AVAILABLE':
                    self.service.append(i['text'])

    @ count_time('import_service')
    def import_service(self):
        with ThreadPoolExecutor(max_workers=10) as t:
            wait_list = []
            self.__do_import(t, wait_list)
            wait(wait_list, return_when=ALL_COMPLETED)
        tmp = {}
        for i in self.service:
            if i not in tmp.keys():
                tmp[i] = [1]
            else:
                tmp[i][0] += 1
        pd.DataFrame(tmp).to_csv('shop_service.csv')


if __name__ == '__main__':
    ShopServer()
