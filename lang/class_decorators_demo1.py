# 类修饰器
import numbers


# demo 1

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


def ensure(name, validate, doc=None):
    def decorator(Class):
        privateName = "__" + name

        # 返回对象的属性值，如果没有就抛出AttributeError
        def getter(self):
            return getattr(self, privateName)

        def setter(self, value):
            validate(name, value)
            return setattr(self, privateName, value)

        # 新建一个属性
        setattr(Class, name, property(getter, setter, doc=doc))
        return Class

    return decorator


@ensure("title", is_not_empty_str)
@ensure("quantity", is_in_range(0, 10000))
class Book:
    def __init__(self, title, isbn, price, quantity):
        self.title = title
        self.isbn = isbn
        self.price = price
        self.quantity = quantity

    @property
    def value(self):
        return self.price * self.quantity

book = Book('test',123,123,1000)
print(book.value)