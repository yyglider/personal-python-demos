import chardet

path = 'D:/006564/Desktop/new2.txt'
#
# fp = open(path,'r')
# tt = fp.read()
# encoding = chardet.detect(tt)
# print(encoding)
#
#




#
# content = fp.read().encode('utf-8')
#
# for lines in content:
#     print(lines.strip())

with open(path,'r') as file:
    for lines in file:
        print(lines)

# a=0
# a_set = set()
# a_dict = dict()
# with open(path,'r') as file:
#     for lines in file:
#         # field2 = lines.strip().split(' ')[1]
#         # field1 = lines.strip().split(' ')[0]
#         # print(field2)
#         # a = a + int(field2)
#         if len(lines)<3:
#             pass
#         else:
#             # print(lines)
#             # field1 = lines.strip().split()[0]
#             # field2 = lines.strip().split()[1]
#             # a_set.add(field1)
#             # a_dict[field1]=field2
#             a_set.add(lines.strip())
#
# path2 = 'D:/006564/Desktop/special.txt'
# with open(path2,'r') as file2:
#     for lines in file2:
#         if lines.strip() in a_set:
#             a=a+1
#             print(lines.strip())
#             # print(lines.strip(),a_dict[lines.strip()])
# print('sum',a)
#

