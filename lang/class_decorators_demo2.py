# demo 2
# 用类修饰器新增属性

# 把相关的attribute都放在类里面，然后只用一个类修饰器来修饰

# 保存验证器函数，相关属性的setter函数稍后会用到这个验证器
import numbers

class Ensure:
    def __init__(self, validate, doc=None):
        self.validate = validate
        self.doc = doc


# do_ensure修饰器就是把每个Ensure是列都替换成对应的属性
def do_ensure(Class):
    def make_property(name, attribute):
        privateName = '__' + name

        # getattr(object, name[,default]), 获取对象object的属性或者方法，如果存在打印出来，如果不存在，打印出默认值，默认值可选。
        # 需要注意的是，如果是返回的对象的方法，返回的是方法的内存地址，如果需要运行这个方法，
        def getter(self):
            return getattr(self, privateName)

        def setter(self, value):
            attribute.validate(name,value)
            return setattr(self, privateName, value)

        # 返回一个属性，该属性会把保其值保存在私有的attribute中
        # 比如title属性就保存名为__title的属性中，属性的setter函数还会调用原来的的Ensure实例的验证器函数
        return property(getter, setter, doc=attribute.doc)

    # 遍历类中的每一个attribute,并用新属性代替原来的Ensure
    for name, attribute in Class.__dict__.items():
        if isinstance(attribute, Ensure):

            setattr(Class, name, make_property(name, attribute))
            print(Class.__dict__[name])

    return Class


# validate function
def is_not_empty_str(name, value):
    if not isinstance(value, str):
        raise ValueError("{} must be of tye str".format(name))
    if not bool(value):
        raise ValueError("{} may not be empty".format(name))


# 工厂函数，每次调用都会创建新的验证器函数
def is_in_range(min=None, max=None):
    assert min is not None and max is not None

    def is_in_range(name, value):
        if not isinstance(value, numbers.Number):
            raise ValueError("{} must be a number")
        if min is not None and value < min:
            raise ValueError("{} {} is too small".format(name, value))
        if max is not None and value > max:
            raise ValueError("{} {} is too big".format(name, value))

    return is_in_range


@do_ensure
class Book:
    title = Ensure(is_not_empty_str)
    quantity = Ensure(is_in_range(1,100))

    def __init__(self, title, isbn, price, quantity):
        self.title = title
        self.isbn = isbn
        self.price = price
        self.quantity = quantity

    @property
    def value(self):
        return self.price * self.quantity


book = Book('test', 123, 123, 10000000)
print(book.value)
