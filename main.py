import networkx as nx
import networkx.algorithms.community as nx_comm
import matplotlib.pyplot as plt
import igraph as ig
import leidenalg as la
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import SpectralClustering
from sklearn.cluster import DBSCAN
from sklearn.cluster import MeanShift
import markov_clustering as mc
def louvain(G):
    B=nx_comm.louvain_communities(G, weight='weight', resolution=1, threshold=1e-07, seed=None)
    A=[]
    for i in range(0,G.number_of_nodes()):    
        A.append(0)
    for i in range(0,len(B)):
        for j in(B[i]):
            A[j]=i
    clusters=[]
    for k in range(G.number_of_nodes()):
        cluster=[]
        clusters.append(cluster)
    for k in range(G.number_of_nodes()):
        clusters[A[k]].append(k)
    clusters=[cluster for cluster in clusters if(cluster!=[])]
    modularity=nx_comm.modularity(G,clusters,weight='weight')
    return({"clusters":A,"modularity":modularity})
def leiden(G):
    g=ig.Graph.from_networkx(G)
    B = la.find_partition(g, la.ModularityVertexPartition)
    A=[]
    for i in range(0,G.number_of_nodes()):    
        A.append(0)
    for i in range(0,len(B)):
        for j in(B[i]):
            A[j]=i
    clusters=[]
    for k in range(G.number_of_nodes()):
        cluster=[]
        clusters.append(cluster)
    for k in range(G.number_of_nodes()):
        clusters[A[k]].append(k)
    clusters=[cluster for cluster in clusters if(cluster!=[])]
    modularity=nx_comm.modularity(G,clusters,weight='weight')
    return({"clusters":A,"modularity":modularity})
def hirarchical(G,minimum_of_clusters,maximum_of_clusters):
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
    return({"clusters":sc.labels_,"modularity":Q_highest_modularity})
def spectral_clustering(G,minimum_number_of_clusters,maximum_number_of_clusters):
    Q_highest_modularity=0
    k_highest_modularity=0
    A=nx.adjacency_matrix(G)
    for k in range(minimum_number_of_clusters,maximum_number_of_clusters):
        sc=SpectralClustering(k,affinity='precomputed',n_init=100)
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
    sc=SpectralClustering(k_highest_modularity,affinity='precomputed',n_init=100)
    sc.fit(A)
    return({"clusters":sc.labels_,"modularity":Q_highest_modularity})
def walk_trap(G,minimum_of_steps,maximum_of_steps):
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
    clusters=[]
    for i in range(0,G.number_of_nodes()):    
        clusters.append(0)
    for i in range(0,len(clust)):
        for j in(clust[i]):
            clusters[j]=i
    return({"clusters":clusters,"modularity":maximum_modularity})
def mcl(G,minimum_of_inflation,maximum_of_inflation,minimum_of_expansion,maximum_of_expansion):
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
    clusts=[]
    for i in range(0,G.number_of_nodes()):    
        clusts.append(0)
    for i in range(0,len(clusters)):
        for j in(clusters[i]):
            clusts[j]=i
    return({"clusters":clusts,"modularity":highest_modularity})
def dbscan(G,minimum_eps,maximum_eps,minimum_min_samples,maximum_min_samples):
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
    return({"clusters":db.labels_,"modularity":Q_highest_modularity})
def mean_shift(G,minimum_bandwidth,maximum_bandwidth):
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
    return({"clusters":ms.labels_,"modularity":Q_highest_modularity})
G=nx.karate_club_graph()
number_of_algorithems=8
clusters=[]
modularities=[]
print('1.Louvain')
clustering_list=louvain(G)
modularities.append(clustering_list["modularity"])
print(clustering_list["modularity"])
clusters.append(clustering_list["clusters"])
print('2.Leiden')
clustering_list=leiden(G)
modularities.append(clustering_list["modularity"])
print(clustering_list["modularity"])
clusters.append(clustering_list["clusters"])
print('3.Hirarchical')
x=2
while(x!=1):
    a=int(input('Enter the minimum number of clusters : '))
    b=int(input('Enter the maximum number of clusters : '))
    clustering_list=hirarchical(G,a,b)
    modularities.append(clustering_list["modularity"])
    print(clustering_list["modularity"])
    clusters.append(list(clustering_list["clusters"]))
    print("Next algorithm?")
    print("1.Yes")
    print("2.No")
    x=int(input())
x=2
print('4.Spectral clustering')
while(x!=1):
    a=int(input('Enter the minimum number of clusters : '))
    b=int(input('Enter the maximum number of clusters : '))
    clustering_list=spectral_clustering(G,a,b)
    modularities.append(clustering_list["modularity"])
    print(clustering_list["modularity"])
    clusters.append(list(clustering_list["clusters"]))
    print("Next algorithm?")
    print("1.Yes")
    print("2.No")
    x=int(input())
x=2
print('5.Walk trap')
while(x!=1):
    a=int(input('Enter the minimum number of steps : '))
    b=int(input('Enter the maximum number of steps : '))
    clustering_list=walk_trap(G,a,b)
    modularities.append(clustering_list["modularity"])
    print(clustering_list["modularity"])
    clusters.append(clustering_list["clusters"])
    print("Next algorithm?")
    print("1.Yes")
    print("2.No")
    x=int(input())
x=2
print('6.MCL')
while(x!=1):
    a=int(input('Enter the minimum of inflation : '))
    b=int(input('Enter the maximum of inflation : '))
    c=int(input('Enter the minimum of expansion : '))
    d=int(input('Enter the maximum of expansion : '))
    clustering_list=mcl(G,a,b,c,d)
    modularities.append(clustering_list["modularity"])
    print(clustering_list["modularity"])
    clusters.append(clustering_list["clusters"])
    print("Next algorithm?")
    print("1.Yes")
    print("2.No")
    x=int(input())
x=2
print('7.DBSCAN')
while(x!=1):
    a=int(input('Enter the minimum of epsilon : '))
    b=int(input('Enter the maximum of epsilon : '))
    c=int(input('Enter the minimum number of min_samples : '))
    d=int(input('Enter the maximum number of min_samples : '))
    clustering_list=dbscan(G,a,b,c,d)
    modularities.append(clustering_list["modularity"])
    print(clustering_list["modularity"])
    clusters.append(list(clustering_list["clusters"]))
    print("Next algorithm?")
    print("1.Yes")
    print("2.No")
    x=int(input())
x=2
print('8.Mean shift')
while(x!=1):
    a=int(input('Enter the minimum of bandwidth : '))
    b=int(input('Enter the maximum of bandwidth : '))
    clustering_list=mean_shift(G,a,b)
    modularities.append(clustering_list["modularity"])
    print(clustering_list["modularity"])
    clusters.append(list(clustering_list["clusters"]))
    print("Output?")
    print("1.Yes")
    print("2.No")
    x=int(input())
y=float(input("Threshold="))
number_of_algorithems=8
final_clusters=[]
for j in range(0,G.number_of_nodes()):
    final_clusters.append([])
    for k in range(0,G.number_of_nodes()):
        x=0
        for i in range(0,number_of_algorithems):
            if((k!=j) and (clusters[i][j]==clusters[i][k])):
                x=x+modularities[i]
        if(x>y):
            final_clusters[j].append(k)         
print(final_clusters)