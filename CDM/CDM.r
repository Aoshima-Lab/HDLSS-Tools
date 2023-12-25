#######################################################################################
#INPUT: CDM(X, r, random); d (≥ 2) by n (≥ 4) matrix X as X = (x1, ..., xn),
# where d is the dimension and n is the sample size.
# r in [2, min{d, n/2 − 1}] : (the number of principal components to be computed).
# random: 'True' or 'False' (default: 'False')

#OUTPUT:
# values[j]; The estimator of the j-th eigenvalue by the CDM method.
# vectors[, j]; The estimator of the j-th PC direction by the CDM method.
# scores[, j];  The estimator of the j-th PC scores for x_1,...,x_n by the CDM method.
#######################################################################################

CDM <- function(X, r, random='False'){
  d <- dim(X)[1]
  n <- dim(X)[2]
  n1 <- as.integer(ceiling(n/2))
  n2 <- n - n1
  n12 <- list(n1, n2)
  q <- min(n2-1, d, r)
  
  if (random=='False'){
    index <- c(1:n)
    Xcdm <- list(X[, 1:n1], X[, (n1+1):n])
  } else if (random=='True'){
    pi <- matrix(1/n, 1, n)
    index <- sample(c(1:n), n, replace=FALSE, pi)
    Xcdm <- list(X[, index[1:n1]], X[, index[(n1+1):n]])
  }
  Mean <- list(apply(Xcdm[[1]], 1, mean), apply(Xcdm[[2]], 1, mean))
  for (i in 1:2){
    Xcdm[[i]] <- sweep(Xcdm[[i]], 1, Mean[[i]], '-')
  }
  
  Sd <- t(Xcdm[[1]]) %*% Xcdm[[2]] / sqrt((n1 - 1) * (n2 - 1))
  eig <- svd(Sd, nu=q, nv=q)
  cdmval <- eig$d[1:q]
  crossvec <- list(eig$u[, 1:q], eig$v[, 1:q])
  
  cdmvec <- matrix(0, d, q)
  cdmscore <- matrix(0, n, q)
  
  for (i in 1:q){
    crossvec[[2]][, i] <- sign(as.numeric(crossvec[[1]][, i] %*% t(Xcdm[[1]]) %*% Xcdm[[2]] %*% crossvec[[2]][, i])) * crossvec[[2]][, i]
    
    #eigenvalue and eigenvector
    h <- list(0, 0)
    for (j in 1:2){
      h[[j]] <- Xcdm[[j]] %*% crossvec[[j]][, i] / sqrt(cdmval[i] * (n12[[j]] - 1))
    }
    
    cdmvec[, i] <- as.vector(h[[1]] + h[[2]]) / 2
    cdmvec[, i] <- cdmvec[, i] / norm(cdmvec[, i], type='2')
    
    
    #score
    r_score <- list(numeric(n1), numeric(n2))
    for (j in 1:2){
      for (k in 1:n12[[j]]){
        r_score[[j]][k] <- crossvec[[j]][k, i] * sqrt(n12[[j]] * cdmval[i])
      }
    }
    for (k in 1:n){
      cdmscore[index[k], i] <- c(r_score[[1]], r_score[[2]])[k]
    }
  }
  
  return(list(values=cdmval, vectors=cdmvec, scores=cdmscore))
}