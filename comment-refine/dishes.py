import os
import grpc
import time
import random
import pandas as pd
import pymongo
import config
from protocol.file_center import file_center_service_pb2_grpc
from protocol.file_center import image_pb2
from protocol.seo import seo_service_pb2_grpc
from protocol.seo import data_pb2

rpc_url_fct = 'seo:9000'
rpc_url_seo = 'seo:9000'
# url = 'mongodb://crawler:hha1layfqyx@gcp-docdb.cluster-cqwt9pwni8mm.ap-southeast-1.docdb.amazonaws.com:27017/?replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false'
url = 'mongodb://crawler:hha1layfqyx@gcp-docdb.cluster-cqwt9pwni8mm.ap-southeast-1.docdb.amazonaws.com:27017/?replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false'
# url = 'mongodb://root:8DNsidknweoRGwSbWgDN@localhost:27019'
database = "content"


class dishes():
    def __init__(self):
        myclient = pymongo.MongoClient(url)
        self.table_dishes_img = myclient[database]["dishes_img"]
        self.table_shop = myclient[database]["shop"]
        self.files = {}
        self.prefix = '.'
        self.__load_path(['cpp5'], self.prefix)

    def __load_path(self, path, o):
        for i in path:
            if os.path.isdir(o + '/' + i):
                self.__load_path(os.listdir(o + '/' + i), o + '/' + i)
            else:
                self.files[i.split('.')[0]] = o + '/' + i

    def img_import(self):
        con = grpc.insecure_channel(rpc_url_fct)
        server = file_center_service_pb2_grpc.FileCenterServiceStub(con)
        self.url_map = {}
        for k in self.files:
            if self.table_dishes_img.count_documents({"name": k}) == 0:
                try:
                    with open(self.files[k], 'rb') as f:
                        s = f.read()
                        rsb = server.UploadImage(image_pb2.UploadImageReq(
                            app_id="418515749146071139", close_img_compress="false", img_content=s))
                        self.url_map[k] = rsb.url
                        self.table_dishes_img.insert_one(
                            {'name': k, 'url': rsb.url, 'create_at': int(time.time())})
                except BaseException as err:
                    print("err name :", k, "                      err:", err)
        print('dishes import fin')

    def __dishes_import(self):
        sum_ = 0
        con = grpc.insecure_channel(rpc_url_seo)
        server = seo_service_pb2_grpc.SeoServiceStub(con)
        # for shop_id in dishes_config.shop_ids:
        for shop in self.table_shop.find({'shop_id': {'$in': {config.shop_ids}}, 'country': 'TR'},
                                         {'tag': True, 'shop_id': True, '_id': False}):
            shop_dishes = []
            shop_names = set()
            if 'tag' in shop.keys():
                rand_list = self.__rand_list(
                    set(shop['tag']['all']) & self.tag_ids)
                sum = max(random.randint(5, 15), 5)
                cs = 0
                while len(rand_list) > 0:
                    cs += 1
                    try:
                        if len(shop_dishes) > sum or cs > 200:
                            print('has use cishu ', cs)
                            break
                        else:
                            data = self.choice_one(self.tag_dishes[self.choice_one(
                                rand_list)]
                                                   )
                            if data.name not in shop_names:
                                shop_dishes.append(data)
                                shop_names.add(data.name)
                    except BaseException as err:
                        pass
            if len(shop_dishes) > 0:
                server.UpdateShop(data_pb2.ShopReq(
                    shop_id=shop['shop_id'], special_dishes=shop_dishes))
                sum_ += len(shop_dishes)
                print(shop['shop_id'], 'has create :',
                      len(shop_dishes), ' ', sum_)
        print("dishes_import fin sum: ", sum_)

    def __rand_list(self, list_):
        rand_map = []
        if len(list_) == 0:
            return rand_map
        for id_ in list_:
            for _ in range(random.randint(0, 19)):
                rand_map.append(id_)
        return rand_map

    def choice_one(self, list: list):
        return list[[random.randint(0, len(list) - 1), random.randint(0,
                                                                      len(list) - 1), random.randint(0, len(list) - 1)][
            random.randint(0, 2)]]

    def dishes_build(self):
        self.tag_dishes = {}
        self.tag_ids = []
        for _, i in pd.read_csv(r'dishes.csv').iterrows():
            img = self.table_dishes_img.find_one(
                {'name': i['Photo file name']})
            try:
                if i['tag id'] not in self.tag_dishes.keys():
                    self.tag_dishes[i['tag id']] = [
                        data_pb2.SpecialDish(name=i['Dishes name'], image=img['url'])]
                else:
                    self.tag_dishes[i['tag id']].append(
                        data_pb2.SpecialDish(name=i['Dishes name'], image=img['url']))

                self.tag_ids.append(i['tag id'])
            except:
                print('没有这个图片 name :', i['Photo file name'])
        self.tag_ids = set(self.tag_ids)
        print('dishes build fin')
        self.__dishes_import()


if __name__ == '__main__':
    # dishes().img_import()
    dishes().dishes_build()
