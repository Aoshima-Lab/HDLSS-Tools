# **Distance-Based Discriminant Analysis**
   [[R](DBDA.r)] [[Python](DBDA.py)] [[Manual](DBDA.pdf)]
   
   The "Distance-Based Discriminant Analysis (DBDA)" provides high-dimensional discriminant analysis for multiclass data. The algorithm is provided in Aoshima and Yata (2014).
   >   Reference : M. Aoshima and K. Yata, A distance-based, misclassification rate adjusted classifier for multiclass, high-dimensional data, Annals of the Institute of Statistical Mathematics (2014).  
    DOI : [[10.1007/s10463-013-0435-8](https://link.springer.com/article/10.1007/s10463-013-0435-8)]

## Usage
### Input
```{r}
# train_X: p × n (=n_1+...+n_k) training data matrix where p is the dimension, k is the number of classes, n is the total sample size and n_i is the size of the i-th class in training data.
# train_y: n dimensional vector where n is the size of training data. The order of the label vector should correspond to training data matrix.
# test_X: p × N testing data matrix, where p is the dimension and N is the sample size of testing data.
# option: Boolean value (default: FALSE). 
#         If TRUE, displays detailed information about the training and testing data, 
#         including the number of samples, data dimensions, and label distributions 
#         in both training data and predictions. Useful for debugging and analysis.
```

### Output
```{r} 
# predictions: Estimated labels based on DBDA.
```