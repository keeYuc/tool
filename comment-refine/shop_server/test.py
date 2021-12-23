from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
import time
import threading
import pandas as pd


def fuck():
    pass


lock = threading.Lock()
a = {}


def tet(i):
    lock.acquire()
    print(i)
    a[i] = i
    lock.release()


list = []
with ThreadPoolExecutor(max_workers=3) as t:
    for i in range(100):
        list.append(t.submit(tet, (i)))


wait(list, return_when=ALL_COMPLETED)
print(len(a))
print(type('stradfaf'))


a = {'a': [1], 'b': [2]}
pd.DataFrame(a).to_csv('shop_service.csv')
