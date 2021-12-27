import pymongo
import threading
import datetime
import pandas as pd
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


class TagImport():
    def __init__(self):
        #url = 'mongodb://root:8DNsidknweoRGwSbWgDN@localhost:27019'
        url = 'mongodb://crawler:hha1layfqyx@gcp-docdb.cluster-cqwt9pwni8mm.ap-southeast-1.docdb.amazonaws.com:27017/?replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false'
        database = "content"
        myclient = pymongo.MongoClient(url)
        self.table_tag = myclient[database]["shop_tag"]
        self.__load()

    @count_time('__load')
    def __load(self):
        for index, i in pd.read_csv(r'tag.csv').iterrows():
            print(index+1)
            update_info = {
                '$set': {}}
            if 'photo' in i.keys() and str(i['photo']) != 'nan':
                update_info['$set']['image'] = i['photo']
            if 'name' in i.keys() and i['name'] != 'nan':
                update_info['$set']['name'] = i['name']
            if len(update_info['$set']) > 0:
                self.table_tag.update_one({'tag_id': i['tag id']}, update_info)


if __name__ == '__main__':
    TagImport()
