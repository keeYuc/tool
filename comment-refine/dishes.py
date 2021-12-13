import os
import grpc
import dishes_config
from protocol.file_center import file_center_service_pb2_grpc
from protocol.file_center import image_pb2

rpc_url_fct = 'localhost:9007'
url = 'mongodb://root:8DNsidknweoRGwSbWgDN@localhost:27019'
database = "content"


class dishes():
    def __init__(self):
        myclient = pymongo.MongoClient(url)
        self.table_dishes = myclient[database]["dishes"]
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
                url_map.url_map[k] = rsb['url']
                self.table_dishes.insert_one({'name': k, 'url': rsb['url']})
        print('dishes import fin')

    def dishes_build(self):
        for shop_id in dishes_config.shop_ids:
            

    def dishes_import(self):
        pass

    def insert_dishes_shop(self, shop_id, dishes):
        pass


if __name__ == '__main__':
    dishes().img_import()
