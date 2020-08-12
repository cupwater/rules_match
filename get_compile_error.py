# -*- coding: utf8
import csv
import numpy as np
import multiprocessing
import pdb

csv.field_size_limit(100000000)
sth = 0.5 # similar threshold
errinfo_errid_dict = {}
errid = 0
eps=0.01

def getSimilarRatioOfCommonSubstr(ori_str1, ori_str2):
    def parse_str(in_str):
        split_str = in_str.split('\'')
        res_str = ""
        for i in range(len(split_str)):
            if i%2==0:
                res_str += split_str[i]
        return res_str
    str1 = parse_str(ori_str1).replace(' ', '')
    str2 = parse_str(ori_str2).replace(' ', '')
    lstr1 = len(str1)
    lstr2 = len(str2)
    if (float(lstr2) / (lstr1+eps) > sth) or float(lstr1) / (lstr2+eps) < sth:
        return 0
    record = [[0 for i in range(lstr2+1)] for j in range(lstr1+1)]
    maxNum = 0 
    p = 0
    for i in range(lstr1):
        for j in range(lstr2):
            if str1[i] == str2[j]:
                record[i+1][j+1] = record[i][j] + 1
                if record[i+1][j+1] > maxNum:
                    maxNum = record[i+1][j+1]
                    p = i + 1
    # return str1[p-maxNum:p], maxNum
    return 2*float(maxNum) / float((len(str1)+len(str2)))

def union_find(nodes, edges):
    father = [0]*len(nodes) 
    for node in nodes:
        father[node] = node
    for edge in edges:  # 标记父节点
        head = edge[0]
        tail = edge[1]
        father[tail] = head

    for node in nodes:
        while True:
            father_of_node = father[node]
            if father_of_node != father[father_of_node]:
                father[node] = father[father_of_node]
            else:
                break
    return father
 
# extract the error content from a string
def parse_err_content(err_content):
    err_content = err_content.replace('‘', '$').replace('’', '$')
    split_str = err_content.split('$')
    res_str = ""
    for i in range(len(split_str)):
        if i%2==0:
            res_str += split_str[i]
    #pdb.set_trace()
    return res_str

def parse_compile_error_info(info_str):
    global errid
    global errinfo_errid_dict
    lines = info_str.split('\n')
    err_id_list = []
    for line in lines:
        if 'error' in line:
            temp = line.split('error')[-1]
            errinfo = parse_err_content(temp)
            #errinfo = temp.split('\'')[0] + temp.split('\'')[-1]
            #pdb.set_trace()
            if len(errinfo)<5:
                continue
            if errinfo not in errinfo_errid_dict.keys():
                errinfo_errid_dict[errinfo] = errid
                err_id_list.append(errid)
                errid += 1
            else:
                err_id_list.append(errinfo_errid_dict[errinfo])
    return list(set(err_id_list))

f_csv = csv.reader(x.replace('\0', '') for x in open('./actual_outputs4.csv'))
headers = next(f_csv)
res_compile_err = []
index = 0
for row in f_csv:
    if index % 1000 == 0:
        print('parse {}'.format(str(index)), flush=True)
    index += 1
    _, out_put, actual_output, git_url, repo_name, shixun_id = row
    if 'successfully' in out_put:
        continue
    else:
        current_err_list = parse_compile_error_info(out_put)
        res_compile_err.append( (repo_name, shixun_id, current_err_list ) )


err_out = open('compile_err_dict_before_merge.txt', 'w')
for k, v in errinfo_errid_dict.items():
    err_out.write(k + ': ' + str(v) + '\n')
err_out.close()

hashable_compile_err = []
for (repo_name, shixun_id, current_err_list) in res_compile_err:
    err_list_str = "["
    for _id in current_err_list:
        err_list_str += str(_id) + ","
    err_list_str += "]"
    hashable_compile_err.append(repo_name.strip('\r').strip('\n') + '\t' + str(shixun_id) + '\t' + err_list_str + '\n')
res_out = open('compile_err_res_before_merge.txt', 'w')
# remove repeated items
hashable_compile_err = list(set(hashable_compile_err))
for item in hashable_compile_err:
    res_out.write(item)
res_out.close()


def common_substr_fun(i):
    similarity_vec = np.zeros(len(errinfo_list))
    similarity_vec[i] = 1
    for j in range(i+1, len(errinfo_list)):
        similarity_vec[j] = getSimilarRatioOfCommonSubstr(errinfo_list[i], errinfo_list[j])
    return similarity_vec


# merge highly similar errors in errinfo_errid_dict
errinfo_list = list(errinfo_errid_dict.keys())
print('length of error information list: {}'.format(str(len(errinfo_list))), flush=True)
pool = multiprocessing.Pool(processes=48)
similarity_vec_list = pool.map(common_substr_fun, range( len(errinfo_list)-1 ) )
# for i in range( len(errinfo_list)-1 ):
    # common_substr_fun(i)

similarity_matrix = np.array(similarity_vec_list).reshape(-1, len(errinfo_list))
print('max common sub-string finished', flush=True)


similarity_matrix[ similarity_matrix > sth ] = 1
nodes = sorted(list(errinfo_errid_dict.values()))
edges = []
for i in range(similarity_matrix.shape[0]-1):
    for j in range(i+1, similarity_matrix.shape[1]):
        if similarity_matrix[i, j] == 1:
            edges.append([i, j])
nodes_father = union_find(nodes, edges)
print('union-find finished', flush=True)


err_out = open('compile_err_dict_after_merge.txt', 'w')
for father_node in set(nodes_father):
    err_out.write(errinfo_list[father_node] + ': ' + str(father_node) + '\n')
err_out.close()
hashable_compile_err = []
for (repo_name, shixun_id, current_err_list) in res_compile_err:
    # update error id lists due to error merge
    merged_err_list = []
    for errid in current_err_list:
        merged_err_list.append(nodes_father[errid])
    merged_err_list = list(set(merged_err_list))
    err_list_str = "["
    for _id in merged_err_list:
        err_list_str += str(_id) + ","
    err_list_str += "]"
    hashable_compile_err.append(repo_name.strip('\r').strip('\n') + '\t' + str(shixun_id) + '\t' + err_list_str + '\n')
res_out = open('compile_err_res_after_merge.txt', 'w')
# remove repeated items
hashable_compile_err = list(set(hashable_compile_err))
for item in hashable_compile_err:
    res_out.write(item)
res_out.close()
