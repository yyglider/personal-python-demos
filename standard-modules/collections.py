# Counter: 计数器
# OrderedDict: 有序字典
# defaultdict: 带有默认值的字典
# namedtuple: 生成可以通过属性访问元素内容的 tuple 子类
# deque: 双端队列，能够在队列两端添加或删除元素

from collections import Counter

s = "aaaabbbcc"
c = Counter(s)
print(c)

from collections import ChainMap

a = {'a': 'A', 'c': 'C'}
b = {'b': 'B', 'c': 'D'}
m = ChainMap(a, b)
print(m)