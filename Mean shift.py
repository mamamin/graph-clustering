from sklearn.cluster import MeanShift
import matplotlib.pyplot as plt
import networkx as nx
import networkx.algorithms.community as nx_comm
G=nx.karate_club_graph()
minimum_bandwidth=80;
maximum_bandwidth=120;
A=nx.adjacency_matrix(G)
A=A.toarray()
bandwidth_of_highest_modularity=0
Q_highest_modularity=0;
for i in range(G.number_of_nodes()):
    A[i][i]=A.max()
for i in range(minimum_bandwidth,maximum_bandwidth):
    ms=MeanShift(bandwidth=i/10)
    ms.fit(A)
    clusters=[]
    for k in range(G.number_of_nodes()):
        cluster=[]
        clusters.append(cluster)
    for k in range(G.number_of_nodes()):
        clusters[ms.labels_[k]].append(k)
    clusters=[cluster for cluster in clusters if(cluster!=[])]
    if(nx_comm.modularity(G,clusters,weight='weight')>Q_highest_modularity):
           bandwidth_of_highest_modularity=i/10
           Q_highest_modularity=nx_comm.modularity(G,clusters,weight='weight')
ms=MeanShift(bandwidth=bandwidth_of_highest_modularity)
ms.fit(A)
colors=['r','b','g','y','purple','orange','black','gray','pink','beige','olive','magenta','violet','teal','navy','turquoise','gold','salmon','crimson']
for i in range(0,G.number_of_nodes()):
    nx.draw_networkx_nodes(G,nx.spring_layout(G,seed=7),nodelist=[i],node_color=colors[ms.labels_[i]],node_size=100,alpha=0.3)
nx.draw_networkx_edges(G,nx.spring_layout(G,seed=7),G.edges())
print(ms.labels_)
print(Q_highest_modularity)
print(bandwidth_of_highest_modularity)
plt.show()