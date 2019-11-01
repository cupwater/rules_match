#!/usr/bin/python3
# encoding: UTF-8

import re
import pattern_lib


'''
void print() {}，void print() {} 一个程序中同时出现（声明）一个以上的同名函数
'''

# check is there is override function in a cpp file
def override_fun_pattern(rule, _str, ):
    a = pattern_dict['function_declaration']
    a.
