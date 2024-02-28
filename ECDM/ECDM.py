############################################################################################
## Estimation of tr(\Sigma^2) by the ECDM methodology.
##
## INPUT: 
##       W(X); p by n matrix X as X=(x_{1},...,x_{n}), 
##       where n (≧ 4) is the sample size and p (≧ 1) is the dimension.
##
## OUTPUT: 
##       Wn: The estimator of \tr(\Sigma^2) by the ECDM methodology.
############################################################################################

import numpy as np
from scipy.stats import norm

def W(X):
    if len(X.shape) == 1:
        n = X.shape[0]
        X = X.reshape(1,n)
    else:
        n = X.shape[1]
    n1 = int(np.ceil(n/2))
    n2 = n - n1
    u = 2 * n1 * n2 / ((n1 - 1) * (n2 - 1) * n * (n - 1))
    W = 0

    def H1(k):
        if np.floor(k/2) >= n1:
            index = np.arange(np.floor(k/2) - n1, np.floor(k/2)).astype(int)
        else:
            index = np.concatenate([np.arange(np.floor(k/2)), np.arange(np.floor(k/2) + n2, n)]).astype(int)
        return(X[:,index].mean(axis = 1))

    def H2(k):
        if np.floor(k/2) <= n1:
            index = np.arange(np.floor(k/2), np.floor(k/2) + n2).astype(int)
        else:
            index = np.concatenate([np.arange(np.floor(k/2) - n1), np.arange(np.floor(k/2), n)]).astype(int)
        return(X[:,index].mean(axis = 1))

    S = np.arange(3, 2 * n)
    M1 = list(map(H1, S))
    M2 = list(map(H2, S))
    
    def q(i,j):
        return(np.dot(X[:,i - 1] - M1[i + j - 3], X[:,j - 1] - M2[i + j - 3])**2)

    for i in range(1, n):
        for j in range(i + 1, n + 1):
            W += q(i,j)
    W *= u
    return(W)


#####################################################################################################################
## The test of high-dimensional correlations by (5) in Yata and Aoshima (2016). 
##
## INPUT:    
##       Tecdm(X1,X2); p_1 by n matrix X1 and p_2 by n matrix X2 as X1=(x_{11},...,x_{1n}) and X2=(x_{21},...,x_{2n}), 
##                     where n (≧ 4) is the sample size and p_i (≧ 1) is the dimension of Xi.
##
##
## OUTPUT: 
##        TestStatistics: The test statistic value for (5) (\hat{T}_n/\hat{\delta}).
##        pvalue: The asymptotic p-value for testing (1) by (5) 
##                (1-\Phi(\hat{T}_n/\hat{\delta}), where \Phi(x) is the c.d.f. of N(0,1)).
##        Tn: The estimator of \Delta (\hat{T}_n).
##        delta: The estimator of the standard deviation for \hat{T}_n. 
#####################################################################################################################

def Tecdm(X1,X2):
    if len(X1.shape) == 1:
        n = X1.shape[0]
        X1 = X1.reshape(1,n)
    else:
        n = X1.shape[1]
    if len(X2.shape) == 1:
        X2 = X2.reshape(1,n)

    n1 = int(np.ceil(n/2))
    n2 = n - n1
    u = 2 * n1 * n2 / ((n1 - 1) * (n2 - 1) * n * (n - 1))
    W = np.zeros(3)

    def V1(k, X):
        if np.floor(k/2) >= n1:
            index = np.arange(np.floor(k/2) - n1, np.floor(k/2)).astype(int)
        else:
            index = np.concatenate([np.arange(np.floor(k/2)), np.arange(np.floor(k/2) + n2, n)]).astype(int)
        return(X[:,index])
    def V2(k, X):
        if np.floor(k/2) <= n1:
            index = np.arange(np.floor(k/2), np.floor(k/2) + n2).astype(int)
        else:
            index = np.concatenate([np.arange(np.floor(k/2) - n1), np.arange(np.floor(k/2), n)]).astype(int)
        return(X[:,index])

    def H1_1(k):
        return(V1(k,X1).mean(axis = 1))
    def H2_1(k):
        return(V2(k,X1).mean(axis = 1))
    def H1_2(k):
        return(V1(k,X2).mean(axis = 1))
    def H2_2(k):
        return(V2(k,X2).mean(axis = 1))
    
    S = np.arange(3, 2 * n)
    M1 = [list(map(H1_1, S)), list(map(H1_2, S))]
    M2 = [list(map(H2_1, S)), list(map(H2_2, S))]

    def q(i,j):
        q1 = np.dot(X1[:,i - 1] - M1[0][i + j - 3], X1[:,j - 1] - M2[0][i + j - 3])**2
        q2 = np.dot(X2[:,i - 1] - M1[1][i + j - 3], X2[:,j - 1] - M2[1][i + j - 3])**2
        q_corr = np.dot(X1[:,i - 1] - M1[0][i + j - 3], X1[:,j - 1] - M2[0][i + j - 3]) * np.dot(X2[:,i - 1] - M1[1][i + j - 3], X2[:,j - 1] - M2[1][i + j - 3])
        return(np.array([q1, q2, q_corr]))
    
    for i in range(1, n):
        for j in range(i + 1, n + 1):
            W += q(i,j)
    W *= u
    
    delta = np.sqrt(2 * W[0] * W[1] / n**2)
    Tn = W[2]
    TestStatistics = Tn / delta
    pvalue = 1 - norm.cdf(TestStatistics)

    return(TestStatistics, pvalue, Tn, delta)