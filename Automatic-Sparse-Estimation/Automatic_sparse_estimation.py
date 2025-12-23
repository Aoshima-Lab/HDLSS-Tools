import numpy as np

def ECDM(X1, X2):
    """
    Compute the threshold (Tn) for sparse estimation via ECDM methodology.
    
    Parameters
    ----------
    X1 : ndarray
        p1 x n matrix (class 1)
    X2 : ndarray
        p2 x n matrix (class 2)
    
    Returns
    -------
    Tn : float
        Sparsification threshold for cross-covariance matrix
    """
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
    W = 0.0

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

    def q_corr(i, j):
        q1_component = np.dot(X1[:,i - 1] - M1[0][i + j - 3], X1[:,j - 1] - M2[0][i + j - 3])
        q2_component = np.dot(X2[:,i - 1] - M1[1][i + j - 3], X2[:,j - 1] - M2[1][i + j - 3])
        return q1_component * q2_component
    
    for i in range(1, n):
        for j in range(i + 1, n + 1):
            W += q_corr(i, j)
    Tn = W * u

    return Tn

def sparse_cross_cov(X1, X2):
    """
    Sparse estimation of the high-dimensional cross-covariance matrix.

    Parameters
    ----------
    X1 : ndarray
        p1 x n matrix (class 1)
    X2 : ndarray
        p2 x n matrix (class 2)

    Returns
    -------
    sparse_cross_cov : ndarray
        Sparse cross-covariance matrix (p1 x p2)
    sample_cross_cov : ndarray
        Sample cross-covariance matrix (p1 x p2)
    Delta : float
        Sparsification threshold from ECDM
    """
    p1, n = X1.shape
    p2 = X2.shape[0]
    p = p1 * p2
    Delta = ECDM(X1=X1, X2=X2)

    X1 = (X1.T - X1.mean(axis=1)).T
    X2 = (X2.T - X2.mean(axis=1)).T
    sample_cross_cov = X1 @ X2.T / (n - 1)
    s_ast = sample_cross_cov.reshape(-1, order='F')
    sparse_cross_cov = np.zeros(p)
    ord = np.argsort(np.abs(s_ast))[::-1]
    cri = 0
    for r in range(p):
        cri += s_ast[ord[r]]**2
        sparse_cross_cov[ord[r]] = s_ast[ord[r]]
        if cri >= Delta:
            break
    sparse_cross_cov = sparse_cross_cov.reshape(p1, p2, order='F')
    return sparse_cross_cov, sample_cross_cov, Delta

def sparse_mean(X1, X2=None):
    """
    Sparse mean vector estimation (one- or two-class).

    Parameters
    ----------
    X1 : ndarray
        p x n1 matrix
    X2 : ndarray or None
        Optional p x n2 matrix (class 2). If None, estimates sparse mean of X1; otherwise
        estimates sparse difference between class means.

    Returns
    -------
    sparse_mean : ndarray
        Sparse mean vector (or sparse mean difference) (p,)
    sample_mean : ndarray
        Sample mean vector (or mean difference) (p,)
    Delta : float
        Sparsification threshold
    """
    p = X1.shape[0]
    n1 = X1.shape[1]

    if X2 is None:
        sample_mean = X1.mean(axis=1)
        trS1 = np.sum((X1.T - sample_mean) ** 2) / (n1 - 1)
        Delta = np.sum(sample_mean ** 2) - trS1 / n1
    else:
        n2 = X2.shape[1]
        mean1 = X1.mean(axis=1)
        mean2 = X2.mean(axis=1)
        sample_mean = mean1 - mean2
        trS1 = np.sum((X1.T - mean1) ** 2) / (n1 - 1)
        trS2 = np.sum((X2.T - mean2) ** 2) / (n2 - 1)
        Delta = np.sum(sample_mean ** 2) - trS1 / n1 - trS2 / n2

    sort_idx = np.argsort(np.abs(sample_mean))[::-1]
    sparse_mean = np.zeros(p)
    cumulative_energy = 0.0

    for idx in range(p):
        element_idx = sort_idx[idx]
        cumulative_energy += sample_mean[element_idx] ** 2
        sparse_mean[element_idx] = sample_mean[element_idx]
        if cumulative_energy >= Delta:
            break

    return sparse_mean, sample_mean, Delta