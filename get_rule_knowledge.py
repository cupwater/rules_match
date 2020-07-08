import numpy as np
import os

keyname_rules = open('data/git_data/taskid_ruleid.txt').readlines()[2:]
knowledge = np.loadtxt('data/git_data/match_result_newdata.txt')
knowledge_keyname_index = open('data/git_data/key_name_for_result.txt').readlines()

# get the keyname and knowledge
keyname_knowledge_dict = {}
for i in range(len(knowledge_keyname_index)):
    keyname_knowledge_dict[knowledge_keyname_index[i]] = knowledge[i, :]


rulesid_content_dict = {}
rulesid_content_list = []
for i in range(len(keyname_rules)):
    keyname, ruleid, rule_content = keyname_rules[i].split('|')[:3]
    keyname = keyname.strip(' ')
    ruleid = ruleid.strip(' ')
    if '_' not in keyname:
        continue
    if ruleid not in rulesid_content_dict.keys():
        rulesid_content_dict[ruleid] = rule_content
        rulesid_content_list.append(ruleid + '|' + rule_content + '\n')
rulesid_to_content_out = open('./data/git_data/rulesid_to_content.txt', 'w')
rulesid_to_content_out.writelines("".join(rulesid_content_list))
rulesid_to_content_out.close()

# get the keyname and rules
keyname_rules_dict = {}
for i in range(len(keyname_rules)):
    print(keyname_rules[i].split('|'))
    keyname, ruleid, rule_content = keyname_rules[i].split('|')[:3]
    if '_' not in keyname:
        continue 
    if keyname not in keyname_rules_dict.keys():
        keyname_rules_dict[keyname] = [ruleid]
    else: 
        keyname_rules_dict[keyname].append(ruleid)


    



