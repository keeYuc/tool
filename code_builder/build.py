#! /usr/bin/env python3
import re
def read():
    with open('main.go', 'r') as f:
        while True:
            line=f.readline()
            if line!='':
                do_(line)
            else:
                break
def do_(s):
    a = re.search('print\(', s)
    print(a)


read()



