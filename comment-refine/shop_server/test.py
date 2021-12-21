from concurrent.futures import ThreadPoolExecutor
import time
import threading

lock = threading.Lock()
a={}
def tet(i):
    lock.acquire()
    print(i)
    a[i]=i
    lock.release()


with ThreadPoolExecutor(max_workers=3) as t:
    for i in range(100):
        t.submit(tet,(i))

print(len(a))
time.sleep(3)