import pymongo
import threading
import datetime
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
        pass
