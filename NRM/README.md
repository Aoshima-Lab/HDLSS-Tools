# **Noise Reduction Methodology**
   [[R](NRM.r)] [[Python](NRM.py)] [[Manual](NRM.pdf)]
   
   The "Noise-Reduction Methodology (NRM)" gives estimators of the eigenvalues, eigenvectors, and principal component scores.
   
   >   Reference : K. Yata, M. Aoshima, Effective PCA for High-Dimension, Low-Sample-Size Data with Noise Reduction via Geometric Representations, Journal of Multivariate Analysis, 105 (2012) 193-215  
      DOI : [[10.1016/j.jmva.2011.09.002](https://www.sciencedirect.com/science/article/pii/S0047259X11001904)]

## Usage
### Input
```{r}
# NRM(X, r);  d (≥ 2) by n (≥ 4) matrix X as X = (x1, ..., xn),
# where d is the dimension and n is the sample size.
# r in [2, min{d, n − 2}] : (the number of principal components to be computed).
```

### Output
```{r} 
# values[j]; The estimator of the j-th eigenvalue by the NR method. 
# vectors[, j]; The estimator of the j-th PC direction by the NR method.
# scores[, j];  The estimator of the j-th PC scores for x_1,...,x_n by the NR method.
```