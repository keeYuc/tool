import pymongo
import pandas as pd
import grpc
from protocol.seo import seo_service_pb2_grpc
from protocol.seo import data_pb2

url = 'mongodb://crawler:hha1layfqyx@gcp-docdb.cluster-cqwt9pwni8mm.ap-southeast-1.docdb.amazonaws.com:27017/?replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false'
#url = 'mongodb://root:8DNsidknweoRGwSbWgDN@localhost:27019'
database = "content"
myclient = pymongo.MongoClient(url)
table_service = myclient[database]['shop_service']
table_shop = myclient[database]['shop']
channel = grpc.insecure_channel("seo:9000")
service_map = {}
country = "TR"


def create_service(p, en, tr):
    ser = seo_service_pb2_grpc.SeoServiceStub(channel)
    rsb = ser.CreateShopService(data_pb2.ShopServiceReq(
        name=en, parent=p, name_tr=tr, country=country))
    return rsb.data


def create_new_service():
    for service in table_service.find({}):
        service_map[service['name_location']] = service

    for index, i in pd.read_csv('new_service.csv').iterrows():
        if i['类型-土耳其语'] not in service_map.keys():
            service_id = create_service('', i['类型-英文'], i['类型-土耳其语'])
            service_map[i['类型-土耳其语']] = {'service_id': service_id}
        if i['服务-土耳其语'] not in service_map.keys():
            service_id = create_service(
                service_map[i['类型-英文']]['service_id'], i['服务-英文'], i['服务-土耳其语'])
            service_map[i['服务-土耳其语']] = {'service_id': service_id}


def shop_replace():
    num = 0
    for shop in table_shop.find({'service': {'$exists': True}}):
        arr_service = []
        for service in shop['service']:
            if service in service_map.keys():
                arr_service.append(service_map[service]['service_id'])
        if len(arr_service) > 0:
            table_shop.update_one({'shop_id': shop['shop_id']}, {'$set': {'service': arr_service}})
            num += 1
            print('has change {}'.format(num))


if __name__ == '__main__':
    create_new_service()
    shop_replace()
