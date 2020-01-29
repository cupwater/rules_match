# -*- coding: utf-8 -*-
import xlwt
import xlrd
import re
from xlutils.copy import copy

file_path = "data/c++_rule.xls"

workbook = xlrd.open_workbook(file_path)
#通过index来获得一个sheet对象，index从0开始算起
sheet = workbook.sheet_by_index(0)
# sheet.nrows：sheet的行数
print (sheet.nrows)
# 字段名称
patterns = ["summary","type","defaultSeverity","inDefaultProfile","availability","ruleKey","tags","description"]

# 获得特定的cell对象的值
str_cell = sheet.cell(0,0).value

# 找到 pattern 在 str_cell 的索引位置
for i in range(len(patterns)):   
    if i<7:
        pattern_index1 = str_cell.find(patterns[i])
        pattern_index2 = str_cell.find(patterns[i+1])
        slice_pattern = str_cell[pattern_index1:pattern_index2]
    else:
        pattern_index1 = str_cell.find(patterns[i])
        slice_pattern = str_cell[pattern_index1:-1]

    # 用 xlrd 提供的方法读取 c++_rule_opt.xls 文件
    workbook3 = xlrd.open_workbook('data/c++_rule_opt.xls')
    # 用 xlutils 提供的copy方法将 xlrd 的对象转化为 xlwt 的对象
    workbook4 = copy(workbook3) 
    # 从复制的一个 excel 文件中得到一个 sheet
    sheet3 = workbook4.get_sheet(0)
    print(sheet3)
    # 写入数据
    # 将 slice_pattern1 存入 excel 中的 相应 cell
    sheet3.write(1, i, slice_pattern)
    # print(slice_pattern)


workbook4.save('data/c++_rule_opt.xls')

# sheet.row_values(index)：返回某一行的值列表
print (sheet.row_values(0))