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

W <- function(X){
  p <- list(dim(X)[1])
  n <- dim(X)[2]
  n1 <- as.integer(ceiling(n/2))
  n2 <- n - n1
  
  K <- c(3:(2*n-1))
  L <- length(K)
  Y <- array(0, dim=c(2, L, p[[1]]))
  for (l in 1:L)
  {
    V <- list()
    dv <- as.integer(floor(K[l]/2))
    
    if (dv >= n1){
      id <- c((dv-n1+1): dv)
      V <- append(V, list(id))
    } else{
      id <- append(c(1: dv), c((dv+n2+1): n))
      V <- append(V, list(id))
    }
    
    if (dv <= n1){
      id <- c((dv+1): (dv+n2))
      V <- append(V, list(id))
    } else{
      id <- append(c(1: (dv-n1)), c((dv+1): n))
      V <- append(V, list(id))
    }
    
    for (i in 1:2)
    {
      Y[i, l, ] <- apply(X[, V[[i]]], 1, mean)
    }
  }
  
  u <- n1 * n2 / ((n1-1) * (n2-1))
  w <- 0
  for (j in 1:n){
    for (i in 1:j){
      if (i != j){
        w <- w + (as.numeric((X[, i] - Y[1, (i+j-2), ]) %*% (X[, j] - Y[2, (i+j-2), ])))^2
      }
    }
  }
  W <-  2 * u / (n * (n - 1)) * w
  return(list(Wn=W))
}


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

Tecdm <- function(X1, X2){
  if (is.null(dim(X1))){
    X1 <- t(as.matrix(X1))
  }
  if (is.null(dim(X2))){
    X2 <- t(as.matrix(X2))
  }
  p <- list(dim(X1)[1], dim(X2)[1])
  n <- dim(X1)[2]
  n1 <- as.integer(ceiling(n/2))
  n2 <- n - n1
  
  K <- c(3:(2*n-1))
  L <- length(K)
  Y1 <- array(0, dim=c(2, L, p[[1]]))
  Y2 <- array(0, dim=c(2, L, p[[2]]))
  for (l in 1:L){
    V <- list()
    dv <- as.integer(floor(K[l]/2))
    
    if (dv >= n1){
      id <- c((dv-n1+1): dv)
      V <- append(V, list(id))
    } else{
      id <- append(c(1: dv), c((dv+n2+1): n))
      V <- append(V, list(id))
    }
    
    if (dv <= n1){
      id <- c((dv+1): (dv+n2))
      V <- append(V, list(id))
    } else{
      id <- append(c(1: (dv-n1)), c((dv+1): n))
      V <- append(V, list(id))
    }
    
    for (i in 1:2){
      if (is.null(dim(X1[, V[[i]]]))){
        Y1[i, l, ] <- apply(t(as.matrix(X1[, V[[i]]])), 1, mean)
      } else {
        Y1[i, l, ] <- apply(X1[, V[[i]]], 1, mean)
      }
      if (is.null(dim(X2[, V[[i]]]))){
        Y2[i, l, ] <- apply(t(as.matrix(X2[, V[[i]]])), 1, mean)
      } else {
        Y2[i, l, ] <- apply(X2[, V[[i]]], 1, mean)
      }
    }
  }
  
  u <- n1 * n2 / ((n1-1) * (n2-1))
  w1 <- 0
  w2 <- 0
  t <- 0
  for (j in 1:n){
    for (i in 1:j){
      if (i != j){
        t  <- t + as.numeric((X1[, i] - Y1[1, (i+j-2), ]) %*% (X1[, j] - Y1[2, (i+j-2), ])) * as.numeric((X2[, i] - Y2[1, (i+j-2), ]) %*% (X2[, j] - Y2[2, (i+j-2), ]))
        w1 <- w1 + (as.numeric((X1[, i] - Y1[1, (i+j-2), ]) %*% (X1[, j] - Y1[2, (i+j-2), ])))^2
        w2 <- w2 + (as.numeric((X2[, i] - Y2[1, (i+j-2), ]) %*% (X2[, j] - Y2[2, (i+j-2), ])))^2
      }
    }
  }
  W1 <-  2 * u / (n * (n - 1)) * w1
  W2 <-  2 * u / (n * (n - 1)) * w2
  T_hat <-  2 * u / (n * (n - 1)) * t
  delta_hat <- sqrt(2 * W1 * W2) / n
  test <- T_hat / delta_hat
  p_value <-  pnorm(test, lower.tail = FALSE)
  return(list(TestStatistics=test, pvalue=p_value, Tn=T_hat, delta=delta_hat))
}