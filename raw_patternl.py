import pandas as pd
import re
import pickle

pattern_deconstruct = re.compile("~[a-zA-Z]+\(\)") 
pattern_point = re.compile("\*[a-zA-Z]+")   #也可能是乘法
pattern_memory_address = re.compile("&[a-zA-Z]+")   #也有可能是引用
pattern_func = re.compile("::")
pattern_array = re.compile("[a-zA-Z]+[0-9]*\[[0-9]*\]")
pattern_multiarray = re.compile("[a-zA-Z]+[0-9]*\[[0-9]*\]\[[0-9]*\]")
pattern_datamember = re.compile("[A-Z][a-z0-9_]*.[a-z][a-zA-Z0-9_]*")
pattern_pass_value_call = re.compile("[a-zA-Z_][a-zA-Z0-9_]*\([a-zA-Z_][a-zA-Z0-9_]*(,\s*[a-zA-Z_][a-zA-Z0-9_]*)*\)")
pattern_variable_declaration1 = re.compile("(int|float|bool|char|double|void|wchar_t)\s[a-zA-Z_][a-zA-Z0-9_]*(,\s*[a-zA-Z_][a-zA-Z0-9_]*)*;")
pattern_variable_declaration2 = re.compile("extern\s(int|float|bool|char|double|void|wchar_t)\s[a-zA-Z_][a-zA-Z0-9_]*(,\s*[a-zA-Z_][a-zA-Z0-9_]*)*;")
pattern_object = re.compile("[A-Z][a-z0-9_]*\s[A-Z][a-z0-9_]*(,\s*[A-Z_][a-z0-9_]*)*;")
pattern_function_declaration = re.compile("(int|float|bool|char|double|void|wchar_t)\s[a-zA-Z_][a-zA-Z0-9_]*\([a-zA-Z_][a-zA-Z0-9_]*(,\s*[a-zA-Z_][a-zA-Z0-9_]*)*\)")
pattern_base_class = re.compile("class\s[A-Z][a-z0-9_]*:\s*(public|private|protected)\s[A-Z][a-z0-9_]*")
pattern_string = re.compile("char\s[a-z][a-zA-Z0-9_]*\[[0-9]*\]")
pattern_variable_definitions = re.compile("(int|float|bool|char|double|void|wchar_t)\s[a-z][a-zA-Z0-9_]*(,\s*[a-z][a-zA-Z0-9_]*)*")
pattern_function_definitions = re.compile("(int|float|bool|char|double|void|wchar_t)\s[a-z][a-zA-Z0-9_]*\((int|float|bool|char|double|void|wchar_t)\s[a-z][a-zA-Z0-9_]*(,\s*(int|float|bool|char|double|void|wchar_t)\s[a-z][a-zA-Z0-9_]*)*\)")
pattern_return_type = re.compile("(int|float|bool|char|double|void|wchar_t)\s[a-zA-Z_][a-zA-Z0-9_]*\([a-zA-Z_][a-zA-Z0-9_]*(,\s*[a-zA-Z_][a-zA-Z0-9_]*)*\)")
pattern_return_type = re.compile("(int|float|bool|char|double|void|wchar_t)\s[a-zA-Z_][a-zA-Z0-9_]*\([a-zA-Z_][a-zA-Z0-9_]*(,\s*[a-zA-Z_][a-zA-Z0-9_]*)*\)")
pattern_array_as_parameter1 = re.compile("(int|float|bool|char|double|void|wchar_t)\s[a-z][a-zA-Z0-9_]*\((int|float|bool|char|double|void|wchar_t)\s[a-z][a-zA-Z0-9_]*\[[0-9]*\](,\s*(int|float|bool|char|double|void|wchar_t)\s[a-z][a-zA-Z0-9_]*\[[0-9]*\])*\)")
pattern_array_as_parameter2 = re.compile("(int|float|bool|char|double|void|wchar_t)\s[a-z][a-zA-Z0-9_]*\((int|float|bool|char|double|void|wchar_t)\s[a-z][a-zA-Z0-9_]*\[\s*\](,\s*(int|float|bool|char|double|void|wchar_t)\s[a-z][a-zA-Z0-9_]*\[[0-9]*\])*\)")
pattern_datamember = re.compile("[A-Z][a-z0-9_]*.[a-z][a-zA-Z0-9_]*")
pattern_pointer_variable_declaration = re.compile("(int|float|bool|char|double|void|wchar_t)\s\*[a-z][a-zA-Z0-9_]*")
pattern_pointer_array = re.compile("\*[a-zA-Z][a-zA-Z0-9_]*\[[a-zA-Z][a-zA-Z0-9_]*\]")
pattern_reference_statement = re.compile("(int|float|bool|char|double|void|wchar_t)&\s*[a-zA-Z][a-zA-Z0-9_]*")
pattern_pointer_to_structure = re.compile("struct\s[a-zA-Z][a-zA-Z0-9_]*\s\*[a-zA-Z][a-zA-Z0-9_]*")
pattern_string = re.compile("string\s*\*[a-zA-Z][a-zA-Z0-9_]*\s*=\s*(\"|\').*(\"|\')")
pattern_derived_class = re.compile("class\s*[A-Z][a-zA-Z0-9_]*\s*:\s*(public|private|protected)\s*[A-Z][a-zA-Z0-9_]*")
pattern_pure_virtual_function = re.compile("virtual\s*(int|float|bool|char|double|void|wchar_t)\s*[a-zA-Z][a-zA-Z0-9_]*\(\s*\)")
pattern_hexadecimal = re.compile("(0x)|(0X)[a-fA-F0-9]*")
pattern_octal = re.compile("0[0-7]*")
pattern_decimal = re.compile("[0-9]*")
pattern_float_number = re.compile("[0-9][0-9]*.[0-9][0-9]*")
pattern_float_e = re.compile("[0-9][0-9]*.[0-9][0-9]*e")
pattern_float_E = re.compile("[0-9][0-9]*.[0-9][0-9]*E")
pattern_str = re.compile("(\"|\')[a-zA-Z0-9_]*\s*(,|\.|;|!|@|#|\$|%|\^|&|\*|-|\+|`|\[|\]|\{|\}|:|<|>|\?)*\s*[a-zA-Z0-9_]*(,|\.|;|!|@|#|\$|%|\^|&|\*|-|\+|`|\[|\]|\{|\}|:|<|>|\?)*\s*(\"|\')")
pattern_miscellaneous_operator_choose = re.compile("[a-zA-Z0-9_]*\s*(\+|-|\*|/|=|<|>)*\s*[a-zA-Z0-9_]*\s*(\+|-|\*|/|=|<|>)*\s*[a-zA-Z0-9_]*\s*\?\s*[a-zA-Z0-9_]*\s*(\+|-|\*|/)*\s*[a-zA-Z0-9_]*\s*:\s*[a-zA-Z0-9_]*(\+|-|\*|/)*[a-zA-Z0-9_]*")
pattern_miscellaneous_operator_comma = re.compile("\([a-zA-Z0-9_]*\s*(\+|-|\*|\\|=|<|>|)*\s*[a-zA-Z0-9_]*\s*,(\s*[a-zA-Z0-9_]*\s*(\+|-|\*|\\|=|<|>|)*\s*[a-zA-Z0-9_]*)*\s*,\s*[a-zA-Z0-9_]*\s*(\+|-|\*|\\|=|<|>|)*\s*[a-zA-Z0-9_]*\s*\)")
pattern_miscellaneous_data_type_cast = re.compile("\((int|float|bool|char|double|void|wchar_t)\)")
pattern_do_while = re.compile("\s*do+\s\s*")
pattern_if_else = re.compile("\s*else+\s\s*")
pattern_formal_parameter = re.compile("(int|float|bool|char|double|void|wchar_t)\s[a-zA-Z_][a-zA-Z0-9_]*\([a-zA-Z_][a-zA-Z0-9_]*(,\s*[a-zA-Z_][a-zA-Z0-9_]*)*\)")
pattern_actual_parameter1 = re.compile("[a-zA-Z_][a-zA-Z0-9_]*\([a-zA-Z_][a-zA-Z0-9_]*(,\s*[a-zA-Z_][a-zA-Z0-9_]*)*\)")
pattern_actual_parameter2 = re.compile("[a-zA-Z_][a-zA-Z0-9_]*\s*\((int|float|bool|char|double|void|wchar_t)\s*\*[a-zA-Z][a-zA-Z0-9_]*\s*(,\s*(int|float|bool|char|double|void|wchar_t)\s*\*[a-zA-Z][a-zA-Z0-9_]*)*\)")
pattern_pointer_call = re.compile("[a-zA-Z_][a-zA-Z0-9_]*\s*\((int|float|bool|char|double|void|wchar_t)\s*\*[a-zA-Z][a-zA-Z0-9_]*\s*(,\s*(int|float|bool|char|double|void|wchar_t)\s*\*[a-zA-Z][a-zA-Z0-9_]*)*\)")
pattern_reference_call = re.compile("[a-zA-Z_][a-zA-Z0-9_]*\s*\((int|float|bool|char|double|void|wchar_t)\s*&[a-zA-Z][a-zA-Z0-9_]*\s*(,\s*(int|float|bool|char|double|void|wchar_t)\s*&[a-zA-Z][a-zA-Z0-9_]*)*\)")
pattern_cos1 = re.compile("cos\((int|float|bool|char|double|void|wchar_t)\s*[a-zA-Z_][a-zA-Z0-9_]*\)")
pattern_cos2 = re.compile("cos\([a-zA-Z_][a-zA-Z0-9_]*\)")
pattern_sin1 = re.compile("sin\((int|float|bool|char|double|void|wchar_t)\s*[a-zA-Z_][a-zA-Z0-9_]*\)")
pattern_sin2 = re.compile("sin\([a-zA-Z_][a-zA-Z0-9_]*\)")
pattern_tan1 = re.compile("tan\((int|float|bool|char|double|void|wchar_t)\s*[a-zA-Z_][a-zA-Z0-9_]*\)")
pattern_tan2 = re.compile("tan\([a-zA-Z_][a-zA-Z0-9_]*\)")
pattern_log1 = re.compile("log\([a-zA-Z_][a-zA-Z0-9_]*\)")
pattern_log2 = re.compile("log10\([a-zA-Z_][a-zA-Z0-9_]*\)")
pattern_pow = re.compile("pow\((([0-9][0-9]*\.[0-9]*)|([0-9][0-9]*)|([a-zA-Z_][a-zA-Z0-9_]*)),\s*(([0-9]*)|([a-zA-Z_][a-zA-Z0-9_]*))\)")
pattern_sqrt1 = re.compile("sqrt\((int|float|bool|char|double|void|wchar_t)\s*[a-zA-Z_][a-zA-Z0-9_]*\)")
pattern_sqrt2 = re.compile("sqrt\([a-zA-Z_][a-zA-Z0-9_]*\)")
pattern_array_declaration = re.compile("(int|float|bool|char|double|void|wchar_t)\s*[a-zA-Z_][a-zA-Z0-9_]*\[[0-9][0-9]*\];")
pattern_initialize_array = re.compile("[a-zA-Z_][a-zA-Z0-9_]*\[\s*\]\s*=")
pattern_null_pointer = re.compile("\*[a-zA-Z_][a-zA-Z0-9_]*\s*=\s*NULL")
pattern_pointer_to_pointer = re.compile("\*\*[a-zA-Z_][a-zA-Z0-9_]*")
pattern_pass_pointer_to_function = re.compile("(int|float|bool|char|double|void|wchar_t)\s*[a-zA-Z_][a-zA-Z0-9_]*\((int|float|bool|char|double|void|wchar_t)\s*\*[a-zA-Z_][a-zA-Z0-9_]*\)")
pattern_return_pointer_from_function = re.compile("(int|float|bool|char|double|void|wchar_t)\s*\*\s*[a-zA-Z_][a-zA-Z0-9_]*\(\s*\)")
pattern_public_inheritance = re.compile("class\s*[A-Z][a-zA-Z0-9_]*\s*:\s*public\s*[A-Z][a-zA-Z0-9_]*")
pattern_protected_inheritance = re.compile("class\s*[A-Z][a-zA-Z0-9_]*\s*:\s*protected\s*[A-Z][a-zA-Z0-9_]*")
pattern_private_inheritance = re.compile("class\s*[A-Z][a-zA-Z0-9_]*\s*:\s*private\s*[A-Z][a-zA-Z0-9_]*")
pattern_public_member = re.compile("class\s*[A-Z][a-zA-Z0-9_]*\s*\n\n*\{\s*\n\n*\s*public:\s*\n\n*\s*(int|float|bool|char|double|void|wchar_t)\s*[a-zA-Z_][a-zA-Z0-9_]*;")
pattern_private_member = re.compile("class\s*[A-Z][a-zA-Z0-9_]*\s*\n\n*\{\s*\n\n*\s*private:\s*\n\n*\s*(int|float|bool|char|double|void|wchar_t)\s*[a-zA-Z_][a-zA-Z0-9_]*;")
pattern_protected_member = re.compile("class\s*[A-Z][a-zA-Z0-9_]*\s*\n\n*\{\s*\n\n*\s*protected:\s*\n\n*\s*(int|float|bool|char|double|void|wchar_t)\s*[a-zA-Z_][a-zA-Z0-9_]*;")

# comment
pattern_intro1 = re.compile("//")
pattern_intro2 = re.compile("/\*\S*\*/")


def check_pattern(pattern, str, knowledge, rule_name, rule):
    res = pattern.match(str)
    if res is not None:
        knowledge[rule.index(rule_name)] = 1

def rule_match(str, rule, knowledge):

    if "struct" in str:
        knowledge[rule.index("['结构']")]=1
    if "class" in str:
        knowledge[rule.index("['类']")]=1
    if "#include" in str:
        knowledge[rule.index("['预处理指令#include']")]=1
    if "inline" in str:
        knowledge[rule.index("['内置函数']")]=1
    if "iostream" in str:
        knowledge[rule.index("['iostream']")]=1
    if "iomanip" in str:
        knowledge[rule.index("['iomanip']")]=1
    if "namespace" in str:
        knowledge[rule.index("['命名空间']")]=1
    if "char" in str:
        knowledge[rule.index("['字符串']")] = 1
    if "string" in str:
        knowledge[rule.index("['String串']")] = 1
    if "friend" in str:
        knowledge[rule.index("['友元函数']")] = 1
    if "this->" in str:
        knowledge[rule.index("['this指针']")] = 1
    if "operator" in str:
        knowledge[rule.index("['运算符重载']")] = 1
    if "bool" in str:
        knowledge[rule.index("['布尔型']")] = 1
    if "int" in str:
        knowledge[rule.index("['整型']")] = 1
    if "float" in str:
        knowledge[rule.index("['浮点型']")] = 1
    if "double" in str:
        knowledge[rule.index("['双浮点型']")] = 1
    if "void" in str:
        knowledge[rule.index("['无类型']")] = 1
    if "wchar_t" in str:
        knowledge[rule.index("['宽字符串']")] = 1
    if "virtual" in str:
        knowledge[rule.index("['虚函数']")] = 1
    if "true" in str:
        knowledge[rule.index("['TRUE']")] = 1
    if "false" in str:
        knowledge[rule.index("['FALSE']")] = 1
    if "\a" in str:
        knowledge[rule.index("['警报铃声']")]=1
    if "\b" in str:
        knowledge[rule.index("['退格键']")]=1
    if "\f" in str:
        knowledge[rule.index("['换页符']")]=1
    if "\n" in str:
        knowledge[rule.index("['换行符']")]=1
    if "\r" in str:
        knowledge[rule.index("['回车']")]=1
    if "\t" in str:
        knowledge[rule.index("['水平制表符']")]=1
    if "\v" in str:
        knowledge[rule.index("['垂直制表符']")]=1
    if "const" in str:
        knowledge[rule.index("['const']")] = 1
    if "#define" in str:
        knowledge[rule.index("['#define']")] = 1
    if "signed" in str:
        knowledge[rule.index("['有符号型']")] = 1
    if "unsigned" in str:
        knowledge[rule.index("['无符号型']")] = 1
    if "long" in str:
        knowledge[rule.index("['长型']")] = 1
    if "short" in str:
        knowledge[rule.index("['短型']")] = 1
    if "+" in str:
        knowledge[rule.index("['算术运算符']")] = 1
    if "-" in str:
        knowledge[rule.index("['算术运算符']")] = 1
    if "*" in str:
        knowledge[rule.index("['算术运算符']")] = 1
    if "/" in str:
        knowledge[rule.index("['算术运算符']")] = 1
    if "%" in str:
        knowledge[rule.index("['算术运算符']")] = 1
    if "++" in str:
        knowledge[rule.index("['算术运算符']")] = 1
    if "--" in str:
        knowledge[rule.index("['算术运算符']")] = 1
    if "==" in str:
        knowledge[rule.index("['关系运算符']")] = 1
    if "!=" in str:
        knowledge[rule.index("['关系运算符']")] = 1
    if "<" in str:
        knowledge[rule.index("['关系运算符']")] = 1
    if ">" in str:
        knowledge[rule.index("['关系运算符']")] = 1
    if "<=" in str:
        knowledge[rule.index("['关系运算符']")] = 1
    if ">=" in str:
        knowledge[rule.index("['关系运算符']")] = 1
    if "&&" in str:
        knowledge[rule.index("['逻辑运算符']")] = 1
    if "||" in str:
        knowledge[rule.index("['逻辑运算符']")] = 1
    if "!" in str:
        knowledge[rule.index("['逻辑运算符']")] = 1
    if "&" in str:
        knowledge[rule.index("['位运算符']")] = 1
    if "|" in str:
        knowledge[rule.index("['位运算符']")] = 1
    if "^" in str:
        knowledge[rule.index("['位运算符']")] = 1
    if "~" in str:
        knowledge[rule.index("['位运算符']")] = 1
    if "<<" in str:
        knowledge[rule.index("['位运算符']")] = 1
    if ">>" in str:
        knowledge[rule.index("['位运算符']")] = 1
    if "=" in str:
        knowledge[rule.index("['赋值运算符']")] = 1
    if "+=" in str:
        knowledge[rule.index("['赋值运算符']")] = 1
    if "-=" in str:
        knowledge[rule.index("['赋值运算符']")] = 1
    if "*=" in str:
        knowledge[rule.index("['赋值运算符']")] = 1
    if "/=" in str:
        knowledge[rule.index("['赋值运算符']")] = 1
    if "%=" in str:
        knowledge[rule.index("['赋值运算符']")] = 1
    if "<<=" in str:
        knowledge[rule.index("['赋值运算符']")] = 1
    if ">>=" in str:
        knowledge[rule.index("['赋值运算符']")] = 1
    if "&=" in str:
        knowledge[rule.index("['赋值运算符']")] = 1
    if "|=" in str:
        knowledge[rule.index("['赋值运算符']")] = 1
    if "^=" in str:
        knowledge[rule.index("['赋值运算符']")] = 1
    if "sizeof" in str:
        knowledge[rule.index("['杂项运算符']")] = 1
    if "auto" in str:
        knowledge[rule.index("['auto存储类']")] = 1
    if "register" in str:
        knowledge[rule.index("['register存储类']")] = 1
    if "static" in str:
        knowledge[rule.index("['static存储类']")] = 1
    if "extem" in str:
        knowledge[rule.index("['extern存储类']")] = 1
    if "mutable" in str:
        knowledge[rule.index("['mutable存储类']")] = 1
    if "thread_local" in str:
        knowledge[rule.index("['thread_local存储类']")] = 1
    if "while" in str:
        knowledge[rule.index("['while循环']")] = 1
    if "for" in str:
        knowledge[rule.index("['for循环']")] = 1
    if "break" in str:
        knowledge[rule.index("['break语句']")] = 1
    if "continue" in str:
        knowledge[rule.index("['continue语句']")] = 1
    if "goto" in str:
        knowledge[rule.index("['goto语句']")] = 1
    if "if" in str:
        knowledge[rule.index("['if语句']")] = 1
    if "switch" in str:
        knowledge[rule.index("['switch语句']")] = 1
    if "main" in str:
        knowledge[rule.index("['主函数main()']")] = 1
    if "srand" in str:
        knowledge[rule.index("['随机数函数']")] = 1
    if "rand" in str:
        knowledge[rule.index("['随机数函数']")] = 1
    if "strcpy" in str:
        knowledge[rule.index("['复制字符串s2到字符串s1函数']")] = 1
    if "strcat" in str:
        knowledge[rule.index("['连接字符串s2到字符串s1的末尾函数']")] = 1
    if "strlen" in str:
        knowledge[rule.index("['返回字符串s1的长度函数']")] = 1
    if "strcmp" in str:
        knowledge[rule.index("['比较字符串s1与s2的长度并返回相应值的函数']")] = 1
    if "strchr" in str:
        knowledge[rule.index("['返回指针并指向s1中字符ch第一次出现的位置函数']")] = 1
    if "strstr" in str:
        knowledge[rule.index("['返回指针并指向s1中字符串s2第一次出现的位置函数']")] = 1
    if "fstream" in str:
        knowledge[rule.index("['fstream']")] = 1
    if "cin" in str:
        knowledge[rule.index("['标准输入流cin']")] = 1
    if "cout" in str:
        knowledge[rule.index("['标准输出流cout']")] = 1
    if "cerr" in str:
        knowledge[rule.index("['cerr']")] = 1
    if "clog" in str:
        knowledge[rule.index("['clog']")] = 1
    if "setw" in str:
        knowledge[rule.index("['setw']")] = 1
    if "setprecision" in str:
        knowledge[rule.index("['setprecision']")] = 1
    if "using" in str:
        knowledge[rule.index("['using指令']")] = 1
    if "printf" in str:
        knowledge[rule.index("['c++库函数printf()']")] = 1
    if "scanf" in str:
        knowledge[rule.index("['c++库函数scanf()']")] = 1
    if "enum" in str:
        knowledge[rule.index("['枚举类型']")] = 1

    check_pattern(pattern_deconstruct, str, knowledge, "['构造器']", rule)
    check_pattern(pattern_point, str, knowledge, "['指针']", rule)
    check_pattern(pattern_memory_address, str, knowledge, "['内存地址']", rule)
    check_pattern(pattern_func, str, knowledge, "['类成员函数']", rule)
    check_pattern(pattern_array, str, knowledge, "['访问数组元素']", rule)
    check_pattern(pattern_multiarray, str, knowledge, "['多维数组']", rule)
    check_pattern(pattern_datamember, str, knowledge, "['数据成员']", rule)
    check_pattern(pattern_pass_value_call, str, knowledge, "['传值调用']", rule)
    check_pattern(pattern_variable_declaration1, str, knowledge, "['变量声明']", rule)
    check_pattern(pattern_variable_declaration2, str, knowledge, "['变量声明']", rule)
    check_pattern(pattern_object, str, knowledge, "['对象']", rule)
    check_pattern(pattern_function_declaration, str, knowledge, "['函数声明']", rule)
    check_pattern(pattern_base_class, str, knowledge, "['基类']", rule)
    check_pattern(pattern_string, str, knowledge, "['字符串']", rule)
    check_pattern(pattern_variable_definitions, str, knowledge, "['变量定义']", rule)
    check_pattern(pattern_function_definitions, str, knowledge, "['变量定义']", rule)
    check_pattern(pattern_return_type, str, knowledge, "['返回类型']", rule)
    check_pattern(pattern_array_as_parameter1, str, knowledge, "['数组作为参数']", rule)
    check_pattern(pattern_array_as_parameter2, str, knowledge, "['数组作为参数']", rule)
    check_pattern(pattern_pointer_variable_declaration, str, knowledge, "['指针变量的声明']", rule)
    check_pattern(pattern_pointer_array, str, knowledge, "['指针数组']", rule)
    check_pattern(pattern_reference_statement, str, knowledge, "['引用声明']", rule)
    check_pattern(pattern_pointer_to_structure, str, knowledge, "['指向结构的指针']", rule)
    check_pattern(pattern_string, str, knowledge, "['String串']", rule)
    check_pattern(pattern_derived_class, str, knowledge, "['派生类'']", rule)
    check_pattern(pattern_pure_virtual_function, str, knowledge, "['纯虚函数']", rule)
    check_pattern(pattern_hexadecimal, str, knowledge, "['整数常量-十六进制']", rule)
    check_pattern(pattern_octal, str, knowledge, "['整数常量-八进制']", rule)
    check_pattern(pattern_decimal, str, knowledge, "['整数常量-十进制']", rule)
    check_pattern(pattern_float_number, str, knowledge, "['浮点常量-小数]", rule)
    check_pattern(pattern_float_e, str, knowledge, "['浮点常量-e表示小数']", rule)
    check_pattern(pattern_float_E, str, knowledge, "['浮点常量-e表示小数]", rule)
    check_pattern(pattern_str, str, knowledge, "['字符常量']", rule)
    check_pattern(pattern_miscellaneous_operator_choose, str, knowledge, "['杂项运算符-选择运算']", rule)
    check_pattern(pattern_miscellaneous_operator_comma, str, knowledge, "['杂项运算符-逗号运算']", rule)
    check_pattern(pattern_miscellaneous_data_type_cast, str, knowledge, "['杂项运算符-强制转换数据类型']", rule)
    check_pattern(pattern_do_while, str, knowledge, "['do-while循环']", rule)
    check_pattern(pattern_if_else, str, knowledge, "['if-else循环']", rule)
    check_pattern(pattern_formal_parameter, str, knowledge, "['形式参数']", rule)
    check_pattern(pattern_actual_parameter1, str, knowledge, "['实际参数']", rule)
    check_pattern(pattern_actual_parameter2, str, knowledge, "['实际参数']", rule)
    check_pattern(pattern_pointer_call, str, knowledge, "['指针调用']", rule)
    check_pattern(pattern_reference_call, str, knowledge, "['引用调用']", rule)
    check_pattern(pattern_cos1, str, knowledge, "['余弦函数']", rule)
    check_pattern(pattern_cos2, str, knowledge, "['余弦函数']", rule)
    check_pattern(pattern_sin1, str, knowledge, "['正弦函数']", rule)
    check_pattern(pattern_sin2, str, knowledge, "['正弦函数']", rule)
    check_pattern(pattern_tan1, str, knowledge, "['正切函数']", rule)
    check_pattern(pattern_tan2, str, knowledge, "['正切函数']", rule)
    check_pattern(pattern_log1, str, knowledge, "['对数函数']", rule)
    check_pattern(pattern_log2, str, knowledge, "['对数函数']", rule)
    check_pattern(pattern_pow, str, knowledge, "['指数函数']", rule)
    check_pattern(pattern_sqrt1, str, knowledge, "['平方根函数']", rule)
    check_pattern(pattern_sqrt2, str, knowledge, "['平方根函数']", rule)
    check_pattern(pattern_array_declaration, str, knowledge, "['数组声明']", rule)
    check_pattern(pattern_initialize_array, str, knowledge, "['初始化数组']", rule)
    check_pattern(pattern_null_pointer, str, knowledge, "['空指针']", rule)
    check_pattern(pattern_pointer_to_pointer, str, knowledge, "['指向指针的指针']", rule)
    check_pattern(pattern_pass_pointer_to_function, str, knowledge, "['传递指针给函数']", rule)
    check_pattern(pattern_return_pointer_from_function, str, knowledge, "['从函数返回指针']", rule)
    check_pattern(pattern_public_inheritance, str, knowledge, "['公有继承']", rule)
    check_pattern(pattern_protected_inheritance, str, knowledge, "['保护继承']", rule)
    check_pattern(pattern_private_inheritance, str, knowledge, "['私有继承']", rule)
    check_pattern(pattern_public_member, str, knowledge, "['公有成员']", rule)
    check_pattern(pattern_private_member, str, knowledge, "['私有成员']", rule)
    check_pattern(pattern_protected_member, str, knowledge, "['私有成员']", rule)

    return knowledge


if __name__ == '__main__':
    df_answer = pd.read_csv("./challenge_answer.csv")
    with open("./code_knowledge.pkl","rb") as file:
        code_knowledge = pickle.load(file)[0:181]
    result_rule = []

    for i, row in df_answer.iterrows():
        knowledge = [0]*181
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
            knowledge = rule_match(tmpstr, code_knowledge, knowledge)

        result_rule.append(knowledge)
    with open("./code_rule.pkl","wb") as file:
        pickle.dump(result_rule, file)
