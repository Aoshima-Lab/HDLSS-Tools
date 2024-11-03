import numpy as np
from scipy.stats import t
from scipy.linalg import eigh

#######################################################################################
# INPUT: PC_OD(X, alpha); d by n matrix X as X = (x1, ..., xn),
# where d is the dimension and n is the sample size.
# alpha: Significance level of the test (0 < alpha < 0.5).

# OUTPUT: 
# outliers: The index of the outliers.
#######################################################################################

def PC_OD(X, alpha = 0.05):
    # Step2
    n_all = X.shape[1]
    samples  = np.arange(n_all)
    inliers = samples.copy()
    while True:
        n = len(inliers)
        X_cent = (X.T - X.mean(axis = 1)).T
        Sd = X_cent.T @ X_cent / (n - 1)
        dualvec = eigh(Sd, subset_by_index=[n - 1,n - 1])[1]
        # Step3
        t_value = t.ppf(alpha / (2 * n), n - 2)
        t0 = ((n - 1) / np.sqrt(n)) * np.sqrt(t_value**2 / (n - 2 + t_value**2))
        T_PC1 = np.max(np.abs(dualvec)) * np.sqrt(n - 1)
        #Step4
        if T_PC1 <= t0:
            break
        else:
            outlier = np.argmax(np.abs(dualvec))
            X = np.delete(X, outlier, axis=1)
            inliers = np.delete(inliers, outlier)
    outliers = np.setdiff1d(samples, inliers)
    return outliers