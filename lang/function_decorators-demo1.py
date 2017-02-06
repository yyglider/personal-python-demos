'''
@functools.wraps 修饰器来保证wrapper()函数的__name__,docstring不会丢失，
在编写修饰器时，最好总是用该修饰器来修饰wrapper()函数，这样就能在trackback中打印出受修饰的原函数名了
'''

import functools

# 类型检查修饰器

# 若想创建参数化的修饰器，则先要创建修饰器工厂，由工厂来创建能修饰器，再由修饰器来创建包装函数

# 套路like this：
# print("让装饰器带参数1")
# def deco4(arg):
#     def _deco(func):
#         def __deco():
#             print("before %s called [%s]." % (func.__name__, arg))
#             func()
#             print("before %s called [%s]." % (func.__name__, arg))
#         return __deco
#     return _deco


def statically_typed(*types,return_type=None):
    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args,**kwargs):
            if len(args) > len(types):
                raise ValueError('too many arguments')
            elif len(args) < len(types):
                raise ValueError('too few arguments')
            for i, (arg,type_) in enumerate(zip(args,types)):
                print(i,arg,type_)
                if not isinstance(arg,type_):
                    raise ValueError('argument {} must be of type {}'.format(i,type.__name__))
            result = function(*args,**kwargs)
            if return_type is not None and not isinstance(result,return_type):
                raise ValueError('return value must be of type {}'.format(return_type.__name__))
            return result
        return wrapper
    return decorator

import html

@statically_typed(str,str,return_type=str)
def make_taggerd(text,tag):
    return "<{0}>{1}</{0}>".format(tag,html.escape(text))

print(make_taggerd('test','br'))


# 无参数的修饰器

# 创建修饰器函数，然后在函数里创建并返回包装函数即可。
def float_args_and_return(function):
    @functools.wraps(function)
    def wrapper(*args,**kwargs):
        args = [float(arg) for arg in args]
        return float(function(*args,**kwargs))
    return wrapper