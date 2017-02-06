# 先从 Python 的调用机制说起，我们如果调用一个属性，那么其顺序是：
# 优先从实例的 __dict__ 里查找，然后如果没有查找到的话，那么一次查询类字典，父类字典，直到彻底查不到为止。

# 其中如果在类实例字典中的该属性是一个 Data descriptors ，那么无论实例字典中存在该属性与否，无条件走描述符协议进行调用，
# 在类实例字典中的该属性是一个 Non-Data descriptors ，那么优先调用实例字典中的属性值而不触发描述符协议，
# 如果实例字典中不存在该属性值，那么触发 Non-Data descriptor 的描述符协议。

# 描述符  指的是实现了描述符协议的特殊的类，
# 三个描述符协议指的是 __get__ , ‘set‘ , __delete__ 以及 Python 3.6 中新增的 __set_name__ 方法，
# 其中实现了 __get__ 以及 __set__ / __delete__ / __set_name__ 的是 Data descriptors ，
# 而只实现了 __get__ 的是 Non-Data descriptor

# example 1
# 在我们的类 Exam 中，其 self.math 的调用过程是，首先在实例化后的实例的 __dict__ 中进行查找，
# 没有找到，接着往上一级，在我们的类 Exam 中进行查找，好的找到了，返回。
# 那么这意味着，我们对于 self.math 的所有操作都是对于类变量 math 的操作。因此造成变量污染的问题。


class Grade(object):
    def __init__(self):
        self._score = 0
    def __get__(self, instance, owner):
        return self._score
    def __set__(self, instance, value):
        if 0 <= value <= 100:
            self._score = value
        else:
            raise ValueError('grade must be between 0 and 100')
    def __str__(self):
        return 'score: '+ str(self._score)

class Exam(object):
    math = Grade()  # math 是类变量
    def __init__(self, math):
        self.math = math    # 类变量

if __name__ == '__main__':
    niche = Exam(math=90)
    print(niche.__dict__)

    print(Exam.__dict__['math'])

    print(niche.math)
    # output : 90
    snake = Exam(math=75)
    print(snake.__dict__)
    print(Exam.__dict__['math'])
    print(snake.math)
    # output : 75
    print(niche.math)
    # output : 75

    # snake.math = 120
    # output: ValueError:grade must be between 0 and 100!

# example 2
# 改良做法 1
# 利用 dict 的 key 唯一性，将具体的值与实例进行绑定，但是同时带来了内存泄露的问题。
# 那么为什么会造成内存泄露呢，首先复习下我们的 dict 的特性，dict 最重要的一个特性，就是凡可 hash 的对象皆可为 key ，
# dict 通过利用的 hash 值的唯一性（严格意义上来讲并不是唯一，而是其 hash 值碰撞几率极小，近似认定其唯一）来保证
# key 的不重复性，同时（敲黑板，重点来了），
# dict 中的 key 引用是强引用类型，会造成对应对象的引用计数的增加，可能造成对象无法被 gc ，从而产生内存泄露。

class Grad(object):
    def __init__(self):
        self._grade_pool = {}
    def __get__(self, instance, owner):
        return self._grade_pool.get(instance, None)
    def __set__(self, instance, value):
        if 0 <= value <= 100:
            _grade_pool = self.__dict__.setdefault('_grade_pool', {})
            _grade_pool[instance] = value
        else:
            raise ValueError("fuck")
# 解决方法 1
class Grad(object):
    def __init__(self):
        # weakref 库中的 WeakKeyDictionary 所产生的字典的 key 对于对象的引用是弱引用类型，
        # 其不会造成内存引用计数的增加，因此不会造成内存泄露。
        # 同理，如果我们为了避免 value 对于对象的强引用，我们可以使用 WeakValueDictionary 。
        import weakref
        self._grade_pool = weakref.WeakKeyDictionary()
    def __get__(self, instance, owner):
        return self._grade_pool.get(instance, None)
    def __set__(self, instance, value):
        if 0 <= value <= 100:
            _grade_pool = self.__dict__.setdefault('_grade_pool', {})
            _grade_pool[instance] = value
        else:
            raise ValueError("fuck")
# 解决方法 2
# 在 Python 3.6 中，实现的 PEP 487 提案，为描述符新增加了一个协议，我们可以用其来绑定对应的对象：
class Grad2(object):
    def __get__(self, instance, owner):
        return instance.__dict__[self.key]
    def __set__(self, instance, value):
        if 0 <= value <= 100:
            instance.__dict__[self.key] = value
        else:
            raise ValueError("fuck")
    def __set_name__(self, owner, name):
        self.key = name