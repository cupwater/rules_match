#!/usr/bin/python3
# encoding: UTF-8
"""
 this file contains complex pattern checking
 there are 6 different complex patterns
 author:xxx
 date: 2019.10.24
"""

import re
from utils import *

__complex_pattern__ = ['overload_fun', 'local_var', 'global_var', 'array_param', 'static_mem_fun', 'polym_class', 'ptr_arith']


def isIncludeKeyWord(content, keyword):
    if  -1 != content.find(keyword):
        pattern_str='(^'+keyword+'$)|(^'+keyword+'(\W+).*)|(.*(\W+)'+keyword+'$)|(.*(\W+)'+tmp_keyword+'(\W+).*)'
        m = re.match(r''+pattern_str+'', content)
        if m:
            return 1
    return 0

def check_overload_fun(fun_heads_list):
    fun_name_list = []
    for _str in fun_heads_list:
        if ';' in _str:
            continue
        fun_name_list.append(_str.split('(')[0].split(' ')[1])
    if len(fun_name_list) != len(set(fun_name_list)):
        return 1
    else:
        return 0

def check_local_var(local_content, var_pattern):
    res = var_pattern.search(local_content)
    if res:
        return 1
    else : 
        return 0

def check_global_var(global_content, var_pattern):
    res = var_pattern.search(local_content)
    if res:
        return 1
    else : 
        return 0

def check_array_param(fun_heads_list, fun_contents_list, ptr_var_declar_pattern):
    for _fun_head, _fun_content in zip(fun_heads_list, fun_contents_list):
        res = ptr_var_declar_pattern.search(_fun_head)
        if res:
            match_content = res.group()
            ptr_name = match_content.split('*')[1]
            key_res = isIncludeKeyWord(_fun_content, ptr_name)
            if key_res == 1:
                return 1
    return 0

def check_static_member_fun(fun_head):
    for _fun_head in fun_heads_list:
        if 'static' in _fun_head:
            return 1
    return 0

def check_polym_class(_str):
    


# check complex patterns
def complex_pattern_checking(_str, pattern_dict):
    global_content, local_content = separate_local_global(_str)
    fun_head_content_idxs = get_all_functions(_str, pattern_dict['function_declaration'])
    # first check the overload function