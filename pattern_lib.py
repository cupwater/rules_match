#!/usr/bin/python3
# encoding: UTF-8
"""
 this file contains all regex rules used for matching
 author:xxx
 date: 2019.10.24
"""

import re

num_ch = "[0-9]"
num_def = "[0-9]*"
type_def = "(int|float|bool|char|double|void|wchar_t)"
acemodi_def = "(public|private|protected)"
var_def = "[a-zA-Z_][a-zA-Z0-9_]*"
mem_name_def = "[a-z][a-zA-Z0-9_]*"
cls_name_def = "[A-Z][a-zA-Z0-9_]*"
sp_line = "\n\n*"
sp = "\s*"
left_square = "\["
right_square = "\]"
left_brackets = "\("
right_brackets = "\)"
left_curbra = "\{"  # curba: curly brackets
right_curbra = "\}"
left_brackets_comma = "(,"
right_brackets_star = ")*"
title_def = ";"
colon = ":"

or_def = '|'
none_def = ''
var_declar = type_def + sp + var_def
array1d_declar = var_declar + left_square + num_def + right_square
arraynd_declar = var_declar + left_square + num_def + right_square + '(\[[0-9]*\])*'
varORarray_declar = '(' + var_declar + or_def + array1d_declar + or_def + arraynd_declar + ')'
repeat_varORarray_declar = varORarray_declar + '(' + ',\s*' + varORarray_declar + ')*'

array1d_def = var_def + left_square + num_def + right_square
arraynd_def = var_declar + left_square + num_def + right_square + '(\[[0-9]*\])*'
array_def   = '(' + array1d_def + or_def + arraynd_def + ')'
varORarray_def = '(' + array_def + or_def + arraynd_def + ')'
repeat_varORarray_def = varORarray_def + '(' + ',\s*' + varORarray_def + ')*'


pattern_dict = {
    #function related pattern
    "func": "::",
    "function_declaration": var_declar + left_brackets + repeat_varORarray_declar + or_def + none_def + right_brackets,
    "pass_value_call": var_def + left_brackets + repeat_varORarray_def + right_brackets,
    "function_definitions": type_def + sp + mem_name_def + left_brackets + type_def + sp + mem_name_def + left_brackets_comma + sp + type_def + sp + mem_name_def + right_brackets_star + right_brackets,
    # "return_type": var_declar + left_brackets + var_def + left_brackets_comma + sp + var_def + right_brackets_star + right_brackets,
    "return_type": var_declar + left_brackets + var_def + left_brackets_comma + sp + var_def + right_brackets_star + right_brackets,
    "reference_call": var_def + sp + left_brackets + type_def + sp + "&" + var_def + sp + left_brackets_comma + sp + type_def + sp + "&" + var_def + right_brackets_star + right_brackets,

    # cosine function related
    "cos1": "cos" + left_brackets + var_declar + right_brackets,
    "cos2": "cos" + left_brackets + var_def + right_brackets,
    "sin1": "sin" + left_brackets + var_declar + right_brackets,
    "sin2": "sin" + left_brackets + var_def + right_brackets,
    "tan1": "tan" + left_brackets + var_declar + right_brackets,
    "tan2": "tan" + left_brackets + var_def + right_brackets,
    "log1": "log" + left_brackets + var_def + right_brackets,
    "log2": "log10" + left_brackets + var_def + right_brackets,
    "sqrt1": "sqrt" + left_brackets + var_declar + right_brackets,
    "sqrt2": "sqrt" + left_brackets + var_def + right_brackets,
    
    # class related pattern
    "public_inheritance": "class" + sp + cls_name_def + sp + colon + sp + "public" + sp + cls_name_def,
    "protected_inheritance": "class" + sp + cls_name_def + sp + colon + sp + "protected" + sp + cls_name_def,
    "private_inheritance": "class" + sp + cls_name_def + sp + colon + sp + "private" + sp + cls_name_def,
    "public_member": "class" + sp + cls_name_def + sp + sp_line + left_curbra + sp + sp_line + sp + "public:" + sp + sp_line + sp + var_declar + title_def,
    "private_member": "class" + sp + cls_name_def + sp + sp_line + left_curbra + sp + sp_line + sp + "private:" + sp + sp_line + sp + var_declar + title_def,
    "protected_member": "class" + sp + cls_name_def + sp + sp_line + left_curbra + sp + sp_line + sp + "protected:" + sp + sp_line + sp + var_declar + title_def,
    "deconstruct": "~" + var_def + left_brackets + sp + right_brackets,
    "base_class": "class" + sp + cls_name_def + colon + sp + acemodi_def + sp + cls_name_def,
    "object_def": cls_name_def + sp + cls_name_def + left_brackets_comma + sp + var_def + right_brackets_star + title_def,
    "datamember": cls_name_def + "." + mem_name_def,
    "derived_class": "class" + sp + cls_name_def + sp + colon + sp + acemodi_def + sp + cls_name_def,
    "pure_virtual_function": "virtual" + sp + var_declar + left_brackets + sp + right_brackets,
    "datamember": cls_name_def + "." + mem_name_def,

    # array or pointer related pattern
    "pointer_variable_declaration": type_def + sp + "\*" + mem_name_def,
    "pointer_array": "\*" + var_def + left_square + var_def + right_square,
    "reference_statement": type_def + "&" + sp + var_def,
    "pointer_to_structure": "struct" + sp + var_def + sp + "\*" + var_def,
    "array": var_def + left_square + num_def + right_square,
    "multiarray": var_def + left_square + num_def + right_square + left_square + num_def + right_square,
    "array_as_parameter1": type_def + sp + mem_name_def + left_brackets + type_def + sp + mem_name_def + left_square + num_def + right_square + left_brackets_comma + sp + type_def + sp + mem_name_def + left_square + num_def + right_square + right_brackets_star + right_brackets,
    "array_as_parameter2": type_def + sp + mem_name_def + left_brackets + type_def + sp + mem_name_def + left_square + sp + right_square + left_brackets_comma + sp + type_def + sp + mem_name_def + left_square + num_def + right_square + right_brackets_star + right_brackets,
    "pointer": "\*" + var_def,
    "array_declaration": var_declar + left_square + num_ch + num_def + right_square + title_def,
    "initialize_array": var_def + left_square + sp + right_square + sp + "=",
    "null_pointer": "\*" + var_def + sp + "=" + sp + "NULL",
    "pointer_to_pointer": "\*\*" + var_def,
    "pass_pointer_to_function": var_declar + left_brackets + type_def + sp + "\*" + var_def + right_brackets,
    "return_pointer_from_function": type_def + sp + "\*" + sp + var_def + left_brackets + sp + right_brackets,
    "pointer_call": var_def + sp + left_brackets + type_def + sp + "\*" + var_def + sp + left_brackets_comma + sp + type_def + sp + "\*" + var_def + right_brackets_star + right_brackets,

    # parameter related
    "miscellaneous_data_type_cast": left_brackets + type_def + right_brackets,
    # "do_while": sp + "do" + sp,
    "if_else": sp + "else" + sp,
    "formal_parameter": var_declar + left_brackets + var_def + left_brackets_comma + sp + var_def + right_brackets_star + right_brackets,
    "actual_parameter1": var_def + left_brackets + var_def + left_brackets_comma + sp + var_def + right_brackets_star + right_brackets,
    "actual_parameter2": var_def + sp + left_brackets + type_def + sp + "\*" + var_def + sp + left_brackets_comma + sp + type_def + sp + "\*" + var_def + right_brackets_star + right_brackets,

    # variable related pattern
    "variable_declaration1": var_declar + left_brackets_comma + sp + var_def + right_brackets_star + title_def,
    "variable_declaration2": "extern" + sp + var_declar + left_brackets_comma + sp + var_def + right_brackets_star + title_def,
    "string": "char" + sp + mem_name_def + left_square + num_def + right_square,
    "variable_definitions": type_def + sp + mem_name_def + left_brackets_comma + sp + mem_name_def + right_brackets_star,
    
    # number related pattern
    "octal": "0[0-7]*",
    "decimal": "[1-9]" + num_def,
    "float_number": num_def + "." + num_def,
    "float_e": num_ch + num_def + "." + num_ch + num_def + "e",
    "float_E": num_ch + num_def + "." + num_ch + num_def + "E",
    "hexadecimal": "(0x)|(0X)[a-fA-F0-9]*",

    
    "intro1": "//",
    "intro2": "/\*\S*\*/",
    # specify declaration
    "memory_address": "&" + var_def,
    "string": "string" + sp + "\*" + var_def + sp + "=" + sp + "(\"|\').*(\"|\')",
    "struct_def" : "struct",
    "class_def": "class",
    # "include_def":  "#include",
    "inline_def": "inline",
    "iostream_def"    : "iostream",
    "iomanip_def"    : "iomanip",
    "namespace_def"    : "namespace",
    "char_def"    : "char",
    "string_def"    : "string",
    "friend_def"    : "friend",
    "this_def"    : "this->",
    "operator_def"    : "operator",
    "bool_def"    : "bool",
    "int_def"    : "int",
    "float_def"    : "float",
    # "double_def"    : "double",
    # "void_def"    : "void",
    "wchar_t_def"    : "wchar_t",
    "virtual_def"    : "virtual",
    "true_def"    : "true",
    "false_def"    : "false",
    # "const_def"    : "const",
    "#define_def"    : "#define",
    "signed_def"    : "signed",
    "unsigned_def"    : "unsigned",
    "long_def"    : "long",
    "short_def"    : "short",
    "sizeof_def"    : "sizeof",
    "auto_def"    : "auto",
    "register_def"    : "register",
    "static_def"    : "static",
    "extem_def"    : "extem",
    "mutable_def"    : "mutable",
    "thread_local_def"    : "thread_local",
    "while_def"    : "while",
    "for_def"    : "for",
    "break_def"    : "break",
    "continue_def"    : "continue",
    "goto_def"    : "goto",
    # "if_def"    : "if",
    "switch_def"    : "switch",
    "main_def"    : "main",
    "srand_def"    : "srand",
    "rand_def"    : "rand",
    "strcpy_def"    : "strcpy",
    "strcat_def"    : "strcat",
    "strlen_def"    : "strlen",
    "strcmp_def"    : "strcmp",
    "strchr_def"    : "strchr",
    "strstr_def"    : "strstr",
    "fstream_def"    : "fstream",
    "cin_def"    : "cin",
    "cout_def"    : "cout",
    "cerr_def"    : "cerr",
    "clog_def"    : "clog",
    "setw_def"    : "setw",
    "setprecision_def"    : "setprecision",
    "using_def"    : "using",
    "printf_def"    : "printf",
    "scanf_def"    : "scanf",
    "enum_def"    : "enum",
    "alarm_def" : "\\a",
    # "back_sp_def": "\\b",
    "page_break_def": "\\f",
    "line_break_def": "\\n",
    "enter_def": "\\r",
    # "tab_def": "\\t",
    "vertical_def": "\\v",
    "plus_def": "\+",
    "sub_def": "-",
    "times_def": "\*",
    "div_def": "/",
    "residual_def": "%",
    "increase_def": "\+\+",
    "decrease_def": "--",
    "equal_def": "==",
    "nonequal_def": "!=",
    "lt_def": "<",
    "gt_def": ">",
    "ngt_def": "<=",
    "nlt_def": ">=",
    "logi_and_def": "&&",
    "logi_or_def": "\|\|",
    "no_def": "!",
    "and_def": "&",
    "or_def": "\|",
    "xor_def": "\^",
    "complement_def": "~",
    "left_move_def": "<<",
    "right_move_def": ">>",
    "assign_value_def": "=",
    "plus_assign_def": "\+=",
    "sub_assign_def": "-=",
    "times_assign_def": "\*=",
    "div_assign_def": "/=",
    "residual_assign_def": "%=",
    "left_move_assign_def": "<<=",
    "right_move_assign_def": ">>=",
    "and_assign_def": "&=",
    "or_assign_def": "\|=",
    "xor_assign_def": "\^="
}


def get_all_patterns(rules_dict = pattern_dict):
    compile_res = {}
    for key, value in pattern_dict.items():
        compile_res[key] = re.compile(value)
    return compile_res