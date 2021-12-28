import threading
import time
import sys
import queue


class ConcurrentExecutor:
    def __init__(self):
        self.task_map = {}
        self.flag = True
        self.__notify()

    def __notify(self):
        handler = threading.Thread(target=self.__do_notify)
        handler.start()
        self.handler = handler

    def __do_notify(self):
        while self.flag:
            for i in self.task_map:
                self.task_map[i].notify()
            time.sleep(0.05)
        for i in self.task_map:
            self.task_map[i].notify()
        print('note 线程退出')

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
                for i in self.task_map:
                    self.task_map[i].exit()
                self.flag = False
                return
            else:
                time.sleep(0.1)


class Tasks:
    def __init__(self):
        self.tasks = queue.Queue()
        self.args = queue.Queue()
        self.hand_index = 0
        self.tasks_num = 0
        self.flag = True
        self.cond = threading.Condition()
        self.__run()

    def __run(self):
        handler = threading.Thread(target=self.__do_task)
        handler.start()
        self.handler = handler

    def __do_task(self):
        while self.flag:
            self.__wait()
            for _ in range(self.tasks_num-self.hand_index):
                fn, args = self.__get_fn_args()
                fn(*args)
                self.__done()
                continue
        print('do 线程退出')

    def notify(self):
        self.cond.acquire()
        self.cond.notify()
        self.cond.release()

    def __wait(self):
        self.cond.acquire()
        self.cond.wait()
        self.cond.release()

    def __get_fn_args(self):
        fn = self.tasks.get()
        args = self.args.get()
        return fn, args

    def __done(self):
        self.hand_index += 1

    def add(self, fn, args):
        self.tasks.put(fn)
        self.args.put(args)
        self.tasks_num += 1
        self.notify()

    def exit(self):
        self.flag = False

    def is_all_done(self):
        return self.tasks_num == self.hand_index
