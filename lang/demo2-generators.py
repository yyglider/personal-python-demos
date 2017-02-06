# 生成器记住上一次返回时这函数体中的位置，上次调用的所有局部变量都保持不变，迭代到下一次调用时，所使用的参数是上一次保留下的
# 本次运行直到出现yield语句

# demo 1
def fib(max):
    a, b = 1, 1
    while a < max:
        yield a # generators return an iterator that returns a stream of value
        a, b = b, a + b

for n in fib(15):
    print(n)

# demo 2
class Fib:
    def __init__(self,max):
        self.max = max
    def __iter__(self):
        self.a = 0
        self.b = 1
    def next(self):
        fib = self.a
        if fib > self.max:
            raise StopIteration
        self.a , self.b = self.b , self.a + self.b
        return fib


# demo 3 列表推导
L = [x * x for x in range(10)]

g = (x * x for x in range(10))
print(g.__next__())
print(g.__next__())
print(g.__next__())
print(g.__next__())

for n in g:
    print(n)