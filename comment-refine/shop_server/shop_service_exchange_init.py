import pymongo
import uuid
import time
import threading
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED

#url = 'mongodb://crawler:hha1layfqyx@gcp-docdb.cluster-cqwt9pwni8mm.ap-southeast-1.docdb.amazonaws.com:27017/?replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false'
url = 'mongodb://root:8DNsidknweoRGwSbWgDN@localhost:27019'
database = "content"
myclient = pymongo.MongoClient(url)
table_service = myclient[database]['shop_service']

service_map = {}


def create_service(p, en, tr):
    item = {
        'service_id': str(uuid.uuid4()),
        'name': en,
        'name_tr': tr,
        'update_at': 1,
        'create_at': 1,
        'is_delete': false
    }
    # table_service.insert_one()
    return {}


for service in table_service.find({}):
    service_map[service['name']] = service

for index, i in pd.read_csv('new_service.csv').iterrows():
    if i['类型-英文'] not in service_map.keys():
        create_service('', i['类型-英文'], i['类型-土耳其语'])
        service_map[i['类型-英文']] = {}
    # if i['服务-英文'] not in service_map.keys():
    #    service_map[i['服务-英文']
    #                ] = create_service(service_map[i['服务-英文']]['service_id'], i['服务-英文'], i['服务-土耳其语'])
