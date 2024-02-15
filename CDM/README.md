# **Cross-Data-Matrix Methodology**
   [[R](CDM.r)] [[Python](CDM.py)] [[Manual](CDM.pdf)]

   The "Cross-Data-Matrix (CDM) Methodology" gives estimators of the eigenvalues, eigenvectors, and principal component scores.
   
   >   Reference : K. Yata, M. Aoshima, Effective PCA for High-Dimension, Low-Sample-Size Data with Singular Value Decomposition of Cross Data Matrix, Journal of Multivariate Analysis, 101 (2010) 2060-2077  
      DOI: [[10.1016/j.jmva.2010.04.006](https://www.sciencedirect.com/science/article/pii/S0047259X10000904)]

## Usage
### Input
```{r}
# CDM(X, r, random); d (≥ 2) by n (≥ 4) matrix X as X = (x1, ..., xn),
# where d is the dimension and n is the sample size.
# r in [2, min{d, n/2 − 1}] : (the number of principal components to be computed).
# random(R), rand(Python): 'True' or 'False' (default: 'False')
```

### Output
```{r}
# values[j]; The estimator of the j-th eigenvalue by the CDM method.
# vectors[, j]; The estimator of the j-th PC direction by the CDM method.
# scores[, j];  The estimator of the j-th PC scores for x_1,...,x_n by the CDM method.
```