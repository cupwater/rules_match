import csv
import numpy as np
import pdb

similar_threshold = 0.5
errinfo_errid_dict = {}
errid = 0

def getSimilarRatioOfCommonSubstr(str1, str2):
    lstr1 = len(str1)
    lstr2 = len(str2)
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
    return float(maxNum) / float((len(str1)+len(str2)))

def union_find(nodes, edges):
    node_father = {}
    for node in nodes:
        node_father[node] = node
    for edge in edges:
        if node_father[edge[1]] == edge[1]:
            node_father[edge[1]] = edge[0]
        else:
            node_father[edge[0]] = edge[1]

    for node in nodes:
        father = node_father[node]
        print(node)
        while father != node_father[father]:
            father = node_father[father]
        node_father[node] = father
    return node_father

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
                errid += 1
                err_id_list.append(errid)
            else:
                err_id_list.append(errinfo_errid_dict[errinfo])
    return list(set(err_id_list))

csv.field_size_limit(100000000)
f_csv = csv.reader(x.replace('\0', '') for x in open('./actual_outputs4.csv'))
headers = next(f_csv)
compile_success = []
res_compile_err = []
index = 0
for row in f_csv:
    if index % 1000 == 0:
        print('parse {}'.format(str(index)), flush=True)
    index += 1
    if index > 100000:
        break
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


# merge highly similar errors in errinfo_errid_dict
errinfo_list = list(errinfo_errid_dict.keys())
similarity_matrix = np.eye(len(errinfo_list))
for i in range(len(errinfo_list)):
    for j in range(i, len(errinfo_list)):
        similarity_matrix[i, j] = getSimilarRatioOfCommonSubstr(errinfo_list[i], errinfo_list[j])
        similarity_matrix[j, i] = getSimilarRatioOfCommonSubstr(errinfo_list[i], errinfo_list[j])


similarity_matrix[ similarity_matrix > similar_threshold ] = 1
nodes = sorted(list(errinfo_errid_dict.values()))
edges = []
for i in range(similarity_matrix.shape[0]):
    for j in range(i, similarity_matrix.shape[1]):
        if similarity_matrix[i, j] == 1:
            edges.append([i, j])
node_father = union_find(nodes, edges)

err_out = open('compile_err_dict_after_merge.txt', 'w')
for node in list(node_father.values()):
    err_out.write(errinfo_list[node] + ': ' + str(node) + '\n')
err_out.close()

hashable_compile_err = []
for (repo_name, shixun_id, current_err_list) in res_compile_err:
    # update error id lists due to error merge
    merged_err_list = []
    for errid in current_err_list:
        merged_err_list.append(node_father[errid])
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
