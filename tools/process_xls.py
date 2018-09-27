from xlwt import Workbook
from collections import defaultdict, OrderedDict
import xlrd
import datetime

input_path = "d:\\006564\\Desktop\\data2.xlsx"
# input_path = "d:\\006564\\Desktop\\low.xls"
output_path = "d:\\006564\\Desktop" + "\\" + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + "_result"
sep = "|"  # 原始文本每行数据的字段分隔符
save_as_file = False  # 是否保存到新文件


# 对字段列表进行处理,返回新的行
# to be overwrite
def process_txt_row(fields):
    result = fields
    return result


def process_excel_row(arow):
    new_arow = []
    new_arow = arow
    return new_arow


# 写入到文件
def save_to_txt(result):
    output_file = output_path + ".txt"

    count_dict = defaultdict(lambda: 0)  # 使用lambda来定义简单的函数
    for record_line in result:
        workNo = record_line[9]
        name = record_line[10]
        department = record_line[11]
        worker_info = workNo + "-" + name + "-" + department
        count_dict[worker_info] += 1

    with open(output_file, "w") as output_file:
        for key in count_dict:
            print(key + "   "+ str(count_dict[key]))
            output_file.write(key + "   "+ str(count_dict[key]))

    print("save to file done!")


def save_to_excel(result):
    save_book = Workbook()
    save_sheet1 = save_book.add_sheet('Sheet 2')
    # save_sheet1.col(1).width = 1200
    # save_sheet1.col(2).width = 17200
    # save_sheet1.col(3).width = 1200
    line_num = 0
    for record in result:
        save_sheet1.write(line_num, 1, record[3])
        save_sheet1.write(line_num, 2, record[6])
        line_num += 1

    save_book.save(output_path + ".xls")
    print("save to flie done")




# 屏幕打印出来
def print_to_screen(result):
    # mac_set = set()
    # for record in result:
    #     if(record[3] == 2):
    #         macs = record[9].split(";")
    #         for mac in macs:
    #             if mac is not None:
    #                 mac_set.add(mac)
    # for val in mac_set:
    #     print(val)
    # print("size " + str(len(mac_set)))


    # ip_set = set()
    # for record in result:
    #     if(record[3] == 1 or record[3] == 2):
    #         if record[4] != 'gprs':
    #             ip = record[5]
    #             if ip is not None:
    #                 ip_set.add(ip)
    # for val in ip_set:
    #     print(val)
    # print("size " + str(len(ip_set)))

    # count = 0
    # mobile_phones = set()
    # for record in result:
    #     if record[3] == 1 or record[3] == 2:
    #         if record[4] == 'gprs':
    #             # mobile = record[10].split(";")[1]
    #             # mobile_phones.add(mobile)
    #             count += 1
    # print(count)
    # for val in mobile_phones:
    #     print(val)

    trade_cnt = 0
    trade_value = 0
    for line in result:
            if int(line[5]) > 5000000:
                trade_cnt += 1
                trade_value += line[5]

    print(trade_cnt,trade_value)

    # count_dict = defaultdict(lambda: 0)  # 使用lambda来定义简单的函数
    # for record_line in result:
    #     workNo = record_line[9]
    #     name = record_line[10]
    #     department = record_line[11]
    #     count_dict[name] += 1
    # print(count_dict)



# 读取excel的每一行
def get_row_data(bk, sh, rowx, colrange):
    result = []
    dmode = bk.datemode
    ctys = sh.row_types(rowx)
    cvals = sh.row_values(rowx)
    for colx in colrange:
        cty = ctys[colx]
        cval = cvals[colx]
        if bk.formatting_info:
            cxfx = str(sh.cell_xf_index(rowx, colx))
        else:
            cxfx = ''
        if cty == xlrd.XL_CELL_DATE:
            try:
                showval = xlrd.xldate_as_tuple(cval, dmode)
            except xlrd.XLDateError as e:
                showval = "%s:%s" % (type(e).__name__, e)
                cty = xlrd.XL_CELL_ERROR
        elif cty == xlrd.XL_CELL_ERROR:
            showval = xlrd.error_text_from_code.get(cval, '<Unknown error code 0x%02x>' % cval)
        else:
            showval = cval
        # result.append((colx, cty, showval, cxfx))
        result.append(showval)
    return result


if __name__ == '__main__':

    wtls_path = 'D:/006564/Desktop/wtls.csv'
    path2 = 'D:/006564/Desktop/dlls.csv'
    file_type = wtls_path.split(".")[1]

    try:
        # 处理excel
        if file_type == "xlsx" or file_type == "xls" or file_type == "csv":
            print("begin to process {0}".format(wtls_path))
            wtls_book = xlrd.open_workbook(wtls_path)
            wtls_sh = wtls_book.sheet_by_index(0)
            nrows, ncols = wtls_sh.nrows, wtls_sh.ncols
            print("start to process {0} rows and {1} cols".format(nrows, ncols))
            colrange = range(ncols)
            for rx in range(nrows):
                arow = get_row_data(wtls_book, wtls_sh, rx, colrange)  # arow is a list
                print(arow)

                # result = []
            # book = xlrd.open_workbook(input_path)
            # # print("The number of worksheets is {0}".format(book.nsheets))
            # # print("Worksheet name(s): {0}".format(book.sheet_names()))
            # print("start to process sheet 1")
            # sh = book.sheet_by_index(0)
            # # print("Cell D30 is {0}".format(sh.cell_value(rowx=29, colx=3)))
            # nrows, ncols = sh.nrows, sh.ncols
            # print("start to process {0} rows and {1} cols".format(nrows, ncols))
            # colrange = range(ncols)
            # for rx in range(nrows):
            #     arow = get_row_data(book, sh, rx, colrange)  # arow is a list
            #     new_arow = process_excel_row(arow)
            #     result.append(new_arow)
            # if save_as_file:
            #     save_to_excel(result)
            # else:
            #     print_to_screen(result)
        # 处理其他文本类型
        else:
            result = []
            with open(input_path, 'r') as file:
                print("start to process file")
                for line in file:
                    line.strip()
                    fields = line.split(sep)
                    result_line = process_txt_row(fields)
                    result.append(result_line)
            if save_as_file:
                save_to_txt(result)
            else:
                print_to_screen(result)
    except Exception as e:
        print("Unexpected Error: {}".format(e))
