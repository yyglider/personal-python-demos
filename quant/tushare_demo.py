import tushare as ts
import numpy as np
#
# stock_code = '002157'
# start_at = '2016-05-05'
# end_at ='2016-05-20'

#
# stock_df = ts.get_hist_data(stock_code,start=start_at,end=end_at)
# print(stock_df)

H/L>=1.05 and \

(O-L)/(c-O)>=2\
open - low / close - open


and c<ref(c,5) and c<ref(c,10) and c<ref(c,20) and c<ref(c,30);

# for i in range(0,4):
#     print(a[i])


# #
# # # # (Year, month, day) tuples suffice as args for quotes_historical_yahoo
# date1 = (2016, 1, 5)
# date2 = (2017, 1, 1)
