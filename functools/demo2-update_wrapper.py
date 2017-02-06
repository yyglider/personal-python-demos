# 默认partial对象没有__name__和__doc__, 这种情况下，对于装饰器函数非常难以debug.
# 使用update_wrapper(),从原始对象拷贝或加入现有partial对象
# 它可以把被封装函数的__name__、module、__doc__和 __dict__都复制到封装函数去
# (模块级别常量WRAPPER_ASSIGNMENTS, WRAPPER_UPDATES)
# 这个函数主要用在装饰器函数中，装饰器返回函数反射得到的是包装函数的函数定义而不是原始函数定义
import functools


def myfunc(a, b=2):
    "Docstring for myfunc()."
    print('  called myfunc with:', (a, b))


def show_details(name, f):
    "Show details of a callable object."
    print('{}:'.format(name))
    print('  object:', f)
    print('  __name__:', end=' ')
    try:
        print(f.__name__)
    except AttributeError:
        print('(no __name__)')
    print('  __doc__', repr(f.__doc__))
    print()


show_details('myfunc', myfunc)

p1 = functools.partial(myfunc, b=4)
show_details('raw wrapper', p1)

print('Updating wrapper:')
print('  assign:', functools.WRAPPER_ASSIGNMENTS)
print('  update:', functools.WRAPPER_UPDATES)
print()

functools.update_wrapper(p1, myfunc)
show_details('updated wrapper', p1)