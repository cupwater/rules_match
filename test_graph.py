import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

corpo_pairs_list = open('./data/corpo_pairs_res.txt').readlines()

G = nx.Graph()
name_index_list = {}
index = 0
for _pair in corpo_pairs_list:
    _, pair_a, _, pair_b, _ = _pair.split(',')
    if pair_a not in name_index_list:
        name_index_list[pair_a] = str(index)
        index += 1
    if pair_b not in name_index_list:
        name_index_list[pair_b] = str(index)
        index += 1
    # print(pair_a + ',' + pair_b)
    G.add_edge(pair_a, pair_b)
# nx.draw(G)
# plt.savefig("path.png")
from networkx.algorithms.centrality import degree_centrality, closeness_centrality,betweenness_centrality,communicability_betweenness_centrality
degree_res = degree_centrality(G)
closeness_res = closeness_centrality(G)
betweenness_res = communicability_betweenness_centrality(G)


centrality_out = open('./data/centrality.txt', 'w')
centrality_out.write('pattern,degree,closeness,betweenness')
for key, value in degree_res.items():
    centrality_out.write('\n' + key + '\t %.2f \t %.2f \t %.2f'%(value,closeness_res[key],betweenness_res[key]))
centrality_out.close()
print(degree_res)
print(closeness_res)
print(betweenness_res)