from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
import threading
import time

lock = threading.Lock()
a = [0]


def test(lock, a):
    lock.acquire()
    print('yes')
    a[0] += 1
    lock.release()


with ThreadPoolExecutor(max_workers=3) as t:
    t.submit(test, lock, a)
    t.submit(test, lock, a)
    t.submit(test, lock, a)
    t.submit(test, lock, a)
    t.submit(test, lock, a)
    t.submit(test, lock, a)



time.sleep(1)
print(a)
