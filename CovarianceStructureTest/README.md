# **Covariance Structure Test**
   [[R](CovStructureTest.R)] [[Python](CovStructureTest.py)]

   The "Covariance Structure Test" module provides hypothesis tests for high-dimensional covariance structures based on the Extended Cross-Data-Matrix (ECDM) methodology.

   > Reference: A. Ishii, K. Yata and M. Aoshima, Hypothesis tests for high-dimensional covariance structures, Annals of the Institute of Statistical Mathematics, 73 (2021), 599-622.  
   DOI: [[10.1007/s10463-020-00760-5](https://link.springer.com/article/10.1007/s10463-020-00760-5)]

## Usage

### Y
`Y(X)`

Computes cross-validated centered components for all n(n-1)/2 (=n_pairs) sample pairs based on ECDM methodology.

- **Parameters**
   - `X`: p x n matrix (p: dimension, n: sample size ≥ 4)
- **Returns** (R: list / Python: dict)
   - `Y1`: p x n_pairs matrix (centered components for first sample in each pair)
   - `Y2`: p x n_pairs matrix (centered components for second sample in each pair)
   - `indices`: (i,j) pair indices where i < j (n_pairs x 2)

### T_scaled_identity
`T_scaled_identity(X)`

Tests whether the covariance matrix has scaled identity structure (Σ = σ²I).

- **Parameters**
   - `X`: p x n matrix
- **Returns** (R: list / Python: dict)
   - `TestStatistics`: test statistic value
   - `pvalue`: asymptotic p-value (1-Φ(test statistic), where Φ is the standard normal CDF)

### T_diagonal
`T_diagonal(X)`

Tests whether the covariance matrix is diagonal (Σ = diag(σ₁², ..., σₚ²)).

- **Parameters**
   - `X`: p x n matrix
- **Returns** (R: list / Python: dict)
   - `TestStatistics`: test statistic value
   - `pvalue`: asymptotic p-value

### T_intraclass
`T_intraclass(X)`

Tests whether the covariance matrix has intraclass correlation structure (compound symmetry).

- **Parameters**
   - `X`: p x n matrix
- **Returns** (R: list / Python: dict)
   - `TestStatistics`: test statistic value
   - `pvalue`: asymptotic p-value

---

## Quick start

```r
# R
# Test for scaled identity structure
result_si <- T_scaled_identity(X)
cat("Test statistic:", result_si$TestStatistics, "\n")
cat("p-value:", result_si$pvalue, "\n")

# Test for diagonal structure
result_diag <- T_diagonal(X)
cat("Test statistic:", result_diag$TestStatistics, "\n")
cat("p-value:", result_diag$pvalue, "\n")

# Test for intraclass structure
result_ic <- T_intraclass(X)
cat("Test statistic:", result_ic$TestStatistics, "\n")
cat("p-value:", result_ic$pvalue, "\n")

# Get cross-validated components for custom analysis
Y_list <- Y(X)
Y1 <- Y_list$Y1  # p x n_pairs
Y2 <- Y_list$Y2  # p x n_pairs
```

```python
# Python
# Test for scaled identity structure
result_si = T_scaled_identity(X)
print("Test statistic:", result_si['TestStatistics'])
print("p-value:", result_si['pvalue'])

# Test for diagonal structure
result_diag = T_diagonal(X)
print("Test statistic:", result_diag['TestStatistics'])
print("p-value:", result_diag['pvalue'])

# Test for intraclass structure
result_ic = T_intraclass(X)
print("Test statistic:", result_ic['TestStatistics'])
print("p-value:", result_ic['pvalue'])

# Get cross-validated components for custom analysis
Y_dict = Y(X)
Y1 = Y_dict['Y1']  # p x n_pairs
Y2 = Y_dict['Y2']  # p x n_pairs
```