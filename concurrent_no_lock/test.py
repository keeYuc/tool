import NoLockExecutor as ex
import threading
import time


def a(s):
    print(s)


e = ex.NoLockExecutor()
e.add('1', a, (1))
e.add('1', a, (1.1))
e.add('2', a, (2))
e.add('2', a, (2.1))


e.wait()

print('yes')
