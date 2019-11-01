# encoding: UTF-8
import pandas as pd
import re
import pickle
import pattern_lib
import numpy as np

from utils import remove_annotation


def check_pattern(_str, pattern, rule_name):
    res = pattern.search(_str)
    if res:
        return 1
    else : 
        return 0

def rule_match(_str, pattern_dict):
    matched_result_dict = {}
    for key, value in pattern_dict.items():
        matched_result_dict[key] = check_pattern(_str, value, key)
    return matched_result_dict


if __name__ == '__main__':
    df_answer = pd.read_csv("./challenge_answer.csv")
    result_rule = []
    pattern_dict = pattern_lib.get_all_patterns()
    for i, row in df_answer.iterrows():
        if isinstance(row["contents"], str):
            content_str = remove_annotation(row["contents"])
            matched_result_dict = rule_match(content_str, pattern_dict)
            result_rule.append( matched_result_dict.values() )
        else :
            continue
    result_array = np.array(result_rule)
    with open("./code_rule.pkl","wb") as file:
        pickle.dump(result_rule, file)