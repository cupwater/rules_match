import numpy as np
import os
import multiprocessing
content = open('./data/sqlresult_4890248.csv').readlines()[1:]

repo_dict = {}
for i in range(len(content)):
    _, task_name, shixun_id, identifier, game_id, repo_url, user_id, username  = content[i].strip('\n').split(',')
    key = repo_url + '_' + task_name
    if key in repo_dict:
        continue
    repo_dict[key] = str(i+1)

git_repo_path_list = []
for key, value in repo_dict.items():
    repo_path = key.split('_')[0]
    idx = value
    git_repo_path_list.append(repo_path + '_' + str(idx))


# git_repo_path_list = [line.split(',')[5] for line in content]
# git_repo_path_list = list(set(git_repo_path_list))
# git_repo_path_list = [ line + '_' + str(i+1) for i,line in enumerate(git_repo_path_list) ]


dst_root = '/Volumes/Data/sonar_code_repos/'
print(len(git_repo_path_list))

def get_fun(_git_path_index):
    _git_path, index = _git_path_index.split('_')
    dst_path =  index + '_' + _git_path.split('/')[-1].split('.')[0]
    os.system('git clone %s %s' % (_git_path, os.path.join(dst_root, dst_path )))

pool = multiprocessing.Pool(processes=10)
print(pool.map(get_fun, git_repo_path_list))