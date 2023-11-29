import igraph as ig
import leidenalg as la
G = ig.Graph.Famous('Zachary')
partition = la.find_partition(G, la.ModularityVertexPartition)
print(partition)