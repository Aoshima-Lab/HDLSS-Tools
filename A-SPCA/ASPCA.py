import numpy as np
from scipy.linalg import eigh

#######################################################################################
# Python-code for A-SPCA.
#
# INPUT: ASPCA(X, r); d (≥ 2) by n (≥ 4) matrix X as X = (x1, ..., xn),
# where d is the dimension and n is the sample size.
# r in [2, min{d, n − 2}]; The number of principal components to be computed.

# OUTPUT:
# values[j]; The estimator of the j-th eigenvalue by A-SPCA (the NR method).
# vectors[, j]; The estimator of the j-th PC direction by A-SPCA.
# scores[, j];  The estimator of the j-th PC scores for the centroid data sets,
#   x_1-\bar{x}, ..., x_n-\bar{x}, by A-SPCA.
#######################################################################################

def ASPCA(X, r):
    d,n = X.shape
    q = min([n-2,d,r])
    X = (X.T - X.mean(axis = 1)).T
    Sd = X.T @ X / (n-1)
    trSd = np.trace(Sd)
    dualval, dualvec = eigh(Sd,subset_by_index=[n - q,n - 1])
    id = np.argsort(dualval)[::-1]
    dualval = dualval[id]
    dualvec = dualvec[:,id]
    values = np.zeros(q)
    nrmvec = np.zeros((d,q))
    vectors = np.zeros((d,q))
    scores = np.zeros((n,q))
    
    for i in range(q):
        values[i] = dualval[i] - (trSd - np.sum(dualval[0 : (i + 1)])) / (n - i - 2)
        nrmvec[:,i] = X @ dualvec[:,i] / np.sqrt((n - 1) * values[i])
        ord = np.argsort(np.abs(nrmvec[:,i]))[::-1]
        cri = 0
        for j in range(d):
            cri = cri + nrmvec[ord[j],i]**2
            vectors[ord[j],i] = nrmvec[ord[j],i]
            if cri >= 1:
                break
    scores = X.T @ vectors
    return(values, vectors, scores)

#######################################################################################
# Python-code for the shrinkage PC direction h_{j\omega} given by (5.2),
# the shrinkage PC scores given by (5.3) and k_{j\omega} given by (5.1) in Yata and Aoshima (2025).
#
# INPUT: SHPC(X, r, om = None); d (≥ 2) by n (≥ 4) matrix X as X = (x1, ..., xn),
# where d is the dimension and n is the sample size.
# r in [2, min{d, n − 2}]; The number of principal components to be computed.
# om; The vector of shrinkage parameters, (\omega_1 ,..., \omega_r),
#     where \omega_j in (0, 1] for j=1, ..., r. (default: om = np.ones(q))

# OUTPUT:
# vectors[, j]; The estimator of the j-th shrinkage PC direction by A-SPCA.
# k[j]; The estimator of the k_{j\omega} given by (5.1) in Yata and Aoshima (2025).
# scores[, j];  The estimator of the j-th shrinkage PC scores for the centroid data sets,
#  x_1-\bar{x}, ..., x_n-\bar{x}.
#######################################################################################

def SHPC(X, r, om = None):
    d,n = X.shape
    q = min([n-2,d,r])
    om = np.concatenate([om, np.ones(q - len(om))]) if om is not None else np.ones(q)
    X = (X.T - X.mean(axis = 1)).T
    Sd = X.T @ X / (n-1)
    trSd = np.trace(Sd)
    dualval, dualvec = eigh(Sd,subset_by_index=[n - q,n - 1])
    id = np.argsort(dualval)[::-1]
    dualval = dualval[id]
    dualvec = dualvec[:,id]
    nrmval = np.zeros(q)
    nrmvec = np.zeros((d,q))
    vectors = np.zeros((d,q))
    scores = np.zeros((n,q))
    k = np.zeros(q)
    
    for i in range(q):
        nrmval[i] = dualval[i] - (trSd - np.sum(dualval[0 : (i + 1)])) / (n - i - 2)
        nrmvec[:,i] = X @ dualvec[:,i] / np.sqrt((n - 1) * nrmval[i])
        ord = np.argsort(np.abs(nrmvec[:,i]))[::-1]
        cri = 0
        for j in range(d):
            cri = cri + nrmvec[ord[j],i]**2
            vectors[ord[j],i] = nrmvec[ord[j],i]
            if cri >= om[i]:
                k[i] = j+1
                break
    scores = X.T @ vectors
    return(vectors, scores, k)