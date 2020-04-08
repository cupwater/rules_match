# -*- encoding: utf-8 -*-
import pandas as pd
import re
import pickle
import simple_pattern
import complex_pattern
import numpy as np
import collections
from utils import *


if __name__ == '__main__':
    df_answer = pd.read_csv("./data/new_data/result.csv")
    result_rule = []
    pattern_name = ''
    pattern_dict = simple_pattern.get_all_patterns()
    # base_class = re.compile("class" + sp + cls_name + sp + colon + sp + acemodi_key + sp + cls_name)
    for i, row in df_answer.iterrows():
        if isinstance(row["answer_contents"], str) and i >3:
            content_str = remove_annotation(row["answer_contents"])
            # print(content_str)
            # print("runing {} !".format(str(i)))
            # content_str = '#include <math.h> class A {int a=10; static int xy(int *a, int b) {int x=10; a=10; } class B : private A {int x; int y;} float x; double SquareRoot(float n) { return n > 0 ? sqrt(n) : -1; } double SquareRoot1(int a, double n1[10], float n) { static int xxxx = 100; return n > 0 ? sqrt(n) : -1; }'
            # baseclass_res = base_class.search(content_str)
            # if baseclass_res:
                # print(baseclass_res.group())
            simple_result_dict = rule_match(content_str, pattern_dict)
            complex_result_dict = complex_pattern.complex_pattern_checking(content_str, pattern_dict)
            result_rule.append( simple_result_dict.values() + complex_result_dict.values() )
            pattern_name = simple_result_dict.keys() + complex_result_dict.keys()
        # else :
        #     continue
    result_array = np.array(result_rule)
    pattern_show_num = np.sum(result_array, axis=0)
    np.savetxt('./data/new_data/pattern_show_num.txt', pattern_show_num, fmt='%d')
    np.savetxt('./data/new_data/match_result_newdata.txt', result_array, fmt='%d')

    pattern_name_num = [ pattern_name[i] + ': ' + str(pattern_show_num[i]) for i in range(len(pattern_name)) ]
    pattern_name_num_out = open('./data/new_data/pattern_name_num.txt', 'w')
    pattern_name_num_out.writelines('\n'.join(pattern_name_num))
    pattern_name_num_out.close()

    name_pattern_dict = {}
    old_name2semantic_list = open('data/name2semantic.txt').readlines()
    for line in old_name2semantic_list:
        name_pattern_dict[line.split(':')[0]] = line.split(':')[1].split('\n')[0]

    new_name2semantic_list = []
    for name in pattern_name:
        if name in name_pattern_dict:
            new_name2semantic_list.append(name + ':' + name_pattern_dict[name])
    new_name2semantic_out = open('data/new_data/name2semantic.txt', 'w')
    new_name2semantic_out.writelines('\n'.join(new_name2semantic_list))
    new_name2semantic_out.close()

    pattern_name_out = open('./data/new_data/pattern_name_newdata.txt', 'w')
    pattern_name_out.writelines('\n'.join(pattern_name))
    pattern_name_out.close()
    with open("./data/new_data/code_rule_newdata.pkl","wb") as file:
        pickle.dump(result_rule, file)

# pattern_dict = simple_pattern.get_all_patterns()
# pattern_key = simple_pattern.pattern_dict
# content_str = '#include <math.h> class A {int a=10; static int xy(int *a, int b) {int x=10; a=10;} } class B : public A {int x; int y;} float x; double SquareRoot(float n) { return n > 0 ? sqrt(n) : -1; } double SquareRoot1(int a, double n1[10], float n) { static int xxxx = 100; return n > 0 ? sqrt(n) : -1; }'
# print(pattern_key['variable_declaration1'])

# content_str = remove_annotation(content_str)
# simple_matched_result_dict = rule_match(content_str, pattern_dict)
# # print(simple_matched_result_dict)
# complex_matched_result_dict = complex_pattern.complex_pattern_checking(content_str, pattern_dict)
# print(complex_matched_result_dict)
