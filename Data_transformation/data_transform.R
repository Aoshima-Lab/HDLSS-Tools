check_sse <- function(X, centering = FALSE, random = FALSE, seed = NULL) {
  #' Estimation of the number of strongly spiked eigenvalues of the covariance matrix
  #'
  #' @param X matrix, shape (d, n) - Data matrix (features x samples)
  #' @param centering logical - If TRUE, center the data before splitting
  #' @param random logical - If TRUE, randomly split samples; if FALSE, split deterministically
  #' @param seed integer or NULL - Random seed for reproducibility (used if random=TRUE)
  #' @return khat integer - Estimated number of spiked eigenvalues
  
  if (centering) {
    X <- sweep(X, 1, rowMeans(X), "-")
  }
  d <- nrow(X)
  n <- ncol(X)
  n1 <- as.integer(ceiling(n / 2))
  n2 <- n - n1
  q  <- min(n2 - 1, d)
  if (isTRUE(random)) {
    if (!is.null(seed)) set.seed(seed)
    idx <- sample.int(n, n, replace = FALSE)
    X1 <- X[, idx[1:n1], drop = FALSE]
    X2 <- X[, idx[(n1 + 1):n], drop = FALSE]
  } else {
    X1 <- X[, 1:n1, drop = FALSE]
    X2 <- X[, (n1 + 1):n, drop = FALSE]
  }
  X1 <- sweep(X1, 1, rowMeans(X1), "-")
  X2 <- sweep(X2, 1, rowMeans(X2), "-")
  Sd <- t(X1) %*% X2 %*% t(X2) %*% X1 / ((n1 - 1) * (n2 - 1))
  cdmval <- eigen(Sd, symmetric = TRUE, only.values = TRUE)$values[1:q]
  kappa <- sqrt(log(n) / n)
  khat <- q
  psi <- sum(diag(Sd))
  tau_hat <- 1 - cdmval[1] / psi
  condition <- tau_hat * (1 + kappa)
  if (q > 1) {
    for (l in 1:(q - 1)) {
      if (condition > 1) {
        khat <- l - 1
        break
      }
      psi <- psi - cdmval[l]
      tau_hat <- 1 - cdmval[l + 1] / psi
      condition <- tau_hat * (1 + (l + 1) * kappa)
    }
  }
  khat <- min(khat, n2 - 2)
  return(as.integer(khat))
}

NRM_trans <- function(X, centering = FALSE, sse_point = NULL, random = FALSE, seed = NULL) {
  #' Data transformation based on the noise-reduction methodology
  #'
  #' @param X matrix, shape (d, n) - Data matrix (features x samples)
  #' @param centering logical - If TRUE, center the data before further processing
  #' @param sse_point integer or NULL - Number of spiked eigenvalues; if NULL, estimated by check_sse
  #' @param random logical - If TRUE, randomly split samples for sse estimation
  #' @param seed integer or NULL - Random seed for reproducibility
  #' @return list with X_trans (sse_point x n) and nrmvec (d x sse_point)
  
  if (centering) {
    X <- sweep(X, 1, rowMeans(X), "-")
  }
  d <- nrow(X)
  n <- ncol(X)
  sse_point <- if (is.null(sse_point)) check_sse(X, centering = centering, random = random, seed = seed) else as.integer(sse_point)
  # Calculate sample eigenvalues and dual-eigenvectors
  X0 <- if (centering) X else sweep(X, 1, rowMeans(X), "-")
  eg <- eigen(t(X0) %*% X0 / (n - 1), symmetric = TRUE)
  eigvals <- eg$values[1:sse_point]
  dualvecs <- eg$vectors[, 1:sse_point, drop = FALSE]
  #Noise-reduced eigenvalues and eigenvectors
  trSd <- sum(X0^2) / (n - 1)
  cs <- cumsum(eigvals)
  denom <- n - (seq_len(sse_point) + 1)
  nrmval <- eigvals - (trSd - cs) / denom
  nrmvec <- (X0 %*% dualvecs) / (sqrt(n - 1) * matrix(sqrt(nrmval), nrow = d, ncol = sse_point, byrow = TRUE))
  #NRM transformation
  c <- sqrt(n - 1) / (n - 2)
  nr_projection_term <- sqrt(n - 1) * crossprod(nrmvec, X)
  #Calculate bias correction term
  dualvec_scaled <- sweep(dualvecs, 2, sqrt(nrmval), "/")
  x0_dot_x <- colSums(X0 * X)
  bias_correction_term <- (n / (n - 1)) * (t(dualvec_scaled) * matrix(x0_dot_x, nrow = sse_point, ncol = n, byrow = TRUE))
  #Final transformed data
  X_trans <- c * (nr_projection_term - bias_correction_term)
  return(list(X_trans = X_trans, nrmvec = nrmvec))
}
