# encoding: UTF-8
import re

pattern_intro1 = re.compile("//")
pattern_intro2 = re.compile("/\*\S*\*/")

def remove_annotation(_str):
    content_array = _str.split("\n")
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
    return tmpstr

def separate_local_global_contents(_str):
    res_index = []
    _stack = []
    for i, letter in enumerate(_str)
        if letter == '{':
            _stack.append(i)
        elif letter == '}':
            if len(_stack) == 1:
                res_index.extend([_stack[0], i])
            _stack.pop()
    local_content = ''
    global_content = ''
    for i in range(int(len(res_index)/2)):
        if i == 0:
            local_content = local_content + _str[0:i]
            global_content = global_content + _str[i:(i+1)]
    return local_content, global_content

# get all function and their content, 
# return a list of 4-tuples: [fc_sidx, fd_eidx, fc_sidx, fc_eidx], record the start and end index of declaration and contents
def get_all_functions(_str, fun_declar):
    fun_contents_list = []
    fun_list = re.finditer(fun_declar, _str)
    fun_idxs_list
    for _fun in fun_list:
        fd_sidx = _fun.start() # function declaration start index
        fc_sidx = -1 # function content start index
        fc_eidx = -1 # function content start index
        _stack = []
        for i, letter in enumerate(_str[fd_sidx:]):
            # only function announcement, but declaration
            if letter == ';':
                fc_eidx = i + fd_sidx
                break
            if letter == '{':
                fd_eidx = i + fd_sidx - 1
                fc_sidx = i + fd_sidx
                _stack.append(i)
            elif letter == '}':
                if len(_stack) == 1:
                    fc_eidx = i + fd_sidx
                    break
        if fc_eidx == -1:
            fc_eidx = len(_str)
        fun_idxs_list.append([fd_sidx, fd_sidx, fc_sidx, fc_eidx])
    return fun_idxs_list

def check_array_params(fun_declar_str, fun_content_str, array_pattern):
    array_list = re.finditer(array_pattern, fun_declar)
    for _array in array_list:
        # first, get the array name
        array_name = _array.split(' ')[1]
        if array_name in fun_content_str:
            return 1
        else: 
            continue
    return 0




    