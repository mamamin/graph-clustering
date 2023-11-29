from sklearn.cluster import AgglomerativeClustering
import matplotlib.pylab as plt
import networkx.algorithms.community as nx_comm
import networkx as nx
G=nx.karate_club_graph()
maximum_of_clusters=10
minimum_of_clusters=3
A=nx.adjacency_matrix(G)
A=A.toarray()
for i in range(0,G.number_of_nodes()):
    A[i][i]=A.max()
Q_highest_modularity=0;
k_highest_modularity=0;
for k in range(minimum_of_clusters,maximum_of_clusters):
    sc=AgglomerativeClustering(linkage='average',n_clusters=k,distance_threshold=None)
    sc.fit(A)
    clusters=[]
    for i in range(G.number_of_nodes()):
        cluster=[]
        clusters.append(cluster)
    for i in range(G.number_of_nodes()):
        clusters[sc.labels_[i]].append(i)
    clusters=[cluster for cluster in clusters if(cluster!=[])]
    if(nx_comm.modularity(G,clusters,weight='weight')>Q_highest_modularity):
           Q_highest_modularity=nx_comm.modularity(G,clusters,weight='weight')
           k_highest_modularity=k
sc=AgglomerativeClustering(linkage='average',n_clusters=k_highest_modularity,distance_threshold=None)
sc.fit(A)
print(Q_highest_modularity)
print(k_highest_modularity)
print(sc.labels_)
colors=['r','b','g','y','purple','orange','black','gray','pink','beige','olive','magenta','violet','teal','navy','turquoise','gold','salmon','crimson']
for i in range(0,G.number_of_nodes()):
    nx.draw_networkx_nodes(G,nx.spring_layout(G,seed=7),nodelist=[i],node_color=colors[sc.labels_[i]],node_size=100,alpha=0.3)
nx.draw_networkx_edges(G,nx.spring_layout(G,seed=7),G.edges())
plt.show()
