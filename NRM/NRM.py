#######################################################################################
#INPUT: NRM(X, r);  d (≥ 2) by n (≥ 4) matrix X as X = (x1, ..., xn),
# where d is the dimension and n is the sample size.
# r in [2, min{d, n − 2}] : (the number of principal components to be computed).

#OUTPUT:
# values[j]; The estimator of the j-th eigenvalue by the NR method. 
# vectors[:, j]; The estimator of the j-th PC direction by the NR method.
# scores[:, j];  The estimator of the j-th PC scores for x_1,...,x_n by the NR method.
#######################################################################################

import numpy as np
from scipy.linalg import eigh

def NRM(X,r):
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
    vectors = np.zeros((d,q))
    scores = np.zeros((n,q))
    for i in range(q):
        values[i] = dualval[i] - (trSd - np.sum(dualval[0 : (i + 1)])) / (n - i - 2)
        vectors[:,i] = X @ dualvec[:,i] / np.sqrt((n - 1) * values[i])
        scores[:,i] = dualvec[:,i] * np.sqrt(n * values[i])
    return(values, vectors, scores)