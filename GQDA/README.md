# **Geometrical quadratic discriminant analysis**
   [[R](GQDA.R)] [[Python](GQDA.py)] [[Manual](GQDA.pdf)]
   
   The "Geometrical quadratic discriminant analysis(GQDA)" provides high-dimensional discriminant analysis for multiclass data. The algorithm is provided in Aoshima and Yata (2015).
   >   Reference : M. Aoshima and K. Yata, Geometric Classifier for Multiclass, High-Dimensional Data, Sequential Anal, 34, 279-294. (2015).  
    DOI : [[10.1080/07474946.2015.1063256](https://www.tandfonline.com/doi/full/10.1080/07474946.2015.1063256)]

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
# predictions: Estimated labels based on GQDA.
```