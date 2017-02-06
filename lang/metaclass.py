# metaclass允许你创建类或者修改类。换句话说，你可以把类看成是metaclass创建出来的“实例”。

# 我们先看一个简单的例子，这个metaclass可以给我们自定义的MyList增加一个add方法：

# metaclass是类的模板，所以必须从`type`类型派生：
# __new__()方法接收到的参数依次是：
# 当前准备创建的类的对象；
# 类的名字；
# 类继承的父类集合；
# 类的方法集合。
class ListMetaclass(type):
    def __new__(cls, name, bases, attrs):
        attrs['add'] = lambda self, value: self.append(value)
        return type.__new__(cls, name, bases, attrs)

# 有了ListMetaclass，我们在定义类的时候还要指示使用ListMetaclass来定制类，传入关键字参数metaclass：
# 当我们传入关键字参数metaclass时，它指示Python解释器在创建MyList时，要通过ListMetaclass.__new__()来创建，
# 在此，我们可以修改类的定义，比如，加上新的方法，然后，返回修改后的定义。
class MyList(list, metaclass=ListMetaclass):
    pass


L =  MyList()
L.add(1)
print(L)