#' Compute the threshold (Tn) for sparse estimation via ECDM methodology.
#'
#' @param X1 p1 x n matrix (class 1)
#' @param X2 p2 x n matrix (class 2)
#'
#' @return Tn: float
#'   Sparsification threshold for cross-covariance matrix
#'
#' @keywords internal
ECDM <- function(X1, X2) {
  if (is.null(dim(X1))) {
    X1 <- t(as.matrix(X1))
  }
  if (is.null(dim(X2))) {
    X2 <- t(as.matrix(X2))
  }
  
  p <- list(dim(X1)[1], dim(X2)[1])
  n <- dim(X1)[2]
  n1 <- as.integer(ceiling(n / 2))
  n2 <- n - n1
  
  K <- c(3:(2 * n - 1))
  L <- length(K)
  Y1 <- array(0, dim = c(2, L, p[[1]]))
  Y2 <- array(0, dim = c(2, L, p[[2]]))
  
  for (l in 1:L) {
    V <- list()
    dv <- as.integer(floor(K[l] / 2))
    
    if (dv >= n1) {
      id <- c((dv - n1 + 1):dv)
      V <- append(V, list(id))
    } else {
      id <- append(c(1:dv), c((dv + n2 + 1):n))
      V <- append(V, list(id))
    }
    
    if (dv <= n1) {
      id <- c((dv + 1):(dv + n2))
      V <- append(V, list(id))
    } else {
      id <- append(c(1:(dv - n1)), c((dv + 1):n))
      V <- append(V, list(id))
    }
    
    for (i in 1:2) {
      if (is.null(dim(X1[, V[[i]]]))) {
        Y1[i, l, ] <- apply(t(as.matrix(X1[, V[[i]]])), 1, mean)
      } else {
        Y1[i, l, ] <- apply(X1[, V[[i]]], 1, mean)
      }
      if (is.null(dim(X2[, V[[i]]]))) {
        Y2[i, l, ] <- apply(t(as.matrix(X2[, V[[i]]])), 1, mean)
      } else {
        Y2[i, l, ] <- apply(X2[, V[[i]]], 1, mean)
      }
    }
  }
  
  u <- n1 * n2 / ((n1 - 1) * (n2 - 1))
  t <- 0
  for (j in 1:n) {
    for (i in 1:j) {
      if (i != j) {
        t <- t + as.numeric((X1[, i] - Y1[1, (i + j - 2), ]) %*% (X1[, j] - Y1[2, (i + j - 2), ])) * 
                 as.numeric((X2[, i] - Y2[1, (i + j - 2), ]) %*% (X2[, j] - Y2[2, (i + j - 2), ]))
      }
    }
  }
  Tn <- 2 * u / (n * (n - 1)) * t
  
  Tn
}

#' Sparse estimation of the high-dimensional cross-covariance matrix.
#'
#' @param X1 p1 x n matrix (class 1)
#' @param X2 p2 x n matrix (class 2)
#'
#' @return A list containing:
#'   \itemize{
#'     \item sparse_cross_cov: Sparse cross-covariance matrix (p1 x p2)
#'     \item sample_cross_cov: Sample cross-covariance matrix (p1 x p2)
#'     \item Delta: Sparsification threshold from ECDM
#'   }
#'
#' @export
sparse_cross_cov <- function(X1, X2) {
  p1 <- nrow(X1)
  n <- ncol(X1)
  p2 <- nrow(X2)
  p <- p1 * p2

  Delta <- ECDM(X1, X2)

  X1c <- sweep(X1, 1, rowMeans(X1))
  X2c <- sweep(X2, 1, rowMeans(X2))

  sample_cross_cov <- (X1c %*% t(X2c)) / (n - 1)
  # Convert to column-major order (same as Python's order='F')
  cross_cov_vec <- as.vector(sample_cross_cov)

  sort_idx <- order(abs(cross_cov_vec), decreasing = TRUE)
  sparse_cross_cov <- rep(0, p)
  cri <- 0

  for (idx in seq_len(p)) {
    element_idx <- sort_idx[idx]
    cri <- cri + cross_cov_vec[element_idx]^2
    sparse_cross_cov[element_idx] <- cross_cov_vec[element_idx]
    if (cri >= Delta) break
  }

  # Reconstruct matrix in column-major order (byrow=FALSE is default)
  sparse_cross_cov_mat <- matrix(sparse_cross_cov, nrow = p1, ncol = p2, byrow = FALSE)
  list(sparse_cross_cov = sparse_cross_cov_mat, sample_cross_cov = sample_cross_cov, Delta = Delta)
}

#' Sparse mean vector estimation (one- or two-class).
#'
#' @param X1 p x n1 matrix
#' @param X2 optional p x n2 matrix (class 2). If missing, estimates sparse mean of X1;
#'           if provided, estimates sparse difference between class means.
#'
#' @return A list containing:
#'   \itemize{
#'     \item sparse_mean: Sparse mean vector (or sparse mean difference) (p,)
#'     \item sample_mean: Sample mean vector (or mean difference) (p,)
#'     \item Delta: Sparsification threshold
#'   }
#'
#' @export
sparse_mean <- function(X1, X2 = NULL) {
  p <- nrow(X1)
  n1 <- ncol(X1)

  if (is.null(X2)) {
    sample_mean <- rowMeans(X1)
    trS1 <- sum((t(X1) - rep(sample_mean, each = n1))^2) / (n1 - 1)
    Delta <- sum(sample_mean^2) - trS1 / n1
  } else {
    n2 <- ncol(X2)
    mean1 <- rowMeans(X1)
    mean2 <- rowMeans(X2)
    sample_mean <- mean1 - mean2
    trS1 <- sum((t(X1) - rep(mean1, each = n1))^2) / (n1 - 1)
    trS2 <- sum((t(X2) - rep(mean2, each = n2))^2) / (n2 - 1)
    Delta <- sum(sample_mean^2) - trS1 / n1 - trS2 / n2
  }

  sort_idx <- order(abs(sample_mean), decreasing = TRUE)
  sparse_mean <- rep(0, p)
  cri <- 0

  for (idx in seq_len(p)) {
    element_idx <- sort_idx[idx]
    cri <- cri + sample_mean[element_idx]^2
    sparse_mean[element_idx] <- sample_mean[element_idx]
    if (cri >= Delta) break
  }

  list(sparse_mean = sparse_mean, sample_mean = sample_mean, Delta = Delta)
}
