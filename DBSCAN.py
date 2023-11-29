import networkx as nx
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
import networkx.algorithms.community as nx_comm
G=nx.karate_club_graph()
minimum_eps=3
maximum_eps=20
minimum_min_samples=3
maximum_min_samples=10
A=nx.adjacency_matrix(G)
A=A.toarray()
eps_of_highest_modularity=0;
min_samples_highest_modularity=0;
Q_highest_modularity=0;
for i in range(G.number_of_nodes()):
    A[i][i]=A.max()
for i in range(minimum_eps,maximum_eps):
    for j in range(minimum_min_samples,maximum_min_samples):
        db=DBSCAN(eps=i,min_samples=j).fit(A)
        clusters=[]
        for k in range(G.number_of_nodes()):
            cluster=[]
            clusters.append(cluster)
        for k in range(G.number_of_nodes()):
            clusters[db.labels_[k]].append(k)
        clusters=[cluster for cluster in clusters if(cluster!=[])]
        if(nx_comm.modularity(G,clusters,weight='weight')>Q_highest_modularity):
           eps_of_highest_modularity=i
           min_samples_highest_modularity=j
           Q_highest_modularity=nx_comm.modularity(G,clusters,weight='weight')
db=DBSCAN(eps=eps_of_highest_modularity,min_samples=min_samples_highest_modularity).fit(A) 
colors=['r','b','g','y','purple','orange','black','gray','pink','beige','olive','magenta','violet','teal','navy','turquoise','gold','salmon','crimson']
for i in range(0,G.number_of_nodes()):
    nx.draw_networkx_nodes(G,nx.spring_layout(G,seed=7),nodelist=[i],node_color=colors[db.labels_[i]],node_size=100,alpha=0.3)
nx.draw_networkx_edges(G,nx.spring_layout(G,seed=7),G.edges())
print(db.labels_)
print(Q_highest_modularity)
plt.show()