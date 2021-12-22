from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
import time
import threading


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
