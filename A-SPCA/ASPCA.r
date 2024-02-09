#######################################################################################
# R-code for A-SPCA.
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

ASPCA <- function(X, r) {
    d <- dim(X)[1]
    n <- dim(X)[2]
    q <- min(n - 2, d, r)
    X <- sweep(X, 1, apply(X, 1, mean), "-")
    X0 <- X
    svd0 <- svd(X0 / (n - 1)^(1 / 2), nu = q, nv = q)
    sval <- svd0$d[1:q]
    svec <- svd0$v[, 1:q]
    trSd <- norm(X0, "F")^2 / (n - 1)
    nrmval <- numeric(q)
    nrmvec <- matrix(0, d, q)
    aspca <- matrix(0, d, q)
    asscore <- matrix(0, n, q)

    for (i in 1:q) {
        nrmval[i] <- sval[i]^2 - (trSd - sum(sval[1:i]^2)) / (n - i - 1)
        nrmvec[, i] <- X %*% svec[, i] / sqrt((n - 1) * nrmval[i])
        ord <- order(abs(nrmvec[, i]), decreasing = T)
        cri <- 0
        for (j in 1:d) {
            cri <- cri + nrmvec[ord[j], i]^2
            aspca[ord[j], i] <- nrmvec[ord[j], i]
            if (cri >= 1) {
                break
            }
        }
    }
    asscore <- t(X0) %*% aspca
    return(list(values = nrmval, vectors = aspca, scores = asscore))
}

#######################################################################################
# R-code for the shrinkage PC direction h_{j\omega} given by (5.2),
# the shrinkage PC scores given by (5.3) and k_{j\omega} given by (5.1) in Yata and Aoshima (2025).
#
# INPUT: SHPC(X, r, om = NULL); d (≥ 2) by n (≥ 4) matrix X as X = (x1, ..., xn),
# where d is the dimension and n is the sample size.
# r in [2, min{d, n − 2}]; The number of principal components to be computed.
# om; The vector of shrinkage parameters, (\omega_1 ,..., \omega_r),
#     where \omega_j in (0, 1] for j=1, ..., r. (default: om = rep(1, r))

# OUTPUT:
# vectors[, j]; The estimator of the j-th shrinkage PC direction by A-SPCA.
# scores[, j];  The estimator of the j-th shrinkage PC scores for the centroid data sets,
#  x_1-\bar{x}, ..., x_n-\bar{x}.
# k[j]; The estimator of the k_{j\omega} given by (5.1) in Yata and Aoshima (2025).
#######################################################################################

SHPC <- function(X, r, om = NULL) {
    d <- dim(X)[1]
    n <- dim(X)[2]
    q <- min(n - 2, d, r)
    # omega
    om <- c(om, rep(1, q - length(om)))
    X <- sweep(X, 1, apply(X, 1, mean), "-")
    X0 <- X
    svd0 <- svd(X0 / (n - 1)^(1 / 2), nu = q, nv = q)
    sval <- svd0$d[1:q]
    svec <- svd0$v[, 1:q]
    trSd <- norm(X0, "F")^2 / (n - 1)
    nrmval <- numeric(q)
    nrmvec <- matrix(0, d, q)
    aspca <- matrix(0, d, q)
    asscore <- matrix(0, n, q)
    # shrinkage (integer \tilde{k}_{jω} for j = 1,..., q)
    k <- numeric(q)
    for (i in 1:q) {
        nrmval[i] <- sval[i]^2 - (trSd - sum(sval[1:i]^2)) / (n - i - 1)
        nrmvec[, i] <- X %*% svec[, i] / sqrt((n - 1) * nrmval[i])
        ord <- order(abs(nrmvec[, i]), decreasing = T)
        cri <- 0
        for (j in 1:d) {
            cri <- cri + nrmvec[ord[j], i]^2
            aspca[ord[j], i] <- nrmvec[ord[j], i]
            # Remark F.1.
            if (cri >= om[i]) {
                k[i] <- j
                break
            }
        }
    }
    asscore <- t(X0) %*% aspca
    return(list(vectors = aspca, scores = asscore, k = k))
}
