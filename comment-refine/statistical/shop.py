import pymongo
import grpc
import datetime
import threading
import json
import time
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, ALL_COMPLETED, wait

# url = 'mongodb://root:8DNsidknweoRGwSbWgDN@localhost:27019'
# url = 'mongodb://sms:hyy9JZFCnV@gcp-card-documentdb.cluster-ctckgm7c9ap0.ap-southeast-1.docdb.amazonaws.com:27017/?replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false'
url = 'mongodb://crawler:hha1layfqyx@gcp-docdb.cluster-cqwt9pwni8mm.ap-southeast-1.docdb.amazonaws.com:27017/?replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false'
domain = 'www.yummyadvisor.com/'
database = "content"
database_crawler = "crawler"


def count_time(prefix):
    def count_time__(func):
        def int_time(*args, **kwargs):
            start_time = datetime.datetime.now()  # 程序开始时间
            func(*args, **kwargs)
            over_time = datetime.datetime.now()  # 程序结束时间
            total_time = (over_time - start_time).total_seconds()
            print('{} 共计: {}秒'.format(prefix, total_time))

        return int_time

    return count_time__


state_map = {'Adana': 'Adana',
             'Adıyaman': 'Adiyaman',
             'Afyonkarahisar': 'Afyonkarahisar',
             'Ankara': 'Ankara',
             'Antalya': 'Antalya',
             'Bursa': 'Bursa',
             'Eskişehir': 'Eskisehir',
             'Gaziantep': 'Gaziantep',
             'Konya': 'Konya',
             'Muğla': 'Mugla',
             'İstanbul': 'Istanbul',
             'İzmir': 'Izmir',
             'Bingöl': 'Bingol',
             'Çanakkale': 'Canakkale',
             'Çeşme': 'Cesme'}


class Grouper:
    def __init__(self):
        myclient = pymongo.MongoClient(url)
        self.table_shop_map = myclient[database]["crawler_shop_id_map"]
        self.table_shop = myclient[database]["shop"]
        self.table_district = myclient[database]['shop_district']
        self.table_comment_zom = myclient[database_crawler]['middleware_review_zomato']
        self.table_comment_trip = myclient[database_crawler]['middleware_review_ta']
        self.shops = {}
        self.lock = threading.Lock()

    @count_time('run')
    def run(self):
        with ThreadPoolExecutor(max_workers=1) as t:
            wait_list = []
            for data in self.table_shop_map.find({},
                                                 {'merchant_shop_id': True, 'crawler_shop_id': True, 'platform': True}):
                # self.get_shop(data['merchant_shop_id'],
                #               data['crawler_shop_id'], data['platform'])
                wait_list.append(
                    t.submit(self.get_shop, data['merchant_shop_id'], data['crawler_shop_id'], data['platform']))
                print('has commit job : {}'.format(len(wait_list)))
            wait(wait_list, return_when=ALL_COMPLETED)
            print('has len ：{}'.format(len(self.shops)))
        pd.DataFrame(self.shops).T.to_csv('shop_message.csv')

    def get_shop(self, shop_id, crawler_shop_id, platform):
        shop = {}
        data = self.table_shop.find_one({'shop_id': shop_id})
        if data != None:
            try:
                shop['shop_id'] = shop_id
                shop['name'] = data['name']
                if 'priority' in data.keys():
                    shop['priority'] = data['priority']
                if 'comment_sum' in data.keys():
                    shop['comment_sum'] = data['comment_sum']
                shop['middleware_comment_num'] = self.get_middleware_comment_num(
                    crawler_shop_id, platform)
                if 'detail_images' in data.keys():
                    shop['detail_image_num'] = len(data['detail_images'])
                if 'tag' in data.keys():
                    shop['tag_num'] = len(data['tag']['all'])
                if 'location' in data.keys():
                    if 'city' in data['location'].keys():
                        shop['city'] = data['location']['city']
                    if 'street' in data['location'].keys():
                        shop['street'] = data['location']['street']
                    if 'state' in data['location'].keys():
                        shop['url'] = self.get_url(
                            data['location']['state'], data['seo_key'])
                if 'district_id' in data.keys():
                    shop['district'] = self.get_district(data['district_id'])
                if 'stars' in data.keys():
                    sum_stars = 0.0
                    sum_num = 0.0
                    for k in data['stars']:
                        sum_num += data['stars'][k]
                        if k == '1':
                            sum_stars += data['stars'][k] * 1
                        if k == '2':
                            sum_stars += data['stars'][k] * 2
                        if k == '3':
                            sum_stars += data['stars'][k] * 3
                        if k == '4':
                            sum_stars += data['stars'][k] * 4
                        if k == '5':
                            sum_stars += data['stars'][k] * 5
                    if sum_stars != 0 and sum_num != 0:
                        shop['score'] = sum_stars / sum_num
            except BaseException as err:
                print(err)
            self.shops[shop_id] = shop
        else:
            return

    def get_url(self, state, seo_key):
        if state in state_map.keys():
            state = state_map[state]
        return domain + 'tr-tr-{}/{}/'.format(state, seo_key)

    def get_district(self, district_id):
        district = self.table_district.find_one(
            {'district_id': district_id})
        try:
            return district['name']
        except:
            return ''

    def get_middleware_comment_num(self, crawler_shop_id, platform):
        if platform == 'tripadvisor':
            return self.table_comment_trip.count_documents({'store_id': crawler_shop_id})
        elif platform == 'zomato':
            return self.table_comment_zom.count_documents(
                {'store_id': crawler_shop_id})


if __name__ == '__main__':
    Grouper().run()
