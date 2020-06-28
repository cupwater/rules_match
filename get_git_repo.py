import numpy as np
import os
import multiprocessing
content = open('./data/sqlresult_4890248.csv').readlines()[1:]
git_repo_path_list = [line.split(',')[5] for line in content]
git_repo_path_list = [ line + '_' + str(i+1) for i,line in enumerate(git_repo_path_list) ]
dst_root = '/Users/cupwaterpeng/code/sonar/git_data_temp/'
git_repo_path_list = list(set(git_repo_path_list))
def get_fun(_git_path_index):
    _git_path, index = _git_path_index.split('_')
    dst_path =  index + '_' + _git_path.split('/')[-1].split('.')[0]
    os.system('git clone %s %s' % (_git_path, os.path.join(dst_root, dst_path )))

pool = multiprocessing.Pool(processes=10)
print(pool.map(get_fun, git_repo_path_list))