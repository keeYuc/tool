import pandas as pd
import pymongo
import grpc
uri = 'mongodb://root:8DNsidknweoRGwSbWgDN@localhost:27019'
database = "content"
myclient = pymongo.MongoClient(uri)
table_shop = myclient[database]["shop"]
table_tag = myclient[database]["shop_tag"]
tag_map = {}
for tag in table_tag.find():
    tag_map[tag['tag_id']] = {'name': tag['name'], 'shops': 0}
for shop in table_shop.find():
    try:
        tag_map[shop['tag']['show']]['shops'] += 1
        for tag_id in shop['tag']['all']:
            tag_map[tag_id]['shops'] += 1
    except:
        pass

pd.DataFrame(tag_map).to_csv('tag_map.csv')
