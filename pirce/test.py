import copy
a = {}


b = copy.deepcopy(a)


a['a'] = 1


print(a)
print(b)
