import os
import grpc
import time
import random
import pymongo
import dishes_config
from protocol.file_center import file_center_service_pb2_grpc
from protocol.file_center import image_pb2

rpc_url_fct = 'localhost:9007'
url = 'mongodb://root:8DNsidknweoRGwSbWgDN@localhost:27019'
database = "content"


class dishes():
    def __init__(self):
        # pass
        myclient = pymongo.MongoClient(url)
        self.table_dishes_img = myclient[database]["dishes_img"]
        self.table_shop = myclient[database]["shop"]
        self.files = {}
        self.prefix = '.'
        self.__load_path(['图片测试'], self.prefix)

    def __load_path(self, path, o):
        for i in path:
            if os.path.isdir(o+'/'+i):
                self.__load_path(os.listdir(o+'/'+i), o+'/'+i)
            else:
                self.files[i.split('.')[0]] = o+'/'+i

    def img_import(self):
        con = grpc.insecure_channel(rpc_url_fct)
        server = file_center_service_pb2_grpc.FileCenterServiceStub(con)
        self.url_map = {}
        for k in self.files:
            with open(self.files[k], 'rb') as f:
                s = f.read()
                rsb = server.UploadImage(image_pb2.UploadImageReq(
                    app_id="1", close_img_compress="false", img_content=s))

                self.url_map[k] = rsb.url
                self.table_dishes_img.insert_one(
                    {'name': k, 'url': rsb.url, 'create_at': int(time.time())})
        print('dishes import fin')

    def dishes_import(self):
        sum_ = 0
        for shop_id in dishes_config.shop_ids:
            shop = self.table_shop.find_one({'shop_id': shop_id})
            try:
                rand_list = self.__rand_list(shop['tag']['all'])
                shop_dishes = []
                for _ in random.randint(5, 15):
                    shop_dishes.append(
                        self.tag_dishes[self.choice_one(rand_list)])
                    sum_ += 1
                # todo 调用更新接口更新shop
            except:
                pass

    def __rand_list(self, list_: list):
        rand_map = []
        for id_ in list_:
            for _ in random.randint(0, 19):
                rand_map.append(id_)
        return rand_map

    def choice_one(self, list: list):
        return list[[random.randint(0, len(list)-1), random.randint(0,
                                                                    len(list)-1), random.randint(0, len(list)-1)][random.randint(0, 2)]]

    def dishes_build(self):
        self.tag_dishes = {}
        for i in dishes_config.tag_map:
            img = self.table_dishes_img.find_one({'name': i[2]})
            if i[0] not in self.tag_dishes.keys():
                self.tag_dishes[i[0]] = [
                    {'dishes_name': i[1], 'image':img['url']}]
            else:
                self.tag_dishes[i[0]].append(
                    {'dishes_name': i[1], 'image': img['url']})
        print('dishes build fin')

    def insert_dishes_shop(self, shop_id, dishes):
        pass


if __name__ == '__main__':
    dishes().dishes_build()
