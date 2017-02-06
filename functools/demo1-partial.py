import functools

'''
which can be used to “wrap” a callable object with default arguments.
The resulting object is itself callable,
and can be treated as though it is the original function.
It takes all of the same arguments as the original,
and can be invoked with extra positional or named arguments as well.


其实就是函数调用的时候，有多个参数，但是其中的一个参数已经知道了，
我们可以通过这个参数重新绑定一个新的函数，然后去调用这个新函数。

functools.partial(func, *args, **keywords)，函数装饰器，返回一个新的partial对象。
调用partial对象和调用被修饰的函数func相同，只不过调用partial对象时传入的参数个数通
常要少于调用func时传入的参数个数。

当一个函数func可以接收很多参数，而某一次使用只需要更改其中的一部分参数，
其他的参数都保持不变时，partial对象就可以将这些不变的对象冻结起来，
这样调用partial对象时传入未冻结的参数，partial对象调用func时连同已经
被冻结的参数一同传给func函数，从而可以简化调用过程。

如果调用partial对象时提供了更多的参数，那么他们会被添加到args的后面，
如果提供了更多的关键字参数，那么它们将扩展或者覆盖已经冻结的关键字参数。


'''

#args/keywords 调用partial时参数

# def partial(func, *args, **keywords):
#     def newfunc(*fargs, **fkeywords):
#         newkeywords = keywords.copy()
#         newkeywords.update(fkeywords)
#         return func(*(args + fargs), **newkeywords)
#     #合并，调用原始函数，此时用了partial的参数
#     newfunc.func = func
#     newfunc.args = args
#     newfunc.keywords = keywords
#     return newfunc
#
# 声明：
# urlunquote = functools.partial(urlunquote, encoding='latin1')
# 当调用 urlunquote(args, *kargs) 相当于 urlunquote(args, *kargs, encoding='latin1')

import functools

def add(a, b):
    return a + b



plus3 = functools.partial(add, 3)
plus5 = functools.partial(add, 5)

print(plus3(0))
print(plus3(1))
print(plus5(1))

# -----------------------------------------------

def myfunc(a, b=2):
    "Docstring for myfunc()."
    print('  called myfunc with:', (a, b))


def show_details(name, f, is_partial=False):
    "Show details of a callable object."
    print('{}:'.format(name))
    print('  object:', f)
    if not is_partial:
        print('  __name__:', f.__name__)
    if is_partial:
        print('  func:', f.func)
        print('  args:', f.args)
        print('  keywords:', f.keywords)
    return


show_details('myfunc', myfunc)
myfunc('a', 3)
print()

# Set a different default value for 'b', but require
# the caller to provide 'a'.
p1 = functools.partial(myfunc, b=4)
show_details('partial with named default', p1, True)
p1('passing a')
p1('override b', b=5)
print()

# Set default values for both 'a' and 'b'.
p2 = functools.partial(myfunc, 'default a', b=99)
show_details('partial with defaults', p2, True)
p2()
p2(b='override b')
print()

print('Insufficient arguments:')
p1()
