import ConcurrentExecutor as ex
import threading
import time


def a(s):
    print(s)


e = ex.ConcurrentExecutor()
e.add('1', a, (1.1))
e.add('1', a, (1.2))
e.add('2', a, (2.1))
e.add('2', a, (2.2))
e.add('3', a, (3.1))
e.add('3', a, (3.2))


e.wait()

print('yes')
