import numpy as np

def random_graph(n,p):
    # returns nxn adj martix W for a graph by method called Erdős-Rényi model
    # the parameter p is the probability of an edge existing between any two nodes
    W=np.zeros((n,n))
    for i in range(n):
        for j in range(i+1,n):
            if np.random.binomial(1,p)==1:
                W[i,j]=1
                W[j,i]=1     
    return W    

def block_model(c,p,q):
    # this is variant of "random graph" where there is more then one probability.
    # c is category vector, indicating to which category that the node belong to
    # p is the probability of an edge existing between two nodes with the same category
    # q is the probability of an edge existing between two nodes with different category
    # returns W - nxn adj martix for the graph
    n=len(c)
    W=np.zeros((n,n))
    for i in range(n):
        for j in range(i+1,n):
            if c[i]==c[j]:
                prob=p
            else:
                prob=q
            if np.random.binomial(1,prob)==1:
                W[i,j]=1
                W[j,i]=1     
    return W

def balanced_block_model(nb_of_clust, clust_size , p, q):
    # nb_of_clust is the number of categories you want in the model.
    # cluster_size is the number of nodes belonging to each category
    # p is the probability of an edge existing between two nodes with the same category
    # q is the probability of an edge existing between two nodes with different category
    # returns W - nxn adj martix for the graph
    # returns c - vector of the nodes categories len - nb_of_clust*cluster size (number of total nodes)
    n = nb_of_clust*clust_size
    c=np.zeros(n)
    for r in range(nb_of_clust):
        start=r*clust_size
        c[start:start+clust_size]=r
    W=block_model(c,p,q)
    return W,c


def unbalanced_block_model(nb_of_clust, clust_size_min, clust_size_max, p, q): 
    # an unbalanced version of "balanced_block_model" that has different cluster sizes (randomly choosen by bounds)
    # the output is the same as "balanced_block_model"
    c = []
    for r in range(nb_of_clust):
        if clust_size_max==clust_size_min:
            clust_size_r = clust_size_max
        else:
            clust_size_r = np.random.randint(clust_size_min,clust_size_max,size=1)[0]
        val_r = np.repeat(r,clust_size_r,axis=0)
        c.append(val_r)
    c = np.concatenate(c)  
    W = block_model(c,p,q)  
    return W,c

  
def add_a_block(W0,W,c,nb_of_clust,q):
    # Connects the two matrices in the following block manner:
    #  :W: V.T:
    #  :V: W0 :
    # q is the probability of an edge existing between two nodes of the two graphs. if q=0 -> total block
    n=W.shape[0]
    n0=W0.shape[0]
    V=(np.random.rand(n0,n) < q).astype(float)
    W_up=np.concatenate(  ( W , V.T ) , axis=1 )
    W_low=np.concatenate( ( V , W0  ) , axis=1 )
    W_new=np.concatenate( (W_up,W_low)  , axis=0)
    c0=np.full(n0,nb_of_clust)
    c_new=np.concatenate( (c, c0),axis=0)
    return W_new,c_new

def schuffle(W,c):
    # relabel the vertices at random
    idx=np.random.permutation( W.shape[0] )
    W_new=W[idx,:]
    W_new=W_new[:,idx]
    c_new=c[idx]
    return W_new , c_new , idx 











