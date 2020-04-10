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
import random

headers = { 'apikey': 'd36b3620-6081-11ea-8cd5-6df14d96169d' }
temp_path = './crawling_data/temp/'

# def fetch_async(query_content, description, url):
def fetch_async(query_data):
    query_content, description, url = query_data
    try:
        response = requests.get(url).text
    except Exception as e:
        with open("./log/source_page_err.log", 'a') as sourepage_err_file:  
            print(query_content + "error is: " + str(e)) 
            response = None
    # return query_content, url, description, response

# def callback(future):
    # query_content, url, description, response = future.result()
    if not response is None:
        knowledage_dict=dict()
        knowledage_dict["des"] = description
        knowledage_dict["url"] = url
        knowledage_dict["url_source_page"] = response
        if not os.path.exists(os.path.join(temp_path, query_content)):
            os.makedirs(os.path.join(temp_path, query_content))
        with open(os.path.join(temp_path, query_content, url.replace('/', '_')), "wb") as resultfile:
            pickle.dump(knowledage_dict, resultfile)
    return query_content

def crawler():
    # 读取中间结果
    info_dict = []
    for dirpath, dirnames, filenames in os.walk(temp_path):
        for fname in filenames:
            file_path = os.path.join(temp_path, fname)
            with open(file_path, 'rb') as f:
                sub_list = pickle.load(f)
                for info in sub_list:
                    info_dict.append( (fname.split('.')[0], info['description'], info['url']) )
                # info_dict.append({fname.split('.')[0]: pickle.load(f)})

    # # 遍历每一条记录
    cores = multiprocessing.cpu_count()
    pool = ProcessPoolExecutor(cores)
    finish_query_set = []
    # with futures.ProcessPoolExecutor() as pool:
    for query_content in pool.map(fetch_async, info_dict):
        finish_query_set.append(query_content)

    # for _dict in info_dict:
    #     for query_content, info_list in _dict.items():
    #         for info in info_list:
    #             # v = pool.submit(fetch_async, query_content, info['description'], info['url'])
    #             # v.add_done_callback(callback)
    # pool.shutdown(wait=True)

if __name__ == "__main__":
    crawler()