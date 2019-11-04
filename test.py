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



# res = get_all_functions(content_str, pattern_dict['function_declaration'])
# global_content, local_content = separate_local_global(content_str)

# # check if there is any 