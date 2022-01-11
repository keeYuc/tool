import threading

import pymongo
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED

#uri = 'mongodb://root:8DNsidknweoRGwSbWgDN@localhost:27019'
uri = 'mongodb://crawler:hha1layfqyx@gcp-docdb.cluster-cqwt9pwni8mm.ap-southeast-1.docdb.amazonaws.com:27017/?replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false'
database = "content"
myclient = pymongo.MongoClient(uri)
table_shop = myclient[database]["shop"]
table_tag = myclient[database]["shop_tag"]
tag_map = {}
tag_name_map = {}
reflect_map = {}



def run():
    for tag in table_tag.find():
        name = tag['name'].replace(' ', '')
        if name == name.rstrip('s'):
            name = name.rstrip('n').upper()
        else:
            name = name.rstrip('s').upper()

        tag_map[tag['tag_id']] = {
            'name': name, 'shops': 0, 'item': tag, 'is_parent': tag['parent'] == ''}
        if name in tag_name_map.keys():
            tag_name_map[name].append(tag['tag_id'])
        else:
            tag_name_map[name] = [tag['tag_id']]

    has = 0
    for shop in table_shop.find({}, {'tag': True}):
        if 'tag_id' in shop.keys():
            for tag_id in shop['tag']['all']:
                tag_map[tag_id]['shops'] += 1
        has += 1
        print(has)

    for k, v in tag_name_map.items():
        if len(v) > 1:
            do_clean(k, v)
    shop_clean()


def do_clean(name, ids):
    max_tag_id = ''
    max_num = -1
    for tag_id in ids:
        item = tag_map[tag_id]
        if item['shops'] > max_num or (item['shops'] == max_num and item['is_parent']):
            max_num = item['shops']
            max_tag_id = tag_id
    for tag_id in ids:
        if tag_id != max_tag_id:
            clean_tag(tag_id, tag_map[tag_id]['is_parent'])
    reflect_map[name] = max_tag_id


def clean_tag(tag_id, is_parent):
    table_tag.delete_one({'tag_id': tag_id})
    if is_parent:
        table_tag.update_many({'parent': tag_id}, {'$set': {'parent': ''}})


def shop_clean():
    with ThreadPoolExecutor(max_workers=20) as t:
        wait_list = []
        for shop in table_shop.find({'tag': {'$exists': True}}, {'tag': True, 'shop_id': True}):
            wait_list.append(t.submit(do_shop_clean, shop))
        wait(wait_list, return_when=ALL_COMPLETED)


def do_shop_clean(shop):
    new_tags = set()
    for tag_id in shop['tag']['all']:
        if tag_id in tag_map.keys():
            name = tag_map[tag_id]['name']
            if name in reflect_map.keys():
                new_tags.add(reflect_map[name])
            else:
                new_tags.add(tag_id)
    tags = list(new_tags)
    if len(tags) > 0:
        table_shop.update_one({'shop_id': shop['shop_id']}, {'$set': {'tag.all': tags, 'tag.show': tags[0]}})
    else:
        table_shop.update_one({'shop_id': shop['shop_id']}, {'$unset': {'tag': 1}})
        print('has clean shop : {}'.format(shop['shop_id']))


if __name__ == '__main__':
    run()
