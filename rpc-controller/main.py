#!/Users/keeyu/homebrew/bin/python3

import os


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
            return f.read()

    def test(self):
        print(self.files)
        print(self.__read(self.files[0]))


a = controller(['balance'])
a.test()
