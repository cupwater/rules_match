import csv
import numpy as np
import pdb

errinfo_errid_dict = {}
errid = 0
def parse_compile_error_info(info_str):
    global errid
    global errinfo_errid_dict
    lines = info_str.split('\r\n')
    err_id_list = []
    for line in lines:
        if 'error' in line:
            temp = line.split('error')[-1]
            errinfo = temp.split('\'')[0] + temp.split('\'')[-1]
            if len(errinfo)<3:
                continue
            if errinfo not in errinfo_errid_dict.keys():
                errinfo_errid_dict[errinfo] = errid
                errid += 1
                err_id_list.append(errid)
            else:
                err_id_list.append(errinfo_errid_dict[errinfo])
    return list(set(err_id_list))

csv.field_size_limit(100000000)
f_csv = csv.reader(x.replace('\0', '') for x in open('../actual_outputs4.csv'))
headers = next(f_csv)
compile_success = []
res_compile_err = []
index = 0
for row in f_csv:
    # if index > 3000000:
    #     break
    # index += 1
    _, out_put, actual_output, git_url, repo_name, shixun_id = row
    if 'successfully' in out_put:
        continue
    else:
        current_err_list = parse_compile_error_info(out_put)
        res_compile_err.append( (repo_name, shixun_id, current_err_list ) )


err_out = open('compile_err_dict.txt', 'w')
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
res_out = open('compile_err_res.txt', 'w')
# remove repeated items
hashable_compile_err = list(set(hashable_compile_err))
for item in hashable_compile_err:
    res_out.write(item)
res_out.close()

# pdb.set_trace()
