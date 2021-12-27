import threading
import time
import sys


class NoLockExecutor:
    def __init__(self):
        self.task_map = {}

    def add(self, k, fn, args):
        if k not in self.task_map.keys():
            self.task_map[k] = Tasks()
        self.task_map[k].add(fn, args)

    def wait(self):
        while True:
            done = 0
            for i in self.task_map:
                if self.task_map[i].is_all_done():
                    done += 1
                else:
                    break
            if done == len(self.task_map):
                return
            else:
                time.sleep(0.1)


class Tasks:
    def __init__(self):
        self.tasks = []
        self.args = []
        self.fin_num = 0
        self.tasks_num = 0
        self.lock = threading.Lock()
        self.__run()

    def __run(self):
        handler = threading.Thread(target=self.__do_task)
        handler.start()
        self.handler = handler

    def done(self):
        self.handler._stop()

    def __do_task(self):
        while True:
            try:
                self.lock.acquire()
                fn = self.tasks.pop()
                args = self.args.pop()
                self.lock.release()
                fn(args)
                self.__done()
            except:
                self.lock.release()
                time.sleep(0.1)

    def __done(self):
        self.fin_num += 1

    def add(self, fn, args):
        self.tasks_num += 1
        self.lock.acquire()
        self.tasks.append(fn)
        self.args.append(args)
        self.lock.release()

    def is_all_done(self):
        return self.tasks_num == self.fin_num
