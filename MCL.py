import markov_clustering as mc
import networkx as nx
import matplotlib.pylab as plt
import networkx.algorithms.community as nx_comm
G=nx.karate_club_graph()
minimum_of_inflation=6
maximum_of_inflation=40
minimum_of_expansion=2
maximum_of_expansion=5
A=nx.adjacency_matrix(G)
inflation_of_highest_modularity=0
expansion_of_highest_modularity=0
highest_modularity=-100
for inflation in [i / 5 for i in range(minimum_of_inflation, maximum_of_inflation)]:
    for expansion in range(minimum_of_expansion,maximum_of_expansion):
        result = mc.run_mcl(A, inflation=inflation,expansion=expansion)
        clusters = mc.get_clusters(result)
        if(nx_comm.modularity(G,clusters,weight='weight')>highest_modularity):
            highest_modularity=nx_comm.modularity(G,clusters,weight='weight')
            inflation_of_highest_modularity=inflation
            expansion_of_highest_modularity=expansion
result = mc.run_mcl(A, inflation=inflation_of_highest_modularity,expansion=expansion_of_highest_modularity)
clusters = mc.get_clusters(result)
print(highest_modularity)
clusts=[]
for i in range(0,G.number_of_nodes()):    
    clusts.append(0)
for i in range(0,len(clusters)):
    for j in(clusters[i]):
        clusts[j]=i
colors=['r','b','g','y','purple','orange','black','gray','pink','beige','olive','magenta','violet','teal','navy','turquoise','gold','salmon','crimson']
for i in range(0,G.number_of_nodes()):
    nx.draw_networkx_nodes(G,nx.spring_layout(G,seed=7),nodelist=[i],node_color=colors[clusts[i]],node_size=100,alpha=0.3)
nx.draw_networkx_edges(G,nx.spring_layout(G,seed=7),G.edges())
plt.show()
