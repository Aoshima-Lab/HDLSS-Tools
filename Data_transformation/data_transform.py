import numpy as np

def check_sse(X, centering=False, random=False, seed=None):
    """
    Estimation of the number of strongly spiked eigenvalues of the covariance matrix

    Parameters
    ----------
    X : ndarray, shape (d, n)
        Data matrix (features x samples)
    centering : bool, default False
        If True, center the data before splitting
    random : bool, default False
        If True, randomly split samples; if False, split deterministically.
    seed : int or None
        Random seed for reproducibility (used if random=True)

    Returns
    -------
    khat : int
        Estimated number of spiked eigenvalues
    """
    if centering:
        X = X - X.mean(axis=1, keepdims=True)
    d, n = X.shape
    n1 = int(np.ceil(n / 2))
    n2 = n - n1
    q = min(n2 - 1, d)
    if not random:
        X1 = X[:, :n1]
        X2 = X[:, n1:]
    else:
        rng = np.random.default_rng(seed)
        idx = rng.permutation(n)
        X1 = X[:, idx[:n1]]
        X2 = X[:, idx[n1:]]
    # Center each split after splitting (same as R)
    X1 = X1 - X1.mean(axis=1, keepdims=True)
    X2 = X2 - X2.mean(axis=1, keepdims=True)
    Sd = X1.T @ X2 @ X2.T @ X1 / ((n1 - 1) * (n2 - 1))
    cdmval = np.linalg.svd(Sd, compute_uv=False)[:q]
    kappa = np.sqrt(np.log(n) / n)
    khat = q
    psi = np.trace(Sd)
    tau_hat = 1 - cdmval[0] / psi
    condition = tau_hat * (1 + kappa)
    for l in range(1, q):
        if condition > 1:
            khat = l - 1
            break
        psi -= cdmval[l - 1]
        tau_hat = 1 - cdmval[l] / psi
        condition = tau_hat * (1 + (l + 1) * kappa)
    khat = min(khat, n2 - 2)
    return khat

def NRM_trans(X, centering=False, sse_point=None, random=False, seed=None):
    """
    Data transformation based on the noise-reduction methodology

    Parameters
    ----------
    X : ndarray, shape (d, n)
        Data matrix (features x samples)
    centering : bool, default False
        If True, center the data before further processing
    sse_point : int or None
        Number of spiked eigenvalues; if None, estimated by check_sse
    random : bool, default False
        If True, randomly split samples for sse estimation
    seed : int or None
        Random seed for reproducibility

    Returns
    -------
    dict with keys:
        'X_trans' : ndarray, shape (sse_point, n)
            Transformed data
        'nrmvec' : ndarray, shape (d, sse_point)
            NRM basis vectors
    """
    if centering:
        X = X - X.mean(axis=1, keepdims=True)
    d, n = X.shape
    sse_point = check_sse(X, centering=centering, random=random, seed=seed) if sse_point is None else sse_point
    # Calculate sample eigenvalues and dual-eigenvectors
    X0 = X if centering else X - X.mean(axis=1, keepdims=True)
    eigvals, dualvecs = np.linalg.eigh(X0.T @ X0 / (n - 1))
    idx = np.argsort(eigvals)[::-1]
    eigvals = eigvals[idx][:sse_point]
    dualvecs = dualvecs[:, idx][:, :sse_point]
    #Noise-reduced eigenvalues and eigenvectors
    trSd = np.sum(X0**2) / (n - 1)
    cs = np.cumsum(eigvals)
    denom = n - (np.arange(sse_point) + 2)
    nrmval = eigvals - (trSd - cs) / denom
    nrmvec = (X0 @ dualvecs) / (np.sqrt(nrmval)[None, :] * np.sqrt(n - 1))
    #NRM transformation
    c = np.sqrt(n - 1) / (n - 2)
    nr_projection_term = np.sqrt(n - 1) * (nrmvec.T @ X)
    #Calculate bias correction term
    dualvec_scaled = dualvecs / np.sqrt(nrmval)[None, :]
    x0_dot_x = np.sum(X0 * X, axis=0)
    bias_correction_term = (n / (n - 1)) * (dualvec_scaled.T * x0_dot_x[None, :])
    # Final transformed data
    X_trans = c * (nr_projection_term - bias_correction_term)
    return {'X_trans': X_trans, 'nrmvec': nrmvec}