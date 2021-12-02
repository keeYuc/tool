import pymongo
import random
import datetime
uri = "mongodb://root:8DNsidknweoRGwSbWgDN@localhost:27019"
database = "content"
HIGH = 'high'
NORMAL = 'normal'
LOW = 'low'
KEY_STORE_NAME = '(store_name)'
KEY_B_HOUR = '(business_hours)'
KEY_TAG = '(tag)'
KEY_LOCATION = '(location)'
KEY_DISTRICT = '(shopping_district)'
KEY_PCT = '(per_customer_transaction)'


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
        self.table_comment = myclient[database]["comment"]
        self.table_shop = myclient[database]["shop"]
        self.table_shop_tag = myclient[database]["shop_tag"]
        self.table_shop_district = myclient[database]["shop_district"]
        self.table_refine_comment = myclient[database]["refine_comment"]
        self.table_avatar = myclient[database]["avatar"]
        self.table_name = myclient[database]["name"]
        # self.init_database()
        self.load_statement()
        self.load_image()
        self.load_commnet_shop_tag_district()
        self.statement_rebuild()

    def init_database(self):
        avatar_list = []
        name_list = []
        for i in self.table_comment.find(
                {}, {"country": True, "user_name": True, "user_avatar": True}):
            avatar_list.append({"avatar": i['user_avatar']})
            name_list.append({'name': i['user_name'], 'country': i['country']})
            if len(name_list) >= 1000:
                self.table_avatar.insert_many(avatar_list)
                self.table_name.insert_many(name_list)
                avatar_list = []
                name_list = []
        if len(name_list) > 0:
            self.table_avatar.insert_many(avatar_list)
            self.table_name.insert_many(name_list)
        print('init_database fin')

    def load_statement(self):
        self.statement_model = {
            LOW: ['(store_name),,,,,(business_hours).....(tag)......(location).......(shopping_district).......(per_customer_transaction)'],
            NORMAL: ['(store_name), , '],
            HIGH: ['..(tag)..']
        }

        self.statement_key = {
            KEY_STORE_NAME: self.__handler_store_name, KEY_B_HOUR: self.__handler_b_hour, KEY_TAG: self.__handler_tag, KEY_LOCATION: self.__handler_location, KEY_DISTRICT: self.__handler_district, KEY_PCT: self.__handler_pct}

    def choice_one(self, list: list):
        return list[random.randint(0, len(list)-1)]

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

    def __load_shop(self, shop_id):
        if shop_id not in self.shop.keys():
            self.shop[shop_id] = self.table_shop.find_one({'shop_id': shop_id})

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
        for i in self.table_comment.find({'store_id': {'$in': ['2113e27d-6ee2-48c1-aac2-81cd4bce8099']}}):
            self.__load_comment_content(
                i, comments_low, comments_high, comments_normal)
            self.__load_shop(i['store_id'])
            try:
                self.__load_tag(self.shop[i['store_id']]['tag']['show'])
            except:
                pass
            try:
                self.__load_district(self.shop[i['store_id']]['district_id'])
            except:
                pass
        self.comment[LOW] = comments_low
        self.comment[NORMAL] = comments_normal
        self.comment[HIGH] = comments_high
        print('load comments finish \nhigh_len: {}\nnormal_len: {}\nlow_len: {}\nshop_len: {}'.format(
            len(comments_high), len(comments_normal), len(comments_low), len(self.shop)))

    def __load_shop_types(self, shop_id, type_):
        if shop_id not in self.shop_types.keys():
            self.shop_types[shop_id] = []
        self.shop_types[shop_id].append(type_)

    def __load_comment_content(self, i: dict, comments_low: dict, comments_high: dict, comments_normal: dict):
        if i['score'] in ['1.0', '2.0']:
            if i['store_id'] not in comments_low.keys():
                comments_low[i['store_id']] = []
            comments_low[i['store_id']].extend(
                [item for item in i['content'].split('.') if item != ''])
            self.__image_insert(LOW, comments_low[i['store_id']])
            self.__new_statement(
                LOW, i['store_id'], comments_low[i['store_id']])
            self.__load_shop_types(i['store_id'], LOW)
        if i['score'] in ['5.0']:
            if i['store_id'] not in comments_high.keys():
                comments_high[i['store_id']] = []
            comments_high[i['store_id']].extend(
                [item for item in i['content'].split('.') if item != ''])
            self.__image_insert(HIGH, comments_high[i['store_id']])
            self.__new_statement(
                HIGH, i['store_id'], comments_high[i['store_id']])
            self.__load_shop_types(i['store_id'], HIGH)
        if i['score'] in ['4.0', '3.0']:
            if i['store_id'] not in comments_normal.keys():
                comments_normal[i['store_id']] = []
            comments_normal[i['store_id']].extend(
                [item for item in i['content'].split('.') if item != ''])
            self.__image_insert(NORMAL, comments_normal[i['store_id']])
            self.__new_statement(
                NORMAL, i['store_id'], comments_normal[i['store_id']])
            self.__load_shop_types(i['store_id'], NORMAL)

    def statement_rebuild(self):
        for shop_id in self.shop:
            for _ in range(self.choice_one(range(40, 50))):  # 生成几条评论
                type_ = self.choice_one(self.shop_types[shop_id])
                string = self.__build(self.__rand_shop_statement(
                    shop_id, type_))
                print('\n--------{}---------'.format(type_)+string)
            return

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
        return
        if self.is_luck(0.0):
            model = self.choice_one(self.statement_model[type_])
            for key in self.statement_key:
                if model.find(key) != -1:
                    model = self.statement_key[key](shop_id, model)
            list.append(model)

    def __handler_store_name(self, shop_id: str, model: str):
        return model.replace(KEY_STORE_NAME, self.shop[shop_id]['name'])

    def __handler_b_hour(self, shop_id: str, model: str):
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

    def load_image(self):
        self.image = {}
        self.image[HIGH] = ['😀',
                            '😄',
                            '😁',
                            '😊',
                            '😇',
                            '🥰',
                            '😍',
                            '😋',
                            '😚',
                            '🤗',
                            '💖',
                            '💯',
                            '👍',
                            '🤤',
                            '😺',
                            '🤞',
                            '😀👍',
                            '🙍',
                            '🙆',
                            '🍔',
                            '🍕',
                            '🍴',
                            '🥄',
                            '🔪',
                            '🌝',
                            '⭐',
                            '🎉',
                            '🏆',
                            '🥇',
                            '🙋‍♀️🥄',
                            '🙆🍴',
                            '😀',
                            '😄',
                            '😁',
                            '😊',
                            '😇',
                            '🥰',
                            '😍',
                            '😋',
                            '😚',
                            '🤗',
                            '😋👍',
                            '😁👍',
                            '😋🙋‍♀️']
        self.image[NORMAL] = ['🙂',
                              '😛',
                              '😏',
                              '🤣',
                              '🤪',
                              '🤗',
                              '🤤',
                              '🤓',
                              '🤡',
                              '😺',
                              '✌',
                              '😀☝',
                              '😀👏',
                              '👩',
                              '🙋‍♀️',
                              '🐵',
                              '🍔',
                              '🍕',
                              '🍴',
                              '🥄',
                              '🔪',
                              '🌝',
                              '⭐',
                              '🎉',
                              '🙋‍♀️🥄',
                              '🤤😀',
                              '🤗😛']
        self.image[LOW] = ['🤔',
                           '🤕',
                           '🤮',
                           '🙁',
                           '😭',
                           '😖',
                           '😩',
                           '😤',
                           '💢',
                           '👎',
                           '😑',
                           '😩',
                           '💩',
                           '💥',
                           '🤚',
                           '🤮😭',
                           '🤕💥',
                           '😤💢',
                           '🤔',
                           '🤕',
                           '🤮',
                           '🙁',
                           '😭',
                           '😖',
                           '😩',
                           '😤',
                           '💢',
                           '👎',
                           '😑',
                           '😩',
                           '💩']


if __name__ == "__main__":
    Refiner()
