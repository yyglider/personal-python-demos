# __new__和__init__的区别。
#
# __init__为初始化方法，__new__方法是真正的构造函数。
# __new__是实例创建之前被调用，它的任务是创建并返回该实例，是静态方法
# __init__是实例创建之后被调用的，然后设置对象属性的一些初始值。
#
# 总结：__new__方法在__init__方法之前被调用，并且__new__方法的返回值将传递给__init__方法作为第一个参数，
# 最后__init__给这个实例设置一些参数。

class TestClass(object):

    def __new__(cls,*args,**kwargs):
        print('__new__')
        return super().__new__(cls)
        # return super(TestClass,cls).__new__(cls)

    def __init__(self,name):
        print('__init__')
        self.name = name

t = TestClass('hello')
print(t.name)


# Python中单下划线和双下划线分别是什么？
# __name__：一种约定，Python内部的名字，用来与用户自定义的名字区分开，防止冲突
# _name：一种约定，用来指定变量私有
# __name：解释器用_classname__name来代替这个名字用以区别和其他类相同的命名

class TestClass2:
    a = 1
    _b = 2
    __c = 3

t2 = TestClass2()
print(t2.a)
print(t2._b)
print(t2._TestClass2__c)
# print(t2.__c)

