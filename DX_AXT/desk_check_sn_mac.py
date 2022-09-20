#encoding:UTF-8
__author__ = 'DX'


import xlrd
import time

# # 打开刚才我们写入的 test_w.xls 文件
# wb = xlrd.open_workbook("d:/desk_sn_mac.xls")
# # 获取并打印 sheet 数量
# print( "sheet 数量:", wb.nsheets)
# # 获取并打印 sheet 名称
# print( "sheet 名称:", wb.sheet_names())
# # 根据 sheet 索引获取内容
# sh1 = wb.sheet_by_index(0)
# # 也可根据 sheet 名称获取内容
# # sh = wb.sheet_by_name('成绩')
# # 获取并打印该 sheet 行数和列数
# print( u"sheet %s 共 %d 行 %d 列" % (sh1.name, sh1.nrows, sh1.ncols))
# # 获取并打印某个单元格的值
# print( "第一行第二列的值为:", sh1.cell_value(0, 1))
# # 获取整行或整列的值
# rows = sh1.row_values(0) # 获取第一行内容
# cols = sh1.col_values(1) # 获取第二列内容
# # 打印获取的行列值
# print( "第一行的值为:", rows)
# print( "第二列的值为:", cols)
# # 获取单元格内容的数据类型
# print( "第二行第一列的值类型为:", sh1.cell(1, 0).ctype)


def check_sn_mac(sn, mac):

    sn = float(sn)
    mac = int(mac)

    # sn1 = str(sn)
    # mac1 = str(mac)

    # print("sn:",sn1)
    # print("mac:",mac1)

    # print(type(sn1))

    # 打开 desk_sn_mac.xls 数据文件
    wb = xlrd.open_workbook('/home/dx/sites/dx1023.com/django_blog/media/images/desk_sn_mac.xls')

    # 根据 sheet 索引获取内容
    sh1 = wb.sheet_by_index(0)

    # 获取 sn mac 列内容
    cols1 = sh1.col_values(1)
    cols2 = sh1.col_values(2)

    cols_sn = cols1[1:]
    cols_mac = cols2[1:]

    # print(type(cols1))

    # 打印获取的行列值
    print( "第2列的值为:", cols_sn)
    print( "第3列的值为:", cols_mac)

    # print(type(sh1.cell(1, 0)))

    # 字典方式查找
    # start =time.clock()    # 计时用
    # if sn1 in cols1:
    if cols_sn.count(sn):
        # print("该元素在列表的第", cols1[sn1], "个")    # 打印sn在原List中的位置
        # print("列表中存在这个元素")
        index = cols_sn.index(sn)
        get_mac = int(cols_mac[index])
        # print("index:", index)
        print("mac_in:", mac)
        print("mac:", get_mac)

        if(mac == get_mac):
            print("mac 匹配")
        else:
            print("mac 不匹配")

        return 1
    else:
        # print("列表中无这个元素")
        return 0
    # end = time.clock()    # 计时用
    # print('查找用时(字典方式): %s秒'%(end-start))

    

# check_sn_mac(1,2)