import pymongo
import grpc
import datetime
import threading
import json
# url = 'mongodb://root:8DNsidknweoRGwSbWgDN@localhost:27019'
url = 'mongodb://sms:hyy9JZFCnV@gcp-card-documentdb.cluster-ctckgm6c9ap0.ap-southeast-1.docdb.amazonaws.com:27017/?replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false'
database = "content"
myclient = pymongo.MongoClient(url)
table_shop_map = myclient[database]["crawler_shop_id_map"]
table_shop = myclient[database]["shop"]


class Grouper:
    def __init__(self):
        myclient = pymongo.MongoClient(url)
        self.table_shop_map = myclient[database]["crawler_shop_id_map"]
        self.table_shop = myclient[database]["shop"]
        self.lock = threading.Lock()


def tmp():
    for data in table_shop_map.find({}, {'merchant_shop_id': True, 'platform': True}):
        get_shop(data['merchant_shop_id'])


def get_shop(shop_id):
    shop = {}
    data = table_shop.find_one({'shop_id': shop_id})
    if data != None:
        shop['shop_id'] = shop_id
        shop['name'] = data['name']
        shop['url'] = 'todo'
        shop['priority'] = 'todo'
        shop['comment_num'] = data['comment_num']
        shop['middleware_comment_num'] = 'todo'
        shop['image_num'] = 'todo'
        shop['tag_num'] = 'todo'
        if 'location' in data.keys():
            if 'city' in data['location'].keys():
                shop['city'] = data['location']['city']
            if 'street' in data.keys():
                shop['street'] = data['location']['street']

        if 'district_id' in data.keys():
            shop['district'] = 'todo'
    else:
        return


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
