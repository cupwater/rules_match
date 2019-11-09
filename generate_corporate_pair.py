# -*- coding: utf-8 -*-
import os
import numpy as np

match_result = np.loadtxt('./data/match_result.txt')
name_list = open('./data/pattern_name.txt').readlines()
name2semantic_dict = {}
name2semantic_in = open('./data/name2semantic.txt').readlines()

name_index_dict = {}
index = 0
for _name in name2semantic_in:
    name_index_dict[_name.split(':')[1].split('\n')[0]] = index
    index += 1
for _str in name2semantic_in:
    name, sematic = _str.split(':')
    name2semantic_dict[name] = sematic


corpo_pairs = np.zeros((match_result.shape[1], match_result.shape[1]))
for prow_idx in range(match_result.shape[1]):
    for pcol_idx in range(match_result.shape[1]):
        for data_idx in range(match_result.shape[0]):
            corpo_pairs[prow_idx, pcol_idx] += match_result[data_idx][prow_idx]*match_result[data_idx][pcol_idx]


corpo_res_name_list = {}
corpo_pairs_res = []
corpo_pairs_out = open('./data/corpo_pairs_res.txt', 'w')
# save the corporate resutls
for row_idx in range(corpo_pairs.shape[0]):
    for col_idx in range(row_idx+1, corpo_pairs.shape[1]):
        if corpo_pairs[row_idx, col_idx] > 0:
            pair_a_name = name2semantic_dict[name_list[row_idx].split('\n')[0]].split('\n')[0]
            pair_b_name = name2semantic_dict[name_list[col_idx].split('\n')[0]].split('\n')[0]
            _str = str(name_index_dict[pair_a_name]) + ',' + pair_a_name + ',协同,' + str(name_index_dict[pair_b_name]) + ',' + pair_b_name + ',' + str(int(corpo_pairs[row_idx, col_idx]))
            # _str = name_list[row_idx].split('\n')[0] + ',' + name2semantic_dict[name_list[row_idx].split('\n')[0]].split('\n')[0] + ',' + name_list[col_idx].split('\n')[0] + ',' + name2semantic_dict[name_list[col_idx].split('\n')[0]].split('\n')[0] + ',' + str(int(corpo_pairs[row_idx, col_idx]))
            # corpo_pairs_res.append(_str)
            # _str = str(row_idx) + ',' + name2semantic_dict[name_list[row_idx].split('\n')[0]].split('\n')[0] + '前驱,' + str(col_idx)  + ',' + name2semantic_dict[name_list[col_idx].split('\n')[0]].split('\n')[0] + ',' + str(int(corpo_pairs[row_idx, col_idx]))
            corpo_pairs_res.append(_str)
            if pair_a_name not in corpo_res_name_list:
                corpo_res_name_list[pair_a_name] = 0
            if pair_b_name not in corpo_res_name_list:
                corpo_res_name_list[pair_b_name] = 0
corpo_pairs_out.writelines('\n'.join(corpo_pairs_res))
corpo_pairs_out.close()



prerequi_pair = open('./data/prerequisite_pairs_res.txt').readlines()
prerequi_res = {}
for _pair in prerequi_pair:
    _, pair_a, _, _, pair_b = _pair.split('\n')[0].split(',')
    if pair_a not in prerequi_res:
        prerequi_res[pair_a] = 0
    if pair_b not in prerequi_res:
        prerequi_res[pair_b] = 0


exist_inCorpo_nexist_inPrere_list = list(set(corpo_res_name_list.keys()) - set(prerequi_res.keys()))
exist_inPrere_nexist_inCorpo_list = list(set(prerequi_res.keys()) - set(corpo_res_name_list.keys()))

exist_inCorpo_nexist_inPrere_out = open('./data/exist_inCorpo_nexist_inPrere_list.txt','w')
exist_inCorpo_nexist_inPrere_out.writelines('\n'.join(exist_inCorpo_nexist_inPrere_list))
exist_inCorpo_nexist_inPrere_out.close()

exist_inPrere_nexist_inCorpo_out = open('./data/exist_inPrere_nexist_inCorpo_list.txt','w')
exist_inPrere_nexist_inCorpo_out.writelines('\n'.join(exist_inPrere_nexist_inCorpo_list))
exist_inPrere_nexist_inCorpo_out.close()


corpo_pairs_res = []
corpo_pairs_out = open('./data/corpo_pairs_res_1.txt', 'w')
# save the corporate resutls
for row_idx in range(corpo_pairs.shape[0]):
    for col_idx in range(row_idx+1, corpo_pairs.shape[1]):
        if corpo_pairs[row_idx, col_idx] > 0:
            pair_a_name = name2semantic_dict[name_list[row_idx].split('\n')[0]].split('\n')[0]
            pair_b_name = name2semantic_dict[name_list[col_idx].split('\n')[0]].split('\n')[0]
            if pair_a_name not in prerequi_res or pair_b_name not in prerequi_res:
                continue
            _str = str(name_index_dict[pair_a_name]) + ',' + pair_a_name + ',协同,' + str(name_index_dict[pair_b_name]) + ',' + pair_b_name + ',' + str(int(corpo_pairs[row_idx, col_idx]))
            # _str = name_list[row_idx].split('\n')[0] + ',' + name2semantic_dict[name_list[row_idx].split('\n')[0]].split('\n')[0] + ',' + name_list[col_idx].split('\n')[0] + ',' + name2semantic_dict[name_list[col_idx].split('\n')[0]].split('\n')[0] + ',' + str(int(corpo_pairs[row_idx, col_idx]))
            # corpo_pairs_res.append(_str)
            # _str = str(row_idx) + ',' + name2semantic_dict[name_list[row_idx].split('\n')[0]].split('\n')[0] + '前驱,' + str(col_idx)  + ',' + name2semantic_dict[name_list[col_idx].split('\n')[0]].split('\n')[0] + ',' + str(int(corpo_pairs[row_idx, col_idx]))
            corpo_pairs_res.append(_str)
corpo_pairs_out.writelines('\n'.join(corpo_pairs_res))
corpo_pairs_out.close()