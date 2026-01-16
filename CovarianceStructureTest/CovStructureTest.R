Y <- function(X) {
  # Basic computation function for covariance matrix estimation via ECDM.
  #
  # Parameters
  # ----------
  # X : matrix
  #     p x n matrix (p: dimension, n: sample size)
  #
  # Returns
  # -------
  # list
  #     Y1: p x n_pairs matrix
  #     Y2: p x n_pairs matrix
  #     indices: (i,j) pair indices (n_pairs x 2)
  
  p <- dim(X)[1]
  n <- dim(X)[2]
  
  n1 <- as.integer(ceiling(n / 2))
  n2 <- n - n1
  u1 <- n1 / (n1 - 1)
  u2 <- n2 / (n2 - 1)
  
  S <- c(3:(2 * n - 1))
  L <- length(S)
  X_var <- array(0, dim = c(2, L, p))
  
  for (l in 1:L) {
    dv <- as.integer(floor(S[l] / 2))
    
    if (dv >= n1) {
      V1_idx <- c((dv - n1 + 1):dv)
    } else {
      V1_idx <- c(c(1:dv), c((dv + n2 + 1):n))
    }
    
    if (dv <= n1) {
      V2_idx <- c((dv + 1):(dv + n2))
    } else {
      V2_idx <- c(c(1:(dv - n1)), c((dv + 1):n))
    }
    
    X_var[1, l, ] <- apply(X[, V1_idx], 1, mean)
    X_var[2, l, ] <- apply(X[, V2_idx], 1, mean)
  }
  
  lower_idx_temp <- which(lower.tri(matrix(0, n, n)), arr.ind = TRUE)
  lower_idx <- lower_idx_temp[, c(2, 1)]
  n_pairs <- nrow(lower_idx)
  Y1_matrix <- matrix(0, p, n_pairs)
  Y2_matrix <- matrix(0, p, n_pairs)
  
  for (k in 1:n_pairs) {
    i <- lower_idx[k, 1]
    j <- lower_idx[k, 2]
    Y1_matrix[, k] <- sqrt(u1) * (X[, i] - X_var[1, (i + j - 2), ])
    Y2_matrix[, k] <- sqrt(u2) * (X[, j] - X_var[2, (i + j - 2), ])
  }
  
  return(list(
    Y1 = Y1_matrix,
    Y2 = Y2_matrix,
    indices = lower_idx
  ))
}


T_scaled_identity <- function(X) {
  # Test statistic under scaled identity covariance assumption.
  #
  # Parameters
  # ----------
  # X : matrix
  #     p x n matrix
  #
  # Returns
  # -------
  # list
  #     TestStatistics: test statistic value
  #     pvalue: asymptotic p-value
  
  p <- dim(X)[1]
  n <- dim(X)[2]
  Y_list <- Y(X)
  W_n <- 2 * sum(colSums(Y_list$Y1 * Y_list$Y2)^2) / (n * (n - 1))
  
  U_nS <- 2 * sum(colSums(Y_list$Y1^2) * colSums(Y_list$Y2^2)) / (p * n * (n - 1))
  
  test <- n * W_n / (2 * U_nS) - n / 2
  p_value <- pnorm(test, lower.tail = FALSE)
  
  return(list(TestStatistics = test, pvalue = p_value))
}


T_diagonal <- function(X) {
  # Test statistic under diagonal covariance assumption.
  #
  # Parameters
  # ----------
  # X : matrix
  #     p x n matrix
  #
  # Returns
  # -------
  # list
  #     TestStatistics: test statistic value
  #     pvalue: asymptotic p-value
  
  n <- dim(X)[2]
  Y_list <- Y(X)
  W_n <- 2 * sum(colSums(Y_list$Y1 * Y_list$Y2)^2) / (n * (n - 1))
  
  U_nD <- 2 * sum(Y_list$Y1^2 * Y_list$Y2^2) / (n * (n - 1))
  Psi_nD <- U_nD^2 - sum((2 * rowSums(Y_list$Y1^2 * Y_list$Y2^2) / (n * (n - 1)))^2)
  Delta_n <- W_n - U_nD
  
  test <- n * Delta_n / (2 * sqrt(Psi_nD))
  p_value <- pnorm(test, lower.tail = FALSE)
  
  return(list(TestStatistics = test, pvalue = p_value))
}


T_intraclass <- function(X) {
  # Test statistic under intraclass covariance assumption.
  #
  # Parameters
  # ----------
  # X : matrix
  #     p x n matrix
  #
  # Returns
  # -------
  # list
  #     TestStatistics: test statistic value
  #     pvalue: asymptotic p-value
  
  p <- dim(X)[1]
  n <- dim(X)[2]
  Y_list <- Y(X)
  W_n <- 2 * sum(colSums(Y_list$Y1 * Y_list$Y2)^2) / (n * (n - 1))
  
  Y1_norm <- colSums(Y_list$Y1^2)
  Y2_norm <- colSums(Y_list$Y2^2)
  Y1_one <- colSums(Y_list$Y1)^2
  Y2_one <- colSums(Y_list$Y2)^2
  
  U_nIC <- 2 * sum(Y1_one * Y2_one) / (p^2 * n * (n - 1)) + 2 * sum((Y1_norm - Y1_one / p) * (Y2_norm - Y2_one / p)) / ((p - 1) * n * (n - 1))
  Psi_nIC <- U_nIC^2 - (2 * sum(Y1_one * Y2_one) / (p^2 * n * (n - 1)))^2
  Delta_nIC <- W_n - U_nIC
  
  test <- n * Delta_nIC / (2 * sqrt(Psi_nIC))
  p_value <- pnorm(test, lower.tail = FALSE)
  
  return(list(TestStatistics = test, pvalue = p_value))
}