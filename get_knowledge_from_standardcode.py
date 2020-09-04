# -*- encoding: utf-8 -*-
import os
import time
import pandas as pd
import re
import pickle
import simple_pattern
import complex_pattern
import numpy as np
import collections
from utils import *
import csv

import sys
sys.stdout.flush()

import pdb

code_list = []
# with open('data/standardcode.csv') as csvfile:
with open('crawler/standardcode.csv') as csvfile:
    standardcode = csv.reader(csvfile)
    for row in standardcode:
        code_list.append(row)

print(len(code_list))
# get the involved rules of each repo
result_rule = []
pattern_name = ''
pattern_dict = simple_pattern.get_all_patterns()
for i, row in enumerate(code_list[1:]):
    print(i)
    # pdb.set_trace()
    _,shixun_id,shixun_name,position,challenge_id,challenge_name,answer_id,answer_contents = row
    content_str = remove_annotation(answer_contents)
    simple_result_dict = rule_match(content_str, pattern_dict)
    complex_result_dict = complex_pattern.complex_pattern_checking(content_str, pattern_dict)
    result_rule.append((shixun_id,shixun_name,position,challenge_id,challenge_name,answer_id, simple_result_dict.values() + complex_result_dict.values() ))
    pattern_name = simple_result_dict.keys() + complex_result_dict.keys()

shixun_rule_str_list = "shixun_id;shixun_name;position,challenge_id;challenge_name;answer_id;rule_res\n"
code_rule_array = []
for i in range(len(result_rule)):
    shixun_id, shixun_name, position, challenge_id, challenge_name, answer_id, rule_res = result_rule[i]
    code_rule_array.append(rule_res)
    shixun_rule_str = ""
    for i in range(len(rule_res)):
        shixun_rule_str += str(rule_res[i]) + ','
    shixun_rule_str_list += str(shixun_id) + ';' + shixun_name + ';' + str(position) + ';' + \
            str(challenge_id) + ';' + challenge_name + ';' + \
            str(answer_id) + ';' + shixun_rule_str + '\n'
    

pattern_show_num = np.sum(code_rule_array, axis=0)
np.savetxt('./data/standard_code/pattern_show_num.txt', pattern_show_num, fmt='%d')
np.savetxt('./data/standard_code/code_rule_array.txt', code_rule_array, fmt='%d')
with open('./data/standard_code/shixunChallenge_knowledge.txt', 'w') as f:
    f.writelines("".join(shixun_rule_str_list))





# # get the names of all repos 
# repo_name_list = [name + '\n' for name in repo_name_list]
# repo_name_out = open('./data/git_data/repo_name_for_result.txt', 'w')
# repo_name_out.writelines("".join(repo_name_list))
# repo_name_out.close()

# pattern_name_num = [ pattern_name[i] + ': ' + str(pattern_show_num[i]) for i in range(len(pattern_name)) ]
# pattern_name_num_out = open('./data/git_data/pattern_name_num.txt', 'w')
# pattern_name_num_out.writelines('\n'.join(pattern_name_num))
# pattern_name_num_out.close()

# name_pattern_dict = {}
# old_name2semantic_list = open('data/name2semantic.txt').readlines()
# for line in old_name2semantic_list:
#     name_pattern_dict[line.split(':')[0]] = line.split(':')[1].split('\n')[0]

# new_name2semantic_list = []
# for name in pattern_name:
#     if name in name_pattern_dict:
#         new_name2semantic_list.append(name + ':' + name_pattern_dict[name])
# new_name2semantic_out = open('data/git_data/name2semantic.txt', 'w')
# new_name2semantic_out.writelines('\n'.join(new_name2semantic_list))
# new_name2semantic_out.close()

# pattern_name_out = open('./data/git_data/pattern_name_newdata.txt', 'w')
# pattern_name_out.writelines('\n'.join(pattern_name))
# pattern_name_out.close()
# with open("./data/git_data/code_rule_newdata.pkl","wb") as file:
#     pickle.dump(result_rule, file)


