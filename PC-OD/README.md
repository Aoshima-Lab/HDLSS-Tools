# **PC-scores-based Outlier Detection**
   [[R](PC_OD.r)] [[Python](PC_OD.py)] [[Manual](PC_OD.pdf)]
   
   The "PC-scores-based Outlier Detection (PC-OD)" identifies outliers based on the PC scores. The algorithm is provided in section 3.2 of Nakayama et al. (2024).
   >   Reference :Y. Nakayama, K. Yata and M. Aoshima, Test for High-Dimensional Outliers with Principal Component Analysis, Japanese Journal of Statistics and Data Science (2024) (in print).  
    DOI : [[10.1007/s42081-024-00255-0](https://link.springer.com/article/10.1007/s42081-024-00255-0)]

## Usage
### Input
```{r}
# PC_OD(X, alpha); d by n matrix X as X = (x1, ..., xn),
# where d is the dimension and n is the sample size.
# alpha: Significance level of the test (0 < alpha < 0.5).
```

### Output
```{r} 
# outliers: The index of the outliers.
```