# 单例模式
# 方法1 使用__new__方法

# 在__new__方法中把类实例绑定到类变量_instance上，如果cls._instance为None表示该类还没有实例化过，
# 实例化该类并返回。如果cls_instance不为None表示该类已实例化，直接返回cls_instance

class SingleTon1(object):

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls,'_instance'):
            cls._instance = object.__new__(cls,*args,**kwargs)
            print(cls._instance)
        return cls._instance

class Testclass1(SingleTon1):
    a = 1

test1 = Testclass1()
test2 = Testclass1()

print(test1.a,test2.a)

test1.a = 2

print(test1.a,test2.a)


# 方法2 使用装饰器(decorator)
def SingleTon2(cls,*args,**kwargs):
    instances = {}
    def _singleton2():
        if cls not in instances:
            instances[cls] = cls(*args,**kwargs)
        return instances[cls]
    return _singleton2

@SingleTon2
class Testclass2(object):
    a = 3

test3 = Testclass2()
test4 = Testclass2()

print(test3.a,test4.a)

test3.a = 4

print(test3.a,test4.a)


# 方法3 使用__metaclass__（元类）
# class SingleTon3(type):
#     def __init__(cls,name,bases,dict):
#         super(SingleTon3,cls).__init__(name,bases,dict)
#         cls._instance = None
#
#     def __call__(cls, *args, **kwargs):
#         if cls._instance is None:
#             cls._instance = super(SingleTon3,cls).__call__(*args,**kwargs)
#         return cls._instance
#
# class Testclass3(object):
#     __metaclass__ = SingleTon3
#     a = 6
#
# test5 = Testclass3()
# test6 = Testclass3()
# test5.a = 5
# print(test5.a,test6.a)

# 方法4 共享属性

# 所谓单例就是所有的引用（实例，对象）拥有相同的属性和方法，同一个类的实例天生都会有相同的方法，
# 那我们只需要保证同一个类所产生的实例都具有相同的属性。所有实例共享属性最简单直接的方法就是共享__dict__属性指向。

class SingleTon4(object):
    _state = {}
    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls,*args,**kwargs)
        obj.__dict__ = cls._state
        return obj
