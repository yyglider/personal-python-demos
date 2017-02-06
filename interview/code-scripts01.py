# demo1 列表反转
# 如果是一个list
temp_list = [1,2,3,4]
temp_list.reverse()
for x in temp_list:
    print(x)

# 如果不是list
temp_tuple = (1,2,3,4)
for i in range(len(temp_tuple)-1, -1, -1):
    print(temp_tuple[i])


# demo2 查询和替换一个文本字符串
# 使用replace进行字符串替换
temp_str = 'hello python'
print(temp_str.replace('hello','bye'))
# 使用sub，通过正则来匹配
import re
rex =  r'(hello|use)'
print(re.sub(rex,'bye',temp_str))

# demo3 重新实现str.strip()
def rightStrip(tempStr, splitStr):
    endindex = tempStr.rfind(splitStr)
    print(endindex)
    while endindex != -1 and endindex == len(tempStr) - 1:
        tempStr = tempStr[:endindex]
        endindex = tempStr.rfind(splitStr)
        print(endindex)
    return tempStr

def leftStrip(tempStr, splitStr):
    beginindex = tempStr.find(splitStr)
    while beginindex == 0:
        tempStr = tempStr[beginindex+1:]
        beginindex = tempStr.find(splitStr)
    return  tempStr

str = '  hello world    '
print(len(str))
print(rightStrip(str,' '))
print(leftStrip(str,' '))

# demo4  函数参数传递
# Python中string、tuple、number属于不可更改对象，而list和dict属于可修改对象。
a = 1
def func(a):
    a = 2

func(a)
print(a) # 1

a = []
def func(a):
    a.append(1)

func(a)
print(a)

# demo5 类变量和实例变量
# 上半部分：name是字符串（不可更改对象），实例变量p1.name一开始指向了类变量name="aaa"，
# 但是在实例的作用域把类变量的引用改变了，就变成了一个实例变量self.name不再引用Person的类变量name
class Person:
    name = 'aaa'

p1 = Person()
p2 = Person()
p1.name = 'bbb'
print(p1.name) # bbb
print(p2.name) # aaa
print(Person.name) # aaa

# name是list（可更改对象）
class Person:
    name = []

p1 = Person()
p2 = Person()
p1.name.append(1)
print(p1.name) # [1]

# demo6





