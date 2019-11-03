# -*- encoding: utf-8 -*-
import pandas as pd
import re
import pickle
import pattern_lib
import numpy as np
from utils import get_all_functions, separate_local_global


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
pattern_dict = pattern_lib.get_all_patterns()
pattern_key = pattern_lib.pattern_dict
content_str = '#include <math.h> double SquareRoot(float n) { return n > 0 ? sqrt(n) : -1; } double SquareRoot1(int a, double n1[10], float n) { int xxxx = 100; return n > 0 ? sqrt(n) : -1; }'
res = get_all_functions(content_str, pattern_dict['function_declaration'])
global_content, local_content = separate_local_global(content_str)

# check if there is any 