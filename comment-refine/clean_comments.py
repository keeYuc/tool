import pymongo
import grpc
uri = 'mongodb://root:8DNsidknweoRGwSbWgDN@localhost:27019'
database = "content"
myclient = pymongo.MongoClient(uri)
table_shop = myclient[database]["shop"]
table_commnet = myclient[database]["comment"]
sum_ = 0
for shop in table_shop.find({}, {'shop_id': True, '_id': False}):
    count = table_commnet.count_documents(
        {'store_id': shop['shop_id'], 'status': 'valid'})
    table_shop.update_one({'shop_id': shop['shop_id']}, {
                          '$set': {'comments': count}})
    sum_ += 1
    print(sum_)
