# -*- encoding: utf-8 -*-
import pandas as pd
import re
import pickle
import simple_pattern
import complex_pattern
import numpy as np
from utils import *

pattern_intro1 = re.compile("//")
pattern_intro2 = re.compile("/\*\S*\*/")
pattern_dict = simple_pattern.get_all_patterns()
pattern_key = simple_pattern.pattern_dict
content_str = '#include <math.h> double SquareRoot(float n) { return n > 0 ? sqrt(n) : -1; } double SquareRoot1(int a, double n1[10], float n) { int xxxx = 100; return n > 0 ? sqrt(n) : -1; }'


content_str = remove_annotation(content_str)
simple_matched_result_dict = rule_match(content_str, pattern_dict)
# print(simple_matched_result_dict)
complex_matched_result_dict = complex_pattern.complex_pattern_checking(content_str, pattern_dict)
print(complex_matched_result_dict)