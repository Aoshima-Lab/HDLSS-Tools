# **Automatic Sparse PCA**<!-- omit in toc -->
   [[R-code](ASPCA.r)] [[Manual](ASPCA.pdf)]

   The "Automatic Sparse PCA (A-SPCA)" gives estimators of the eigenvalues, eigenvectors and
   PC scores for the centroid data sets.

   >  Reference : K. Yata, M. Aoshima, Automatic Sparse PCA for High-Dimensional Data, Statistica Sinica 35 (2025) (in press).  
      DOI : [[10.5705/ss.202022.0319](https://www3.stat.sinica.edu.tw/ss_newpaper/SS-2022-0319_na.pdf)] [[Supplement](https://www3.stat.sinica.edu.tw/preprint/supp/2022-0319_supp.pdf)]

## Usage<!-- omit in toc -->

### Contents<!-- omit in toc -->
- [A-SPCA](#a-spca)
- [The shrinkage PC direction h\_{j\\omega} given by (5.2), the shrinkage PC scores given by (5.3) and k\_{j\\omega} given by (5.1) in the reference](#the-shrinkage-pc-direction-h_jomega-given-by-52-the-shrinkage-pc-scores-given-by-53-and-k_jomega-given-by-51-in-the-reference)


### A-SPCA
#### Input<!-- omit in toc -->
```{r}
# ASPCA(X, r); d (≥ 2) by n (≥ 4) matrix X as X = (x1, ..., xn),
# where d is the dimension and n is the sample size.
# r in [2, min{d, n − 2}]; The number of principal components to be computed.
```
#### Output<!-- omit in toc -->
```{r} 
# values[j]; The estimator of the j-th eigenvalue by A-SPCA (the NR method).
# vectors[, j]; The estimator of the j-th PC direction by A-SPCA.
# scores[, j];  The estimator of the j-th PC scores for the centroid data sets,
#   x_1-\bar{x}, ..., x_n-\bar{x}, by A-SPCA.
```

### The shrinkage PC direction h_{j\omega} given by (5.2), the shrinkage PC scores given by (5.3) and k_{j\omega} given by (5.1) in the reference
#### Input<!-- omit in toc -->
```{r} 
# SHPC(X, r, om = NULL); d (≥ 2) by n (≥ 4) matrix X as X = (x1, ..., xn),
# where d is the dimension and n is the sample size.
# r in [2, min{d, n − 2}]; The number of principal components to be computed.
# om; The vector of shrinkage parameters, (\omega_1 ,..., \omega_r), 
#     where \omega_j in (0, 1] for j=1, ..., r. (default: om = rep(1, r))
```
#### Output<!-- omit in toc -->
```{r}
# vectors[, j]; The estimator of the j-th shrinkage PC direction by A-SPCA.
# scores[, j];  The estimator of the j-th shrinkage PC scores for the centroid data sets,
#  x_1-\bar{x}, ..., x_n-\bar{x}.
# k[j]; The estimator of the k_{j\omega} given by (5.1) in Yata and Aoshima (2025).
```