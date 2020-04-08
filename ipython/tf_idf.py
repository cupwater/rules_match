# coding: utf-8
import xlwt
import xlrd
from xlutils.copy import copy
import re



# 计算 IDF
# docList 为所有文档的 list
def computeIDF(docList):
    import math
    # 用一个字典对象保存 IDF
    idfDict = {}
    N = len(docList)    # 语料库的文档总数
    
    # 初始化 idfDict 字典，已备后续计算填入值
    # docList[0].keys(): 取出第一个文档（字典）里的所有 keys，分别是 ['dog', 'on', 'cat', 'my', 'sat', 'The', 'bed', 'face']
    # 其实取第几个文档的字典里的 keys 都一样，在前面我们已经把所有词都放入了每个文档里，只不过 value 值不一样，相当于 one-hot
    # dict.fromkeys(docList[0].keys(), 0): 再另所有 keys 的 value 为 0，分别是 {'dog': 0, 'on': 0, 'cat': 0, 'my': 0, 'sat': 0, 'The': 0, 'bed': 0, 'face': 0}
    idfDict = dict.fromkeys(docList[0].keys(), 0)
    for doc in docList: # docList = [wordDictA, wordDictB]
        for word, val in doc.items():
            if val > 0:
                # idfDict 为一个统计词典，遍历每一个文档，把出现过至少一次的词对应在 idfDict 字典中的 value 都+1，则 value 就能表示改词在几个文档中出现过
                idfDict[word] += 1  
    
    for word, val in idfDict.items():
        idfDict[word] = math.log10(N / float(val))  # log() 计算 math.log10()
        
    return idfDict


# workbook = xlrd.open_workbook(r'../data/c++_rule_opt.xls')
workbook = xlrd.open_workbook(r'../data/sonar_rule.xls')
# 通过index来获得一个sheet对象，index从0开始算起
sheet = workbook.sheet_by_index(0)
print(sheet.name)   # sheet 的名字
print (sheet.nrows) # sheet 的行数

word_bag = []
word_set = []
for i in range(sheet.nrows):
    # 获得特定的cell对象的值
    str_cell = sheet.cell(i,0).value
    # 去掉每行句子头尾的双引号
    str_cell = str_cell.strip('"')
    # 去掉每行句子中的双引号
    str_cell = str_cell.replace('"', '')
    # 把每行的句子用空格分成若干个词
    word_set = str_cell.split(" ")

    #print(word_set)
    word_bag.append(word_set)
print(word_bag)

# word_bag 为词袋，里面存着所有文本中出现过的词
# set() 函数创建一个无序不重复元素集
word_bag_union = []
for i in range(sheet.nrows-1):
    word_bag_union_tmp = set(word_bag[i]).union(set(word_bag[i+1]))
    word_bag_union = set.union(word_bag_union_tmp, word_bag_union)
    # for k,v in word_bag_union_tmp.items():
    #     word_bag_union[k] = v
    # word_bag_union = dict(word_bag_union_tmp.items() + word_bag_union.items())
# print(word_bag_union)

for i in range(sheet.nrows):
    # dict.fromkeys(docList[0].keys(), 0): 再另所有 keys 的 value 为 0，分别是 {'dog': 0, 'on': 0, 'cat': 0, 'my': 0, 'sat': 0, 'The': 0, 'bed': 0, 'face': 0}
    wordDict = dict.fromkeys(word_bag_union, 0)
    # 动态生成变量 wordDict_0 ... wordDict_438，并把 value 为 0 赋给每个 key
    exec('wordDict_{} = {}'.format(i, wordDict))

print(sheet.nrows)

# print(wordDict_0)
print(wordDict_438)
