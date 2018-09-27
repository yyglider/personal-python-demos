# coding=utf-8
from collections import defaultdict

defaults = defaultdict(lambda :0)
defaults["tester"] += 1
print(defaults)