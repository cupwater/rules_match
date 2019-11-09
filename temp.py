# -*- coding: utf-8 -*-
import numpy as np


name_list = open('./data/name2semantic.txt').readlines()
name_dict = {}
index = 0
for _name in name_list:
    name_dict[_name.split(':')[1].split('\n')[0]] = index
    index += 1


non_match_list = {}
match_list = {}
non_exist_list = []
exist_list = []
cpp_name_list = {}

cpp_pre_list = open('./data/cpp_prerequisite.csv').readlines()
index = 0
for _pair in cpp_pre_list:
    _, pair_a, _, _, pair_b = _pair.split('\n')[0].split(',')
    if pair_a not in cpp_name_list:
        cpp_name_list[pair_a] = 0
    if pair_b not in cpp_name_list:
        cpp_name_list[pair_b] = 0
    if pair_a not in name_dict or pair_b not in name_dict:
        non_exist_list.append(_pair)
    else:
        _temp = str(name_dict[pair_a]) + ',' + pair_a + ',前驱,' + str(name_dict[pair_b]) + ',' + pair_b
        exist_list.append(_temp)
    
    if pair_a not in name_dict:
        non_match_list[pair_a] = 0
    if pair_b not in name_dict:
        non_match_list[pair_b] = 0
    if pair_a in name_dict:
        match_list[pair_a] = 0
    if pair_b in name_dict:
        match_list[pair_b] = 0

manual_pre = open('./data/manual.txt').readlines()
for _pair in manual_pre:
    pair_a, _, pair_b = _pair.split('\n')[0].split(',')
    if pair_a not in cpp_name_list:
        cpp_name_list[pair_a] = str(index)
        index += 1
    if pair_b not in cpp_name_list:
        cpp_name_list[pair_b] = str(index)
        index += 1
    if pair_a not in name_dict or pair_b not in name_dict:
        non_exist_list.append(_pair)
    else:
        _temp = str(name_dict[pair_a]) + ',' + pair_a + ',前驱,' + str(name_dict[pair_b]) + ',' + pair_b
        exist_list.append(_temp)
        # exist_list.append(_pair)
    
    if pair_a not in name_dict:
        non_match_list[pair_a] = 0
    if pair_b not in name_dict:
        non_match_list[pair_b] = 0

non_exist_out = open('./data/non_exist_list.txt', 'w')
non_exist_out.writelines(''.join(non_exist_list))
non_exist_out.close()

exist_out = open('./data/exist_list.txt', 'w')
exist_out.writelines('\n'.join(exist_list))
exist_out.close()





non_match_list = non_match_list.keys()
match_list = match_list.keys()
non_match_list_1 = list(set(name_dict.keys()) - set(match_list))

non_match_list.sort()
non_match_list_1.sort()


non_match_out = open('non_match_list.txt', 'w')
non_match_out.writelines('\n'.join(non_match_list))
non_match_out.close()

non_match_out = open('non_match_list_1.txt', 'w')
non_match_out.writelines('\n'.join(non_match_list_1))
non_match_out.close()

# non_match_out.close()
# name_list = [_str.split('\n')[0] for _str in name_list]
# non_match_list = [_str.split('\n')[0] for _str in non_match_list]
# match_list = set(name_list) - set(non_match_list) 


# name_list1 = name_dict.keys()
# name_list2 = cpp_name_list.keys()
# print(len(name_list1))
# print(len(name_list2))
# print(len(set(name_list1) - set(name_list2)))
# print(len(set(name_list2) - set(name_list1)))