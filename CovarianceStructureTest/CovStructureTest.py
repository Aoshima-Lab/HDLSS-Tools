import numpy as np
from scipy.stats import norm


def Y(X):
    """
    Basic computation function for covariance matrix estimation via ECDM.
    
    Parameters
    ----------
    X : ndarray
        p x n matrix (p: dimension, n: sample size)
    
    Returns
    -------
    dict
        Y1: p x n_pairs matrix
        Y2: p x n_pairs matrix
        indices: (i,j) pair indices (n_pairs x 2)
    """
    if len(X.shape) == 1:
        n = X.shape[0]
        X = X.reshape(1, n)
    else:
        p = X.shape[0]
        n = X.shape[1]
    
    p = X.shape[0]
    n = X.shape[1]
    
    n1 = int(np.ceil(n / 2))
    n2 = n - n1
    u1 = n1 / (n1 - 1)
    u2 = n2 / (n2 - 1)
    
    S = np.arange(3, 2 * n)
    L = len(S)
    X_var = np.zeros((2, L, p))
    
    for l in range(L):
        dv = int(np.floor(S[l] / 2))
        
        if dv >= n1:
            V1_idx = np.arange(dv - n1, dv).astype(int)
        else:
            V1_idx = np.concatenate([np.arange(dv), np.arange(dv + n2, n)]).astype(int)
        
        if dv <= n1:
            V2_idx = np.arange(dv, dv + n2).astype(int)
        else:
            V2_idx = np.concatenate([np.arange(dv - n1), np.arange(dv, n)]).astype(int)
        
        X_var[0, l, :] = X[:, V1_idx].mean(axis=1)
        X_var[1, l, :] = X[:, V2_idx].mean(axis=1)
    
    lower_idx = np.column_stack(np.triu_indices(n, k=1))
    n_pairs = lower_idx.shape[0]
    Y1_matrix = np.zeros((p, n_pairs))
    Y2_matrix = np.zeros((p, n_pairs))
    
    for k in range(n_pairs):
        i, j = lower_idx[k]
        Y1_matrix[:, k] = np.sqrt(u1) * (X[:, i] - X_var[0, (i + j - 1), :])
        Y2_matrix[:, k] = np.sqrt(u2) * (X[:, j] - X_var[1, (i + j - 1), :])
    
    return {
        'Y1': Y1_matrix,
        'Y2': Y2_matrix,
        'indices': lower_idx
    }


def T_scaled_identity(X):
    """
    Test statistic under scaled identity covariance assumption.
    
    Parameters
    ----------
    X : ndarray
        p x n matrix
    
    Returns
    -------
    dict
        TestStatistics: test statistic value
        pvalue: asymptotic p-value
    """
    p,n = X.shape
    Y_list = Y(X)
    W_n = 2 * np.sum(np.sum(Y_list['Y1'] * Y_list['Y2'], axis=0) ** 2) / (n * (n - 1))

    U_nS = 2 * np.sum(np.sum(Y_list['Y1'] ** 2, axis=0) * np.sum(Y_list['Y2'] ** 2, axis=0)) / (p * n * (n - 1))

    test = n * W_n / (2 * U_nS) - n / 2
    p_value = 1 - norm.cdf(test)
    
    return {'TestStatistics': test, 'pvalue': p_value}


def T_diagonal(X):
    """
    Test statistic under diagonal covariance assumption.
    
    Parameters
    ----------
    X : ndarray
        p x n matrix
    
    Returns
    -------
    dict
        TestStatistics: test statistic value
        pvalue: asymptotic p-value
    """
    n = X.shape[1]
    Y_list = Y(X)
    W_n = 2 * np.sum(np.sum(Y_list['Y1'] * Y_list['Y2'], axis=0) ** 2) / (n * (n - 1))

    U_nD = 2 * np.sum(Y_list['Y1'] ** 2 * Y_list['Y2'] ** 2) / (n * (n - 1))
    Psi_nD = U_nD ** 2 - np.sum((2 * np.sum(Y_list['Y1'] ** 2 * Y_list['Y2'] ** 2, axis=1) / (n * (n - 1)))**2)
    Delta_n = W_n - U_nD
    
    test = n * Delta_n / (2 * np.sqrt(Psi_nD))
    p_value = 1 - norm.cdf(test)
    
    return {'TestStatistics': test, 'pvalue': p_value}


def T_intraclass(X):
    """
    Test statistic under intraclass covariance assumption.
    
    Parameters
    ----------
    X : ndarray
        p x n matrix
    
    Returns
    -------
    dict
        TestStatistics: test statistic value
        pvalue: asymptotic p-value
    """
    p,n = X.shape
    Y_list = Y(X)
    W_n = 2 * np.sum(np.sum(Y_list['Y1'] * Y_list['Y2'], axis=0) ** 2) / (n * (n - 1))
    
    Y1_norm = np.sum(Y_list['Y1'] ** 2, axis=0)
    Y2_norm = np.sum(Y_list['Y2'] ** 2, axis=0)
    Y1_one = np.sum(Y_list['Y1'], axis=0) ** 2
    Y2_one = np.sum(Y_list['Y2'], axis=0) ** 2
    
    U_nIC = 2 * np.sum(Y1_one * Y2_one) / (p ** 2 * n * (n - 1)) + 2 * np.sum((Y1_norm - Y1_one / p) * (Y2_norm - Y2_one / p)) / ((p - 1) * n * (n - 1))
    Psi_nIC = U_nIC ** 2 - (2 * np.sum(Y1_one * Y2_one) / (p ** 2 * n * (n - 1))) ** 2
    Delta_nIC = W_n - U_nIC
    
    test = n * Delta_nIC / (2 * np.sqrt(Psi_nIC))
    p_value = 1 - norm.cdf(test)
    
    return {'TestStatistics': test, 'pvalue': p_value}
