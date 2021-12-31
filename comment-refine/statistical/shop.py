import pymongo
import grpc
import datetime
import json
#url = 'mongodb://root:8DNsidknweoRGwSbWgDN@localhost:27019'
url = 'mongodb://sms:hyy9JZFCnV@gcp-card-documentdb.cluster-ctckgm6c9ap0.ap-southeast-1.docdb.amazonaws.com:27017/?replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false'
database = "content"


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


class Cleaner:
    def __init__(self):
        myclient = pymongo.MongoClient(url)
        self.table_shop = myclient[database]["shop"]
        self.table_shop_map = myclient[database]["crawler_shop_id_map"]
        self.table_comment = myclient[database]["comment"]
        self.back = []

    def run(self):
        self.__clean_shop_comment()
        self.__clean_shop_comment_by_map()
        self.__save()

    def __update_by_shop_id(self, shop_id):
        self.table_comment.update_many(
            {'store_id': shop_id, 'type': 'normal'}, {'$set': {
                'type': 'import'
            }})
        self.back.append(shop_id)
        print('has change shop len :{}'.format(len(self.back)))

    @count_time('__clean_shop_comment')
    def __clean_shop_comment(self):
        for shop in self.table_shop.find(
                {'data_source': 'import'}, {'_id': False,  'shop_id': True}):
            shop_id = shop['shop_id']
            self.__update_by_shop_id(shop_id)

    @count_time('__clean_shop_comment_by_map')
    def __clean_shop_comment_by_map(self):
        for shop in self.table_shop_map.find(
                {}, {'_id': False,  'merchant_shop_id': True}):
            shop_id = shop['merchant_shop_id']
            self.__update_by_shop_id(shop_id)

    def __save(self):
        with open('back.json', 'w') as fd:
            json.dump(self.back, fd)


if __name__ == '__main__':
    Cleaner().run()
