#######################################################################################
#INPUT: NRM(X, r);  d (≥ 2) by n (≥ 4) matrix X as X = (x1, ..., xn),
# where d is the dimension and n is the sample size.
# r in [2, min{d, n − 2}] : (the number of principal components to be computed).

#OUTPUT:
# values[j]; The estimator of the j-th eigenvalue by the NR method. 
# vectors[, j]; The estimator of the j-th PC direction by the NR method.
# scores[, j];  The estimator of the j-th PC scores for x_1,...,x_n by the NR method.
#######################################################################################

NRM <- function(X, r){
  d <- dim(X)[1]
  n <- dim(X)[2]
  q <- min(n-2, d, r)
  X <- sweep(X, 1, apply(X, 1, mean), '-')
  X0 <- X
  svd0 <- svd(X0/(n - 1)^(1/2), nu=q, nv=q)
  sval <- svd0$d[1:q]
  svec <- svd0$v[, 1:q]
  trSd <- norm(X0, "F")^2/(n-1)
  nrmval <- numeric(q)
  nrmvec <- matrix(0, d, q)
  nrmscore <- matrix(0, n, q)
  
  for (i in 1:q){
        nrmval[i] <- sval[i]^2 - (trSd - sum(sval[1:i]^2))/(n - i - 1)
        nrmvec[, i] <- X %*% svec[, i]/sqrt((n - 1) * nrmval[i])
    
    for (j in 1:n){
      nrmscore[j, i] <- svec[j, i] * sqrt(n * nrmval[i])
    }
  }
  return(list(values=nrmval, vectors=nrmvec, scores=nrmscore))
}