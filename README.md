./data/ 目录下的各个文件

challenge_answer.csv: 代码片段集合 

pattern_name.txt: 使用到的所有知识点的名字 

name2semantic.txt: 知识点的名字及其对应的中文语义 

match_result.txt: 知识点匹配结果矩阵， 1 表示代码段包含相应的知识点， 0 表示不包含 

corpo_pairs_res.txt: 在代码段内同时出现的两个知识点，及出现的总次数 

cpp_prerequisite.csv: 基于人力标记的前驱后继关系


关卡(step)，一共 19747 条，路径保存于 data/git_data/repo_name_list.txt。知识点（正则式）一共有176条，保存于 pattern_name_num.txt 

步骤：
## 1. 获取关卡到知识点的映射（git_knowledge_from_git.py）。对所有关卡代码扫描，使用正则式进行知识点匹配，得到关卡到knowledge映射结果，以矩阵形式(19747x176)保存在 data/git_data/repo_knowledge_corresponding_matrix.txt； 
应该对标准代码进行正则式扫描，且标准代码应当包含 challenge_id,shuxun_id ，可以从其获取到challenge_id,shuxun_id和 知识点的映射关系 保存在 standardcode_to_knowledge.txt。

2. 获取关卡到sonar规则的映射（scan_all_repo.py ）。对所有关卡代码使用 sonar 扫描，得到每个关卡的代码违反的 sonar 规则，这部分是使用 sonar + cppcheck 工具完成的，结果保存在 data/git_data/repo_ruleid_all.txt。
   
## 3. 获取规则到知识点的匹配（get_rule_knowledge.py）。根据步骤1 repo_knowledge_corresponding_matrix.txt和步骤2的结果repo_ruleid_all.txt，来建立 rule 到 knowledge 的映射关系，结果以矩阵形式 (规则数量x知识点数量) 保存在 data/git_data/rulesid_knowledge_out.txt。第一列记录了规则的编号，规则编号到规则内容的映射记录在 rulesid_to_content.txt 文件里。

3. 获取规则到知识点的匹配（get_rule_knowledge.py）。根据步骤1 standardcode_to_knowledge.txt 和步骤2的结果repo_ruleid_all.txt，（利用challenge_id）来建立 rule 到 knowledge 的映射关系，结果以矩阵形式 (规则数量x知识点数量) 保存在 data/git_data/rulesid_knowledge_out.txt。第一列记录了规则的编号，规则编号到规则内容的映射记录在 rulesid_to_content.txt 文件里。
   

4. 获取学生提交的关卡代码出现的所有编译错误（get_compile_error.py 对 ../compile_err_4_c++.csv进行处理).涉及到的步骤是：1. 由于 compile_err_4_c++ 并没有给错误编号，只给出了错误消息字符串，对所有错误消息字符串进行归类合并编号，涉及到的算法是最长公共子序列和并查集，结果保存在 data/new_data/compile_err_dict_after_merge.txt（错误内容 和 error_ID）；2. 获取关卡到error_ID 的对应关系。

5. 获取error_ID 到 knowledge 的对应关系.