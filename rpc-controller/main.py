#!/Users/keeyu/homebrew/bin/python3

import os
import re


class controller:
    def __init__(self, path=[]):
        self.files = []
        self.prefix = './protocol/grpc'
        self.__load_path(path, self.prefix)

    def __load_path(self, path, o):
        for i in path:
            if os.path.isdir(o+'/'+i):
                self.__load_path(os.listdir(o+'/'+i), o+'/'+i)
            else:
                self.files.append(o+'/'+i)

    def __read(self, path):
        with open(path, 'r') as f:
            return f.readlines()

    def __match(self, lines):
        for i in lines:
            res = re.search('Invoke', i)
            if res != None:
                print(res)

    def test(self):
        print(self.files)
        print(self.files[1])
        self.__match(self.__read(self.files[1]))


a = controller(['merchant'])
a.test()
