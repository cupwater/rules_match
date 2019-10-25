# encoding: UTF-8
import pandas as pd
import re
import pickle
import pattern_lib
import numpy as np


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


pattern_intro1 = re.compile("//")
pattern_intro2 = re.compile("/\*\S*\*/")

if __name__ == '__main__':
    df_answer = pd.read_csv("./challenge_answer.csv")
    result_rule = []
    pattern_dict = pattern_lib.get_all_patterns()
    head_str = None
    for i, row in df_answer.iterrows():
        if isinstance(row["contents"], str):
            content_array = row["contents"].split("\n")
            tmpstr = ''
            for content_str in content_array:
                content_str = content_str.strip(" ")
                intro = pattern_intro1.match(content_str)
                if intro is not None:
                    if intro.pos == 0:
                        continue
                    else:
                        content_str = content_str[:intro.pos]
                if len(content_str) == 0:
                    continue
                tmpstr = tmpstr+content_str
            reslist = pattern_intro2.findall(tmpstr)
            if len(reslist) != 0:
                for res in reslist:
                    tmpstr = tmpstr.replace(res,"")
            matched_result_dict = rule_match(tmpstr, pattern_dict)
        result_rule.append( matched_result_dict.values() )
        if head_str is None:
            head_str = matched_result_dict.keys()
    result_array = np.array(result_rule)
    with open("./code_rule.pkl","wb") as file:
        pickle.dump(result_rule, file)
