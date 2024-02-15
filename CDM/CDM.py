#######################################################################################
#INPUT: CDM(X, r);  d (≥ 2) by n (≥ 4) matrix X as X = (x1, ..., xn),
# where d is the dimension and n is the sample size.
# r in [2, min{d, n − 2}] : (the number of principal components to be computed).
# random: 'True' or 'False' (default: 'False')

#OUTPUT:
# values[j]; The estimator of the j-th eigenvalue by the CDM method. 
# vectors[:, j]; The estimator of the j-th PC direction by the CDM method.
# scores[:, j];  The estimator of the j-th PC scores for x_1,...,x_n by the CDM method.
#######################################################################################

import numpy as np
from scipy.linalg import svd
import random

def CDM(X,r,rand = "False"):
    d,n = X.shape
    n1 = int(np.ceil(n/2))
    n2 = n - n1
    q = min([n2-1,d,r])
    if (rand == "False"):
        index = np.arange(n)
    else:
        index = np.array(random.sample(list(np.arange(n)),n))
    index = list([index[:n1],index[n1:n]])
    Xcdm = [0] * 2
    for i in range(2):
        Xcdm[i] = (X[:,index[i]].T - X[:,index[i]].mean(axis = 1)).T
    Sd = Xcdm[0].T @ Xcdm[1]/np.sqrt((n1 - 1) * (n2 - 1))
    svdu,cdmval,svdv = svd(Sd)

    id = np.argsort(cdmval)[::-1]
    cdmval = (cdmval[id])[:q]
    svdu = (svdu[:,id])[:,:q]
    svdv = (svdv.T[:,id])[:,:q]
    for i in range(q):
        svdv[:,i] = np.sign(np.dot(Sd @ svdv[:,i],svdu[:,i])) * svdv[:,i]

    cdmvec = np.zeros((d,q))
    cdmscore = np.zeros((n,q))

    for s in range(q):
        hs = (Xcdm[0] @ svdu[:,s]/np.sqrt(n1 - 1) + Xcdm[1] @ svdv[:,s]/np.sqrt(n2 - 1))/(2 * np.sqrt(cdmval[s]))
        cdmvec[:,s] = hs/np.linalg.norm(hs)
        for i in range(n1):
            cdmscore[index[0][i],s] = svdu[i,s] * np.sqrt(n1 * cdmval[s])
        for j in range(n2):
            cdmscore[index[1][j],s] = svdv[j,s] * np.sqrt(n2 * cdmval[s])
    
    return(cdmval,cdmvec,cdmscore)