from xlwt import Workbook
from collections import defaultdict, OrderedDict
import xlrd
import datetime

input_path = "d:\\006564\\Desktop\\test.xls"
output_path = "d:\\006564\\Desktop" + "\\" + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + "_result"
sep = "|"  # 原始文本每行数据的字段分隔符
save_as_file = True  # 是否保存到新文件


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
    with open(output_file, "w") as output_file:
        for line in result:
            output_file.write(line + "\n")
    print("save to file done!")


def save_to_excel(result):
    save_book = Workbook()
    save_sheet1 = save_book.add_sheet('Sheet 2')
    # save_sheet1.col(1).width = 1200
    # save_sheet1.col(2).width = 17200
    # save_sheet1.col(3).width = 1200
    version_dict = defaultdict(list)
    for row, value in enumerate(result):
        if row > 4:
            v_info = value[1].split("|")
            if len(v_info) > 1:
                system = str(v_info[0]).upper()
                version = ''.join(str(e) for e in v_info[1:])
                num_of_person = str(int(value[2]))
                version_dict[system].append((version, num_of_person))
            else:
                system = str(value[1]).upper()
                version = ''
                num_of_person = str(int(value[2]))
                version_dict[system].append((version, num_of_person))

    sorted_version_list = sorted(version_dict.items(), key=lambda d: d[0]) # 对key进行排序
    line_num = 0
    for key in sorted_version_list:
        system = key[0]
        verison_list = version_dict[system]
        if system == "ROOT" or system == "TAS" or system == "TEL" or system == "THIRD":
            continue
        for rx, value in enumerate(verison_list):
            if rx == 0:
                print(system, value[0], value[1])
                save_sheet1.write(line_num, 0, system)
                save_sheet1.write(line_num, 1, value[0])
                save_sheet1.write(line_num, 2, value[1])
            else:
                print(value[0], value[1])
                save_sheet1.write(line_num, 1, value[0])
                save_sheet1.write(line_num, 2, value[1])
            line_num += 1
    # nrows = len(result)
    # for rx in range(nrows):
    #     for cx, c_value in enumerate(result[rx]):
    #         save_sheet1.write(rx, cx, c_value)
    save_book.save(output_path + ".xls")
    print("save to flie done")

# 屏幕打印出来
def print_to_screen(result):
    version_dict = defaultdict(list)
    # print(result)
    # for row, value in enumerate(result):
    #     if row > 4:
    #         v_info = value[1].split("|")
    #         if len(v_info) > 1:
    #             system = v_info[0]
    #             version = ''.join(str(e) for e in v_info[1:])
    #             num_of_person = str(int(value[2]))
    #             version_dict[system].append((version,num_of_person))
    #
    # for system in version_dict:
    #     print(system,version_dict[system])


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

    file_type = input_path.split(".")[1]

    try:
        # 处理excel
        if file_type == "xlsx" or file_type == "xls" or file_type == "csv":
            result = []
            book = xlrd.open_workbook(input_path)
            # print("The number of worksheets is {0}".format(book.nsheets))
            # print("Worksheet name(s): {0}".format(book.sheet_names()))
            print("start to process sheet 1")
            sh = book.sheet_by_index(0)
            # print("Cell D30 is {0}".format(sh.cell_value(rowx=29, colx=3)))
            nrows, ncols = sh.nrows, sh.ncols
            print("start to process {0} rows and {1} cols".format(nrows, ncols))
            colrange = range(ncols)
            for rx in range(nrows):
                arow = get_row_data(book, sh, rx, colrange)  # arow is a list
                new_arow = process_excel_row(arow)
                result.append(new_arow)
            if save_as_file:
                save_to_excel(result)
            else:
                print_to_screen(result)
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
