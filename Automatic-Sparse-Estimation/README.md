# **Automatic Sparse Estimation**
   [[R](Automatic_sparse_estimation.r)] [[Python](Automatic_sparse_estimation.py)]

   The "Automatic Sparse Estimation" module provides sparse estimation of the high-dimensional cross-covariance matrix and mean vectors.
   
   **Methodology:** This method uses the Extended Cross-Data-Matrix (ECDM) methodology to compute sparsification thresholds. For the hypothesis test of cross-covariance, see [[HDLSS-tools/ECDM](../../HDLSS-tools/ECDM/)].

   > Reference : T. Umino, K. Yata and M. Aoshima, Automatic sparse estimation of the high-dimensional cross-covariance matrix, Journal of Multivariate Analysis, (2025) (in press).  
      DOI: [[10.1016/j.jmva.2025.105590](https://doi.org/10.1016/j.jmva.2025.105590)]

## Usage

### sparse_cross_cov
`sparse_cross_cov(X1, X2)`

- **Parameters**
   - `X1`: p1 x n matrix (class 1)
   - `X2`: p2 x n matrix (class 2)
- **Returns** (R: list / Python: tuple)
   - `sparse_cross_cov`: sparse cross-covariance (p1 x p2)
   - `sample_cross_cov`: sample cross-covariance (p1 x p2)
   - `Delta`: sparsification threshold (ECDM)

### sparse_mean
`sparse_mean(X1, X2 = NULL)`

- **Parameters**
   - `X1`: p x n1 matrix
   - `X2`: optional p x n2 matrix (class 2). If missing, estimates sparse mean of `X1`; if provided, estimates sparse difference between class means.
- **Returns** (R: list / Python: tuple)
   - `sparse_mean`: sparse mean (or mean difference) (p,)
   - `sample_mean`: sample mean (or mean difference) (p,)
   - `Delta`: sparsification threshold

---

## Quick start

```r
# R
cov_res <- sparse_cross_cov(X1, X2)
sparse_cov  <- cov_res$sparse_cross_cov
sample_cov  <- cov_res$sample_cross_cov
Delta_cov   <- cov_res$Delta

mean_res <- sparse_mean(X1, X2)
sparse_mean_vec  <- mean_res$sparse_mean
sample_mean_vec  <- mean_res$sample_mean
Delta_mean       <- mean_res$Delta
```

```python
# Python
sparse_cov, sample_cov, Delta_cov = sparse_cross_cov(X1, X2)
sparse_mean_vec, sample_mean_vec, Delta_mean = sparse_mean(X1, X2)
```