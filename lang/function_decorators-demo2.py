# exception_decor.py
import logging

def create_logger():
    """
    Creates a logging object and returns it
    """
    logger = logging.getLogger("example_logger")
    logger.setLevel(logging.INFO)
    # create the logging file handler
    fh = logging.FileHandler("F:/Workspace/pythonProject/logTest/exceptoion.log")
    fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)
    # add handler to logger object
    logger.addHandler(fh)
    return logger

# def exception(function):
#     """
#     A decorator that wraps the passed in function and logs
#     exceptions should one occur
#     """
#     def wrapper(*args, **kwargs):
#         logger = create_logger()
#         try:
#             return function(*args, **kwargs)
#         except:
#             # log the exception
#             err = "There was an exception in  "
#             err += function.__name__
#             logger.exception(err)
#         # re-raise the exception
#         raise
#     return wrapper

# 将代码泛化成从外界传递一个logger对象到装饰器会更好些

import functools


def exception(logger):
    """
    A decorator that wraps the passed in function and logs
    exceptions should one occur

    @param logger: The logging object
    """

    def decorator(func):

        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                # log the exception
                err = "There was an exception in  "
                err += func.__name__
                logger.exception(err)

            # re-raise the exception
            raise

        return wrapper

    return decorator

# @exception
# def zero_divide():
#     1 / 0

logger = create_logger()
@exception(logger)
def zero_divide2():
    1 / 0
#
#
# print("让装饰器带参数3")
# print("---------------")
#
# from functools import wraps
# import logging
#
# def logged(level, name=None, msg=None):
#     def decorate(func):
#         logname = name if name else func.__name__
#         log = logging.getLogger(logname)
#         logmsg = msg if msg else func.__name__
#
#         @wraps(func)
#         def wrapper(*args,**kwargs):
#             log.log(level,logmsg)
#             return func(*args,**kwargs)
#         return wrapper
#     return decorate
#
# # exmaple use
# @logged(logging.DEBUG)
# def add(x,y):
#     return x+y
#
# add(1,2)
# print("---------------")


if __name__ == '__main__':
    # zero_divide()
    zero_divide2()


