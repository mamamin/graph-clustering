import igraph as ig
import networkx as nx
import matplotlib.pyplot as plt
G=nx.karate_club_graph()
maximum_of_steps=10
minimum_of_steps=3
g=ig.Graph.from_networkx(G)
k_with_maximum_modularity=0
maximum_modularity=0
for k in range(minimum_of_steps,maximum_of_steps):
    wtrap = g.community_walktrap(weights=g.es['weight'],steps = k)
    clust = wtrap.as_clustering()
    if( g.modularity(membership=clust,weights=g.es['weight'])>maximum_modularity):
        k_with_maximum_modularity=k
        maximum_modularity=g.modularity(membership=clust,weights=g.es['weight'])
wtrap = g.community_walktrap(weights=g.es['weight'],steps = k_with_maximum_modularity)
clust = wtrap.as_clustering()
colors=['r','b','g','y','purple','orange','black','gray','pink','beige','olive','magenta','violet','teal','navy','turquoise','gold','salmon','crimson']
for i in range(0,len(clust)):
    nx.draw_networkx_nodes(G,nx.spring_layout(G,seed=7),nodelist=clust[i],node_color=colors[i],node_size=100,alpha=0.3)
nx.draw_networkx_edges(G,nx.spring_layout(G,seed=7),G.edges())
plt.show()