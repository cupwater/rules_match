import numpy as np


name_list = open('./data/name2semantic.txt').readlines()
name_dict = {}
for _name in name_list:
    name_dict[_name.split(':')[1].split('\n')[0]] = 0

non_exist_list = []
exist_list = []
cpp_pre_list = open('./data/cpp_prerequisite.csv').readlines()
cpp_name_list = {}
index = 0
for _pair in cpp_pre_list:
    _, pair_a, _, _, pair_b = _pair.split('\n')[0].split(',')
    if pair_a not in cpp_name_list:
        cpp_name_list[pair_a] = str(index)
        index += 1
    if pair_b not in cpp_name_list:
        cpp_name_list[pair_b] = str(index)
        index += 1
    if pair_a not in name_dict and pair_b not in name_dict:
        non_exist_list.append(_pair)
    else:
        exist_list.append(_pair)
print(len(exist_list))
print(len(non_exist_list))

non_exist_out = open('./data/non_exist_list.txt', 'w')
non_exist_out.writelines(''.join(non_exist_list))
non_exist_out.close()

exist_out = open('./data/exist_list.txt', 'w')
exist_out.writelines(''.join(exist_list))
exist_out.close()



# name_list1 = name_dict.keys()
# name_list2 = cpp_name_list.keys()
# print(len(name_list1))
# print(len(name_list2))
# print(len(set(name_list1) - set(name_list2)))
# print(len(set(name_list2) - set(name_list1)))