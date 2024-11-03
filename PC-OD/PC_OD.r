#######################################################################################
# INPUT: PC_OD(X, alpha); d by n matrix X as X = (x1, ..., xn),
# where d is the dimension and n is the sample size.
# alpha: Significance level of the test (0 < alpha < 0.5).

# OUTPUT: 
# outliers: The index of the outliers.
#######################################################################################

PC_OD <- function(X, alpha = 0.05){
  # Step2
  n_all <- dim(X)[2]
  samples <- seq_len(n_all)
  inliers <- samples
  while (TRUE) {
    n <- length(inliers)
    X_cent <- X - rowMeans(X)
    svd0 <- svd(X_cent / (n - 1)^(1/2), nu=1, nv=1)
    dualvec <- svd0$v
    # Step3
    t_value <- qt(alpha / (2 * n) ,n - 2)
    t0 <- ((n - 1) / sqrt(n)) * sqrt(t_value^2 / (n - 2 + t_value^2))
    T_PC1 <- max(abs(dualvec)) * sqrt(n - 1)
    # Step4
    if (T_PC1 <= t0) {
      break
    } else {
    outlier <- which.max(abs(dualvec))
    X <- X[, -outlier]
    inliers <- inliers[-outlier]
    }
  }
  outliers <- setdiff(samples, inliers)
  return(outliers)
}