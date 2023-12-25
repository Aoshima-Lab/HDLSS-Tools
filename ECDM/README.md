# **Extended Cross-Data-Matrix Methodology**<!-- omit in toc -->
   [[R-code](ECDM.r)] [[Manual](ECDM.pdf)]

   The "Extended Cross-Data-Matrix (ECDM) Methodology" gives an estimator of $\mathrm{Tr}(\Sigma^2)$, where $\Sigma$ is a  covariance matrix. This code tests the correlation coefficient matrix by the ECDM estimator.
   
   >   Reference : K. Yata, M. Aoshima, High-Dimensional Inference on Covariance Structures via the Extended Cross-Data-Matrix Methodology, Journal of Multivariate Analysis, 151 (2016) 151-166  
      DOI: [[10.1016/j.jmva.2016.07.011](https://www.sciencedirect.com/science/article/pii/S0047259X16300550)]

## Usage<!-- omit in toc -->

### Contents<!-- omit in toc -->
- [Estimation of Tr(Σ^2) by the ECDM methodology.](#estimation-of-trς2-by-the-ecdm-methodology)
- [Test of the correlation coefficient matrix by the ECDM estimator.](#test-of-the-correlation-coefficient-matrix-by-the-ecdm-estimator)


### Estimation of Tr(Σ^2) by the ECDM methodology.
#### Input<!-- omit in toc -->
```{r}
# W(X); p by n matrix X as X=(x_{1},...,x_{n}), 
# where n (≧ 4) is the sample size and p (≧ 1) is the dimension.
```
#### Output<!-- omit in toc -->
```{r}
# Wn: The estimator of \tr(\Sigma^2) by the ECDM methodology.
```

### Test of the correlation coefficient matrix by the ECDM estimator. 
#### Input<!-- omit in toc -->
```{r} 
# Tecdm(X1,X2); p_1 by n matrix X1 and p_2 by n matrix X2 as X1=(x_{11},...,x_{1n}) and X2=(x_{21},...,x_{2n}), 
# where n (≧ 4) is the sample size and p_i (≧ 1) is the dimension of Xi.
```
#### Output<!-- omit in toc -->
```{r}
# TestStatistics: The test statistic value for (5) (\hat{T}_n/\hat{\delta}).
# pvalue: The asymptotic p-value for testing (1) by (5) 
# (1-\Phi(\hat{T}_n/\hat{\delta}), where \Phi(x) is the c.d.f. of N(0,1)).
# Tn: The estimator of \Delta (\hat{T}_n).
# delta: The estimator of the standard deviation for \hat{T}_n. 
```