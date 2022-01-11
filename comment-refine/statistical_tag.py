import pandas as pd
import pymongo

# uri = 'mongodb://root:8DNsidknweoRGwSbWgDN@localhost:27019'
uri = 'mongodb://crawler:hha1layfqyx@gcp-docdb.cluster-cqwt9pwni8mm.ap-southeast-1.docdb.amazonaws.com:27017/?replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false'
database = "content"
myclient = pymongo.MongoClient(uri)
table_shop = myclient[database]["shop"]
table_tag = myclient[database]["shop_tag"]
tag_map = {}
for tag in table_tag.find():
    tag_map[tag['tag_id']] = {'name': tag['name'], 'shops': 0}
for shop in table_shop.find({}, {'tag': True, 'shop_id': True}):
    try:
        for tag_id in shop['tag']['all']:
            tag_map[tag_id]['shops'] += 1
            if table_tag.count_documents({'tag_id': tag_id}) == 0:
                print(tag_id)
        print('has check : {}'.format(shop['shop_id']))
    except:
        pass

pd.DataFrame(tag_map).T.to_csv('tag_map.csv')
