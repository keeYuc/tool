import datetime


def decorator(class_):
    class wrapper():
        def __init__(self, *args, **kwargs):
            start_time = datetime.datetime.now()  # 程序开始时间
            self.wrapped = class_(*args, **kwargs)
            over_time = datetime.datetime.now()   # 程序结束时间
            total_time = (over_time-start_time).total_seconds()
            print('初始化共计%s秒' % total_time)

        def __getattr__(self, name):
            return getattr(self.wrapped, name)
    return wrapper


@decorator
class cls():
    def __init__(self, x, y):
        self.attrx = x
        self.attry = y

    def method(self):
        return self.attrx, self.attry


c = cls(3, 4)
print(c.attrx)
print(c.attry)
print(c.method())
