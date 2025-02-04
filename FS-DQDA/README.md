# **Feature Selected Diagonal Quadratic Discriminant Analysis**
   [[R](FS-DQDA.r)] [[Python](FS-DQDA.py)] [[Manual](FS-DQDA.pdf)]
   
   The "Feature Selected Diagonal Quadratic Discriminant Analysis" provides high-dimensional discriminant analysis for multiclass data. The algorithm is provided in Aoshima and Yata (2019).
   >   Reference : M. Aoshima and K. Yata, High-dimensional quadratic classifiers in non-sparse settings.Method- ology and Computing in Applied Probability.(2019) 
    DOI : [[10.1007/s11009-018-9646-z](https://link.springer.com/article/10.1007/s11009-018-9646-z]

## Usage
### Input
```{r}
# train_X: p × n (=n_1+...+n_k) training data matrix where p is the dimension, k is the number of classes, n is the total sample size and n_i is the size of the i-th class in training data.The diagonal components of the sample covariance matrix must not be zero.
# train_y: n dimensional vector where n is the size of training data. The order of the label vector should correspond to training data matrix.
# test_X: p × N testing data matrix, where p is the dimension and N is the sample size of testing data.
# gamma: A parameter ranging from 0 to 1.　The default value of gamma is 0.5. When the condition log(p)/n < 1 holds,larger values of gamma result in selecting more variables, while smaller values lead to stricter feature selection criteria.
# option1: Boolean value (default: False). 
#         If True, displays detailed information about the training and testing data, 
#         including the number of samples, data dimensions, number of selected variables, gamma, and label distributions in both training data and predictions. Useful for debugging and analysis.
# option2: Boolean value (default: False). 
#         If True, displays detailed information about selected variables.
```

### Output
```{r} 
# predictions: Estimated labels based on FS-DQDA.