import networkx as nx
import networkx.algorithms.community as nx_comm
import matplotlib.pyplot as plt
G=nx.karate_club_graph()
B=nx_comm.louvain_communities(G, weight='weight', resolution=1, threshold=1e-07, seed=None)
A=[]
for i in range(0,G.number_of_nodes()):    
    A.append(0)
for i in range(0,len(B)):
    for j in(B[i]):
        A[j]=i
print(A)
colors=['r','b','g','y','purple','orange','black','gray','pink','beige','olive','magenta','violet','teal','navy','turquoise','gold','salmon','crimson']
for i in range(0,G.number_of_nodes()):
    nx.draw_networkx_nodes(G,nx.spring_layout(G,seed=7),nodelist=[i],node_color=colors[A[i]],node_size=100,alpha=0.3)
nx.draw_networkx_edges(G,nx.spring_layout(G,seed=7),G.edges())
plt.show()

 
