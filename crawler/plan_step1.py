# -*- coding: utf-8

import requests
import json
import pickle
import time
from concurrent import futures
from concurrent.futures import ProcessPoolExecutor
import multiprocessing
import os
import pdb

headers = { 'apikey': 'd36b3620-6081-11ea-8cd5-6df14d96169d' }
temp_path = './crawling_data/temp/'
# 解析请求数据
def parser_query(query_content):
    global info_dict
    knowledage_dict = dict()
    query_knowledage = "what is " + "\"" + query_content + "\"" + " in C++ "
    params = (
        ('q', query_knowledage),
        ('device', 'desktop'),
        ('location', 'United States'),
        ('search_engine', 'google.com'),
        ('hl', 'en'),
        ('num', '71')
    )
    try:
        response = str(requests.get('https://app.zenserp.com/api/v2/search', headers=headers, params=params).content, encoding='utf-8')
    except Exception as e:
        print('error, no {}'.format(query_content))
        with open("./log/err.log", 'a') as err_file:        
            err_file.write(query_knowledage + "error is: " + str(e) + '\n')
        return None
    response_json = json.loads(response)
    query_result = []
    for info in response_json["organic"]:
        if "description" in info:
            query_result.append(info)
    with open(os.path.join(temp_path, "{}.pkl".format(query_content)), "wb") as resultfile:
        pickle.dump(query_result, resultfile)

def crawler():
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)
    info_dict = list()
    ###获取知识点
    lines = open("./chin_name2eng_name_process.txt", 'r', encoding='utf-8').readlines()
    query_list = [line.split(":")[2].strip("\n") for line in lines]
    finish_query_set = []
    # for query in query_list:
    #     parser_query(query)
    with futures.ProcessPoolExecutor() as pool:
        for query_content in pool.map(parser_query, query_list):
            finish_query_set.append(query_content)
    pool.shutdown(wait=True)

if __name__ == "__main__":
    crawler()