# -*- encoding: utf-8 -*-
# use python3 to run this code

import numpy as np
import os
import io
import pdb

keyname_rules = open('data/git_data/taskid_ruleid.txt').readlines()[2:]
knowledge = np.loadtxt('data/git_data/match_result_newdata.txt')
knowledge_keyname = open('data/git_data/key_name_for_result.txt').readlines()

knowledge_num = knowledge.shape[1]

# get all knowledge given a repo
repos_knowledge_dict = {}
for i in range(len(knowledge_keyname)):
    repos_knowledge_dict[knowledge_keyname[i].strip('\n')] = knowledge[i, :]
    # task_name = knowledge_keyname[i].split('_')[1] + '_' + knowledge_keyname[i].split('_')[-1]
    # if task_name not in repos_knowledge_dict.keys():
    #     repos_knowledge_dict[knowledge_keyname[i]] = [knowledge[i, :]]
    # else: 
    #     repos_knowledge_dict[knowledge_keyname[i]].append(knowledge[i, :])

rulesid_content_dict = {}
rulesid_content_list = []
rulesid_repos_dict = {}
for i in range(len(keyname_rules)):
    keyname, ruleid, rule_content = keyname_rules[i].split('|')[:3]
    keyname = keyname.strip(' ')
    ruleid = ruleid.strip(' ')
    rule_content = rule_content.strip(' ')
    if '_' not in keyname:
        continue
    if ruleid not in rulesid_content_dict.keys():
        rulesid_content_dict[ruleid] = rule_content
        rulesid_content_list.append(ruleid + '|' + rule_content + '\n')
    
    # get all repos that may involves a given rule
    if ruleid not in rulesid_repos_dict.keys():
        rulesid_repos_dict[ruleid] = [keyname]
    else :
        rulesid_repos_dict[ruleid].append(keyname)
    
rulesid_to_content_out = open('./data/git_data/rulesid_to_content.txt', 'w')
rulesid_to_content_out.writelines("".join(rulesid_content_list))
rulesid_to_content_out.close()


rulesid_knowledge_list = []
# link the rulesid_repos_dict to repos_knowledge_dict by taskid
for rule_id, repos_list in rulesid_repos_dict.items():
    involved_knowledge = np.ones(knowledge_num)
    for repo in repos_list:
        involved_knowledge = involved_knowledge * repos_knowledge_dict[repo]
    
    involved_knowledge_str = ''
    for i in list(involved_knowledge):
        involved_knowledge_str += str(i) + ' '
    rulesid_knowledge_list.append(str(rule_id) + ' ' + involved_knowledge_str + '\n')

rulesid_knowledge_out = open('./data/git_data/rulesid_to_knowledge.txt', 'w')
rulesid_knowledge_out.writelines("".join(rulesid_knowledge_list))
rulesid_knowledge_out.close()
