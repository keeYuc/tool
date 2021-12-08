import pymongo
import pandas as pd
uri = 'mongodb://content:nbp4te5fxkq@gcp-docdb.cluster-cqwt9pwni8mm.ap-southeast-1.docdb.amazonaws.com:27017/?replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false'
#uri = 'mongodb://root:8DNsidknweoRGwSbWgDN@localhost:27019'
database = "content"
database_crawler = "crawler"

if __name__ == '__main__':
    myclient = pymongo.MongoClient(uri)
    table_shop_crawler = myclient[database_crawler]["middleware_store_ta"]
    table_shop_map = myclient[database]["crawler_shop_id_map"]
    table_shop = myclient[database]["shop"]
    list = []
    for item in table_shop_map.find({"country": "TR"}):
        data = {}
        shop_id = item['merchant_shop_id']
        shop = table_shop_crawler.find_one({'id': item['crawler_shop_id']})
        shop_ = table_shop.find_one({'shop_id': shop_id})
        data['shop_id'] = shop_id
        if 'priority' in shop_.keys():
            data['priority'] = shop_['priority']
        if 'name' in shop.keys():
            data['name'] = shop['name']
        if 'review_score_distribution' in shop.keys():
            data['stars'] = shop['review_score_distribution']
        list.append(data)
        print(len(list))
    pd.DataFrame(list).to_csv('shop.csv')
