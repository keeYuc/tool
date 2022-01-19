import pandas as pd
import pymongo

#url = 'mongodb://root:8DNsidknweoRGwSbWgDN@localhost:27019'
url = 'mongodb://crawler:hha1layfqyx@gcp-docdb.cluster-cqwt9pwni8mm.ap-southeast-1.docdb.amazonaws.com:27017/?replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false'
database = "content"
myclient = pymongo.MongoClient(url)
table_shop = myclient[database]["shop"]
tag_map = []
for item in table_shop.find({},{""}).limit(100):
    tag_map.append(item)
    print(len(tag_map))

pd.DataFrame(tag_map).to_csv('shop_map.csv')
