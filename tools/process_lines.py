import chardet
import datetime
from collections import OrderedDict, defaultdict

path = 'W:/页面升级.txt'
f = open(path,'r')

for lines in f:
    print(lines)

# wtls_path = 'D:/006564/Desktop/wtls.csv'
# dlls_path = 'D:/006564/Desktop/dlls.csv'
#
# wt_date_set = set()
# dl_date_set = set()
#
# wt_dict = defaultdict(lambda: list())
# dl_dict = defaultdict(lambda: list())
#
# wtls_f = open(wtls_path, 'r')
# i = 1
# for lines in wtls_f:
#     if i > 1:
#         wt_record = lines.strip().split(",")
#         wt_date = wt_record[5][2:-1]
#         wt_time = wt_record[8][2:-1]
#         wt_dict[wt_date].append(wt_time)
#
#         wt_date_set.add(wt_date)
#
#     i = i + 1
#
# dlls_f = open(dlls_path, 'r')
# j = 1
# for lines in dlls_f:
#     if j > 1:
#         dl_record = lines.strip().split(",")
#         dl_date = dl_record[0]
#         year = dl_date[2:6]
#         mon = dl_date[7:9]
#         day = dl_date[10:12]
#         dl_times = dl_record[1].split(":")
#
#         dl_date = year + mon + day
#         dl_time = dl_times[0][2:] + dl_times[1] + dl_times[2][0:-1]
#
#         dl_dict[dl_date].append(dl_time)
#
#         dl_date_set.add(dl_date)
#     j = j + 1
#
# question_record = dict()
# for date in wt_date_set:
#     flag = False
#     wt_time_list = wt_dict.get(date)
#     if (dl_dict.__contains__(date)):
#         dl_time_list = dl_dict.get(date)
#
#         earliest_wt_time = min(wt_time_list) #当日最早的委托时间
#         earliest_dl_time = min(dl_time_list) #当日最早的登陆时间
#
#         # 看最早的委托时间是否晚于最早的登陆时间
#         if earliest_dl_time <= earliest_wt_time:
#             flag = True
#     question_record[date] = flag
#
#     if flag == False and dl_dict.__contains__(date):
#         print(date + "\t" + earliest_dl_time + "\t" + earliest_wt_time)
# lost_record.sort()
# for day in lost_record:




# wtls_f.close()
# dlls_f.close()

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

# import os
#
# path = 'D:/006564/Desktop/log'
#
# login = []
#
# def checkAction100(file_name):
#     flag = False
#     with open(file_name,'r') as file:
#         for line in file:
#             if "Action=100" in line:
#                 record = filename.split("/")[-1][0:8] + " "+ line
#                 login.append(record.strip())
#                 flag = True
#     return flag
# loss = []
# all = []
#
# for root,dirs,files in os.walk(path):
#     all.append(files)
#     for file in files:
#         filename = path + "/" + file
#         result = checkAction100(filename)
#         if result == False:
#             loss.append(file)
#
# print(login)
#
# for record in login:
#     print(record)
