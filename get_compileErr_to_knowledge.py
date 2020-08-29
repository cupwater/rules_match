# -*- encoding: utf-8 -*-
# use python3 to run this code

import numpy as np
import os
import io
import pdb

repo_errs = open('data/git_data/repoUrl_shixunid_errlist.txt').readlines()
knowledge = np.loadtxt('data/git_data/repo_knowledge_corresponding_matrix.txt')
repo_name_list = open('data/git_data/repo_name_list.txt').readlines() 

knowledge_num = knowledge.shape[1]

# get all knowledge given a repo
repos_knowledge_dict = {}
merged_repos_knowledge_dict = {}
for i in range(len(repo_name_list)):
    # since multiple repos belong to the same task, involve same knowledge, we merge those repos into a single one
    repo_url = repo_name_list[i].strip('\n').split('_')[-2:]
    repo_url = repo_url[0] + '_' + repo_url[1]
    if repo_url not in merged_repos_knowledge_dict.keys():
        merged_repos_knowledge_dict[repo_url] = knowledge[i, :]
    else:
        merged_repos_knowledge_dict[repo_url] += knowledge[i, :]
    repos_knowledge_dict[repo_name_list[i].strip('\n')] = knowledge[i, :]

errid_content_dict = {}
errid_repos_dict = {}
for i in range(len(repo_errs)):
    repo_url, shixun_id, err_ids = repo_errs[i].strip('\n').split(' ')
    # we need to process the repo_url
    repo_url = repo_url.strip('\n')
    err_ids = err_ids.strip(',').split(',')
    for _id in err_ids:
        if _id not in errid_repos_dict.keys():
            errid_repos_dict[_id] = [repo_url]
        else :
            errid_repos_dict[_id].append(repo_url)


errid_knowledge_list = []
# link the errid_repos_dict to repos_knowledge_dict by taskid
for error_id, repos_list in errid_repos_dict.items():
    involved_knowledge = np.ones(knowledge_num)
    for repo in repos_list:
        if repo in merged_repos_knowledge_dict:
            involved_knowledge = involved_knowledge * merged_repos_knowledge_dict[repo]
        else:
            continue # do nothing
    involved_knowledge_str = ''
    for i in list(involved_knowledge):
        involved_knowledge_str += ('1' if i>0 else '0') + ' '
    if '0' not in involved_knowledge_str or '1' not in involved_knowledge_str:
        continue
    errid_knowledge_list.append(str(error_id) + ' ' + involved_knowledge_str + '\n')

errid_knowledge_out = open('./data/git_data/errid_to_knowledge.txt', 'w')
errid_knowledge_out.writelines("".join(errid_knowledge_list))
errid_knowledge_out.close()