# -*- encoding: utf-8 -*-
# use python3 to run this code

import numpy as np
import os
import io
import pdb

repo_rules = open('data/git_data/repo_ruleid_all.txt').readlines()[2:]
knowledge = np.loadtxt('data/git_data/match_result_newdata.txt')
# key_name_for_result.txt records the repo name
repo_name_list = open('data/git_data/repo_name_list.txt').readlines() 

knowledge_num = knowledge.shape[1]

# get all knowledge given a repo
repos_knowledge_dict = {}
for i in range(len(repo_name_list)):
    repos_knowledge_dict[repo_name_list[i].strip('\n')] = knowledge[i, :]
    # task_name = repo_name_list[i].split('_')[1] + '_' + repo_name_list[i].split('_')[-1]
    # if task_name not in repos_knowledge_dict.keys():
    #     repos_knowledge_dict[repo_name_list[i]] = [knowledge[i, :]]
    # else: 
    #     repos_knowledge_dict[repo_name_list[i]].append(knowledge[i, :])

rulesid_content_dict = {}
rulesid_content_list = []
rulesid_repos_dict = {}
for i in range(len(repo_rules)):
    repo_name, ruleid, rule_content = repo_rules[i].split('|')[:3]
    repo_name = repo_name.strip(' ')
    ruleid = ruleid.strip(' ')
    rule_content = rule_content.strip(' ')
    if '_' not in repo_name:
        continue # filter LZ1 repo
    if ruleid not in rulesid_content_dict.keys():
        rulesid_content_dict[ruleid] = rule_content
        rulesid_content_list.append(ruleid + '|' + rule_content + '\n')
    
    # get all repos that may involves a given rule
    if ruleid not in rulesid_repos_dict.keys():
        rulesid_repos_dict[ruleid] = [repo_name]
    else :
        rulesid_repos_dict[ruleid].append(repo_name)
    
rulesid_to_content_out = open('./data/git_data/rulesid_to_content.txt', 'w')
rulesid_to_content_out.writelines("".join(rulesid_content_list))
rulesid_to_content_out.close()


rulesid_knowledge_list = []
# link the rulesid_repos_dict to repos_knowledge_dict by taskid
for rule_id, repos_list in rulesid_repos_dict.items():
    involved_knowledge = np.ones(knowledge_num)
    print(rule_id),
    for repo in repos_list:
        print(repo)
        involved_knowledge = involved_knowledge * repos_knowledge_dict[repo]
    
    involved_knowledge_str = ''
    for i in list(involved_knowledge):
        involved_knowledge_str += str(i) + ' '
    rulesid_knowledge_list.append(str(rule_id) + ' ' + involved_knowledge_str + '\n')

rulesid_knowledge_out = open('./data/git_data/rulesid_to_knowledge.txt', 'w')
rulesid_knowledge_out.writelines("".join(rulesid_knowledge_list))
rulesid_knowledge_out.close()


# # compute the std
# rulesid_knowledge_result = np.loadtxt('./data/git_data/rulesid_to_knowledge.txt')[:, 1:]
# rule2knowledge_std = np.std(rulesid_knowledge_result, axis=0)
# pdb.set_trace()