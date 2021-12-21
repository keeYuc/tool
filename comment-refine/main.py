import pymongo
import random
import datetime
import pandas as pd
import config
import grpc
from concurrent.futures import ThreadPoolExecutor
import threading
from protocol.seo import seo_service_pb2_grpc
from protocol.seo import data_pb2
import time
#uri = 'mongodb://root:8DNsidknweoRGwSbWgDN@localhost:27019'
#uri = 'mongodb://root:8DNsidknweoRGwSbWgDN@mongo:27017'
uri = 'mongodb://crawler:hha1layfqyx@gcp-docdb.cluster-cqwt9pwni8mm.ap-southeast-1.docdb.amazonaws.com:27017/?replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false'
rpc_url = 'seo:9007'
database = "content"
database_crawler = "crawler"
HIGH = 'high'
NORMAL = 'normal'
LOW = 'low'
KEY_STORE_NAME = '{store_name}'
KEY_B_HOUR = '{business_hours}'
KEY_TAG = '{tag}'
KEY_LOCATION = '{location}'
KEY_DISTRICT = '{shopping_district}'
KEY_PCT = '{per_customer_transaction}'
KEY_STREET = '{street}'
TR = 'TR'


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


class Refiner():
    @ count_time("__init__")
    def __init__(self) -> None:
        myclient = pymongo.MongoClient(uri)
        #self.table_comment = myclient[database]["comment"]
        self.table_shop = myclient[database]["shop"]
        self.table_shop_tag = myclient[database]["shop_tag"]
        self.table_shop_district = myclient[database]["shop_district"]
        self.table_refine_comment = myclient[database]["refine_comment"]
        self.table_avatar = myclient[database]["avatar"]
        self.table_name = myclient[database]["name"]
        self.table_middleware_review = myclient[database_crawler]["middleware_review_ta"]
        self.table_shop_map = myclient[database]["crawler_shop_id_map"]
        # self.init_database()
        self.load_shop_id()
        self.load_connect()
        self.load_statement()
        self.load_image()
        self.load_word()
        self.load_commnet_shop_tag_district()
        self.statement_rebuild()
        self.lock = threading.Lock()

    def create_comments(self, list: list):
        serve = seo_service_pb2_grpc.SeoServiceStub(self.connect)
        serve.CreateComments(data_pb2.CommentsReq(items=list))

    def init_database(self):
        avatar_list = []
        name_list = []
        for i in self.table_middleware_review.find(
                {}, {"language": True, "user_name": True, "user_avatar": True}):
            try:
                avatar_list.append({"avatar": i['user_avatar']})
                name_list.append(
                    {'name': i['user_name'], 'country': i['language']})
            except:
                pass
            if len(name_list) >= 1000:
                self.table_avatar.insert_many(avatar_list)
                self.table_name.insert_many(name_list)
                avatar_list = []
                name_list = []
                print('yes')
        if len(name_list) > 0:
            self.table_avatar.insert_many(avatar_list)
            self.table_name.insert_many(name_list)
        print('init_database fin')

    def choice_one(self, list: list):
        return list[[random.randint(0, len(list)-1), random.randint(0,
                                                                    len(list)-1), random.randint(0, len(list)-1)][random.randint(0, 2)]]

    def is_luck(self, rate):
        new = [i <= rate*100 for i in range(100)]
        random.shuffle(new)
        return self.choice_one(new)

    def luck_num(self, rate: dict):
        new = []
        sum = 0
        for k in rate:
            sum += int(rate[k]*300)
            for _ in range(int(rate[k]*300)):
                new.append(k)
        for _ in range(abs(300-sum)):
            new.append(1)
        random.shuffle(new)
        return self.choice_one(new)

    def load_shop_id(self):
        self.shop_ids = []
        self.shop_id_map = {}
        for i in self.table_shop_map.find(
                {'merchant_shop_id': {'$in': config.shop_ids}}, {'crawler_shop_id': True, 'merchant_shop_id': True}):
            self.shop_ids.append(i['crawler_shop_id'])
            self.shop_id_map[i['crawler_shop_id']] = i['merchant_shop_id']
            print('has load', i['merchant_shop_id'], '   ', len(self.shop_ids))

    def get_shop_id_by_crawler(self, crawler_shop_id):
        return self.shop_id_map[crawler_shop_id]

    def __load_shop(self, shop_id):
        if shop_id not in self.shop.keys():
            self.shop[shop_id] = self.table_shop.find_one({'shop_id': shop_id})
            self.sum_comment[shop_id] = 1
            print('has load shop len:',len(self.shop))
        else:
            self.sum_comment[shop_id] += 1

    def __load_tag(self, tag_id):
        if tag_id not in self.tag.keys():
            self.tag[tag_id] = self.table_shop_tag.find_one({'tag_id': tag_id})

    def __load_district(self, district_id):
        if district_id not in self.district.keys():
            self.district[district_id] = self.table_shop_district.find_one({
                'district_id': district_id})

    def load_commnet_shop_tag_district(self):
        comments_low = {}
        comments_normal = {}
        comments_high = {}
        self.comment = {}
        self.shop = {}
        self.tag = {}
        self.district = {}
        self.shop_types = {}
        self.sum_comment = {}
        #with ThreadPoolExecutor(max_workers=3) as t:
        for store_id in self.shop_ids:
            for i in self.table_middleware_review.find({'language': TR, 'store_id': {'$eq': store_id}}):
                self.__load__(i, comments_low,
                            comments_high, comments_normal)
        self.comment[LOW] = comments_low
        self.comment[NORMAL] = comments_normal
        self.comment[HIGH] = comments_high
        print('load comments finish \nhigh_len: {}\nnormal_len: {}\nlow_len: {}\nshop_len: {}'.format(
            len(comments_high), len(comments_normal), len(comments_low), len(self.shop)))

    def __load__(self, i, comments_low, comments_high, comments_normal):
        print("start")
        shop_id = self.get_shop_id_by_crawler(i['store_id'])
        self.__load_shop(shop_id)
        self.__load_comment_content(
            i, shop_id, comments_low, comments_high, comments_normal)
        try:
            self.__load_tag(self.shop[shop_id]['tag']['show'])
        except:
            pass
        try:
            self.__load_district(self.shop[shop_id]['district_id'])
        except:
            pass
        print("end")

    def __load_shop_types(self, shop_id, type_):
        if shop_id not in self.shop_types.keys():
            self.shop_types[shop_id] = []
        self.shop_types[shop_id].append(type_)

    def __load_comment_content(self, i: dict, shop_id: str, comments_low: dict, comments_high: dict, comments_normal: dict):
        if i['review_score'] in [1, 2]:
            if shop_id not in comments_low.keys():
                comments_low[shop_id] = []
            comments_low[shop_id].extend(
                [item for item in i['review'].split('.') if item != ''])
            self.__image_insert(LOW, comments_low[shop_id])
            self.__new_statement(
                LOW, shop_id, comments_low[shop_id])
            self.__load_shop_types(shop_id, LOW)
        if i['review_score'] in [5]:
            if shop_id not in comments_high.keys():
                comments_high[shop_id] = []
            comments_high[shop_id].extend(
                [item for item in i['review'].split('.') if item != ''])
            self.__image_insert(HIGH, comments_high[shop_id])
            self.__new_statement(
                HIGH, shop_id, comments_high[shop_id])
            self.__load_shop_types(shop_id, HIGH)
        if i['review_score'] in [4, 3]:
            if shop_id not in comments_normal.keys():
                comments_normal[shop_id] = []
            comments_normal[shop_id].extend(
                [item for item in i['review'].split('.') if item != ''])
            self.__image_insert(NORMAL, comments_normal[shop_id])
            self.__new_statement(
                NORMAL, shop_id, comments_normal[shop_id])
            self.__load_shop_types(shop_id, NORMAL)

    @ count_time("statement_rebuild")
    def statement_rebuild(self):
        sum = 0
        cs = 0
        for shop_id in self.shop:
            tmp = []
            max, min = self.get_max_min(shop_id)
            # max, min = 20, 30 #手动指定或者按照数量生成
            names, avatars = self.get_database_avatar_name(
                self.shop[shop_id]['country'], max*2)
            for i in range(self.choice_one(range(min, max))):  # 生成几条评论
                type_ = self.choice_one(self.shop_types[shop_id])
                string = self.__build(self.__rand_shop_statement(
                    shop_id, type_))
                string = self.word_replace(
                    string, self.shop[shop_id]['country'])
                print('has cache : ', len(tmp))
                try:
                    name = names[i]
                    avatar = avatars[i]
                    country = self.shop[shop_id]['country']
                    tmp.append(data_pb2.Comment(
                        user_name=name, user_avatar=avatar, score=self.get_star(type_), content=string, store_id=shop_id, country=country, status='valid', type='normal'))
                except BaseException as err:
                    print(err)
                    print(i, len(names), len(avatars))
            self.create_comments(tmp)
            sum += len(tmp)
            cs += 1
            print('has commit : {}has create shop len : {}'.format(sum, cs))

    def get_max_min(self, shop_id):
        sum = self.sum_comment[shop_id]
        return sum, max(int(sum*0.5), 0)

    def word_replace(self, statement: str, country):
        for k in self.word[country]:
            statement = statement.replace(
                k, self.choice_one(self.word[country][k]))
        return statement

    def get_star(self, type_):
        star = "1"
        if type_ == HIGH:
            star = "5"
        elif type_ == NORMAL:
            star = self.choice_one(["3", "4"])
        elif type_ == LOW:
            star = self.choice_one(["2", "1"])
        return star

    def get_database_avatar_name(self, country, size):
        curosr = self.table_avatar.aggregate([{'$sample': {'size': size}}])
        avatars = []
        names = []
        for i in curosr:
            avatars.append(i['avatar'])
        curosr = self.table_name.aggregate(
            [{'$sample': {'size': size}}, {'$match': {'country': country}}])
        for i in curosr:
            names.append(i['name'])
        return names, avatars

    def __rand_shop_statement(self, shop_id, type):
        has = []
        for _ in range(self.luck_num({1: 0.1, 2: 0.3, 3: 0.3, 4: 0.2, 5: 0.1})):
            item = self.choice_one(self.comment[type][shop_id])
            has.append(item)
        random.shuffle(has)
        return list(set(has))

    def __build(self, list: list):
        string = ''
        i = 0
        while i < len(list)-1:
            if list[i].strip() != '':
                string += list[i].strip()
                if len(list[i+1]) > 4 and len(list[i]) > 3:
                    string += '.'
            i += 1
        string += list[i].strip()
        string += '.'
        return string

    def __image_insert(self, type_, list: list):
        images = self.image[type_]
        if self.is_luck(0.5):  # 表情插入概率
            size = random.randint(0, int(max(min(len(list)/2, 5), 1)))
            for _ in range(size):
                list.append(self.choice_one(images) *
                            self.luck_num({1: 0.8, 2: 0.2}))

    def __new_statement(self, type_, shop_id, list: list):
        if self.is_luck(1):
            for _ in range(self.luck_num({1: 0.1, 2: 0.4, 3: 0.5})):
                model = self.choice_one(
                    self.statement_model[self.shop[shop_id]['country']][type_])
                for key in self.statement_key:
                    if model.find(key) != -1:
                        model = self.statement_key[key](shop_id, model)
                list.append(model)

    def __handler_store_name(self, shop_id: str, model: str):
        return model.replace(KEY_STORE_NAME, self.shop[shop_id]['name'])

    def __handler_b_hour(self, shop_id: str, model: str):
        return model

    def __handler_street(self, shop_id: str, model: str):
        return model

    def __handler_tag(self, shop_id: str, model: str):
        tag = 'Restaurant'
        try:
            tag = self.tag[self.shop[shop_id]['tag']['show']]['name']
        except:
            pass
        return model.replace(KEY_TAG, tag)

    def __handler_location(self, shop_id: str, model: str):
        try:
            location = self.shop[shop_id]["location"]["detail"]
            model = model.replace(KEY_LOCATION, location)
        except:
            pass
        return model

    def __handler_district(self, shop_id: str, model: str):
        district = self.shop[shop_id]["location"]["city"]
        try:
            district = self.district[self.shop[shop_id]['district_id']]['name']
        except:
            pass
        model = model.replace(KEY_DISTRICT, district)
        return model

    def __handler_pct(self, shop_id: str, model: str):
        cfo = 20
        try:
            cfo = self.shop[shop_id]['cfo']
        except BaseException as err:
            pass
        return model.replace(KEY_PCT, str(cfo))

    def load_statement(self):
        self.statement_model = {TR: {
            LOW: config.tr_statement_1,
            NORMAL: config.tr_statement_2,
            HIGH: config.tr_statement_3,
        }}

        self.statement_key = {
            KEY_STORE_NAME: self.__handler_store_name, KEY_B_HOUR: self.__handler_b_hour, KEY_TAG: self.__handler_tag, KEY_LOCATION: self.__handler_location, KEY_DISTRICT: self.__handler_district, KEY_PCT: self.__handler_pct, KEY_STREET: self.__handler_street}

    def load_image(self):
        self.image = {}
        self.image[HIGH] = config.image_1
        self.image[NORMAL] = config.image_2
        self.image[LOW] = config.image_3

    def load_word(self):
        self.word = {TR: config.tr_word}

    def load_connect(self):
        self.connect = grpc.insecure_channel(rpc_url)

    def statistical_word_frequency(self):
        sum = 0
        statistical_word = {}
        statistical_word_2 = {}
        statistical_com_word = {}
        for i in self.table_comment.find(
                {'country': {'$in': [TR]}}, {"content": True, "_id": False}):
            sum += 1
            wards = []
            index = 0
            for j in i['content'].split('.'):
                if j != '':
                    for l in j.split(','):
                        if l != '':
                            for h in l.split(' '):
                                if h != '':
                                    wards.append(h)
            while index < len(wards):
                if wards[index]not in statistical_word.keys():
                    statistical_word[wards[index]] = 1
                else:
                    statistical_word[wards[index]] += 1
                if index > 0:
                    string_2 = '{} {}'.format(
                        wards[index-1], wards[index])
                    if string_2 not in statistical_word_2.keys():
                        statistical_word_2[string_2] = 1
                    else:
                        statistical_word_2[string_2] += 1
                if index > 0 and index < len(wards)-1:
                    string = '{} {} {}'.format(
                        wards[index-1], wards[index], wards[index+1])
                    if string not in statistical_com_word.keys():
                        statistical_com_word[string] = 1
                    else:
                        statistical_com_word[string] += 1
                index += 1
        statistical_word = sorted(
            statistical_word.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        statistical_word_2 = sorted(
            statistical_word_2.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        statistical_com_word = sorted(
            statistical_com_word.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        pd.DataFrame(statistical_com_word).to_csv('statistical_com_word.csv')
        pd.DataFrame(statistical_word).to_csv('statistical_word.csv')
        pd.DataFrame(statistical_word_2).to_csv('statistical_word_2.csv')
        # list = []
        # list_ = []
        # for k, v in statistical_word:
        #    list.append((k, v))
        #    if len(list) >= 2000:
        #        break
        # for k, v in statistical_com_word:
        #    list_.append((k, v))
        #    if len(list_) >= 2000:
        #        break
        # view.build(list, 'statistical_word')
        # view.build(list_, 'statistical_com_word')

    def statistical_word_shop(self):
        map = {}
        for i in self.table_comment.find({'language': TR}):
            s = i['content']
            shop_id = i['store_id']
            for word in config.tr_word_statistical:
                c = s.count(word)
                if c > 0:
                    if shop_id not in map.keys():
                        map[shop_id] = {word: c}
                    else:
                        map[shop_id][word] = c
        pd.DataFrame(map).to_csv('map.csv')

    def statistical_shop(self):
        list = []
        for shop in self.table_shop.find({'country': TR}):
            item = {}
            if 'shop_id' in shop.keys():
                item['shop_id'] = shop['shop_id']
            if 'priority' in shop.keys():
                item['priority'] = shop['priority']
            if 'name' in shop.keys():
                item['name'] = shop['name']
            if 'stars' in shop.keys():
                item['stars'] = shop['stars']
            list.append(item)
        pd.DataFrame(list).to_csv('shop.csv')


if __name__ == "__main__":
    Refiner()
