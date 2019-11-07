import os
import numpy as np

match_result = np.loadtxt('./data/match_result.txt')
name_list = open('./data/pattern_name.txt').readlines()
name2semantic_dict = {}
name2semantic_in = open('./data/name2semantic.txt').readlines()

for _str in name2semantic_in:
    name, sematic = _str.split(':')
    name2semantic_dict[name] = sematic


corpo_pairs = np.zeros((match_result.shape[1], match_result.shape[1]))
for prow_idx in range(match_result.shape[1]):
    for pcol_idx in range(match_result.shape[1]):
        for data_idx in range(match_result.shape[0]):
            corpo_pairs[prow_idx, pcol_idx] += match_result[data_idx][prow_idx]*match_result[data_idx][pcol_idx]

corpo_pairs_res = []
corpo_pairs_out = open('./data/corpo_pairs_res.txt', 'w')
# save the corporate resutls
for row_idx in range(corpo_pairs.shape[0]):
    for col_idx in range(row_idx+1, corpo_pairs.shape[1]):
        if corpo_pairs[row_idx, col_idx] > 0:
            _str = name_list[row_idx].split('\n')[0] + ',' + name2semantic_dict[name_list[row_idx].split('\n')[0]].split('\n')[0] + ',' + name_list[col_idx].split('\n')[0] + ',' + name2semantic_dict[name_list[col_idx].split('\n')[0]].split('\n')[0] + ',' + str(int(corpo_pairs[row_idx, col_idx]))
            corpo_pairs_res.append(_str)
corpo_pairs_out.writelines('\n'.join(corpo_pairs_res))
corpo_pairs_out.close()