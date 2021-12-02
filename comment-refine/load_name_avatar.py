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
        self.load_statement()
        self.load_commnet_avatar_shop_tag_district()
        self.load_image()
        self.statement_rebuild()

    def load_statement(self):
        self.statement_model = [
            '(store_name),,,,,(business_hours).....(tag)......(location).......(shopping_district).......(per_customer_transaction)']
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

    def load_commnet_avatar_shop_tag_district(self):
        comments_low = {}
        comments_normal = {}
        comments_high = {}
        self.names = []
        self.avatar = []
        self.comment = {}
        self.shop = {}
        self.tag = {}
        self.district = {}
        self.statement_shop = {}
        for i in self.table_comment.find().limit(1000):
            for name in i['user_name'].strip().split(' '):
                if len(name) < 10 and len(name) > 3:
                    self.names.append(name)
            if i['score'] in ['1.0', '2.0']:
                comments_low[i['id']] = i
            if i['score'] in ['5.0']:
                comments_high[i['id']] = i
            if i['score'] in ['4.0', '3.0']:
                comments_normal[i['id']] = i
            self.avatar.append(i['user_avatar'])
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
        self.avatar_index = [i for i in range(len(self.avatar))]
        random.shuffle(self.avatar_index)
        print('load comments finish \nhigh_len: {}\nnormal_len: {}\nlow_len: {}\nshop_len: {}'.format(
            len(comments_high), len(comments_normal), len(comments_low), len(self.shop)))

    def rand_name_EN(self):
        name = ''
        for i in range(random.randint(4, 10)):
            if random.randint(1, 10) % 3 == 0:
                name += chr(random.randint(65, 90))
            else:
                name += chr(random.randint(97, 122))
        return name

    def statement_rebuild(self):
        index = 0
        model = "same-shop"  # same-shop  statement
        for i in self.comment:
            for j in self.comment[i]:
                tmp = [i for i in self.comment[i][j]
                       ['content'].split('.') if i != '']
                self.__image_insert(i, tmp)
                self.comment[i][j]['user_avatar'] = self.avatar_random(
                    index)
                # self.__new_statement(
                # self.comment[i][j]['store_id'], tmp)  # 语句模板
                if model == "full-random":
                    random.shuffle(tmp)
                    tmp = self.__random_statement(tmp)
                    self.comment[i][j]['content'] = self.__build(tmp)
                elif model == "same-shop":
                    self.__load_shop_statement(
                        self.comment[i][j]['store_id'], i, tmp)
                elif model == "statement":
                    pass
                index += 1
        if model == "same-shop":
            for i in self.comment:
                for j in self.comment[i]:
                    self.comment[i][j]['content'] = self.__build(self.__rand_shop_statement(
                        self.comment[i][j]['store_id'], i))
                    self.table_refine_comment.insert_one(
                        self.comment[i][j])

    def __rand_shop_statement(self, shop_id, type):
        has = []
        for _ in range(self.luck_num({2: 0.1, 3: 0.2, 4: 0.25, 5: 0.25, 6: 0.1, 7: 0.1})):
            item = self.choice_one(self.statement_shop[shop_id][type])
            has.append(item)
        return list(set(has))

    def __load_shop_statement(self, shop_id, type, list: list):
        if shop_id not in self.statement_shop.keys():
            self.statement_shop[shop_id] = {type: list}
        elif type not in self.statement_shop[shop_id].keys():
            self.statement_shop[shop_id][type] = list
        else:
            self.statement_shop[shop_id][type].extend(list)

    def __random_statement(self, list: list):
        # todo 改变乱序算法
        hand = list[0: 1]
        back = list[1:]
        random.shuffle(back)
        hand.extend(back)
        return hand

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
        if self.is_luck(0.8):  # 表情插入概率
            size = random.randint(0, int(max(min(len(list)/2, 2), 1)))
            for _ in range(size):
                list.append(self.choice_one(images) *
                            self.luck_num({1: 0.75, 2: 0.15, 3: 0.1}))
                random.shuffle(list)

    def avatar_random(self, index):
        return self.avatar[self.avatar_index[index]]

    def __new_statement(self, shop_id, list: list):
        if self.is_luck(0.6):
            model = self.choice_one(self.statement_model)
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
