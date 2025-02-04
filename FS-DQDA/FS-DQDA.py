import numpy as np
import pandas as pd
from collections import Counter
#######################################################################################
# INPUT: FS_DQDA(train_X, train_y, test_X, gamma, option1, option2)
# train_X: p × n (=n_1+...+n_k) training data matrix where p is the dimension, k is the number of classes, n is the total sample size and n_i is the size of the i-th class in training data.The diagonal components of the sample covariance matrix must not be zero.
# train_y: n dimensional vector where n is the size of training data. The order of the label vector should correspond to training data matrix.
# test_X: p × N testing data matrix, where p is the dimension and N is the sample size of testing data.
# gamma: A parameter ranging from 0 to 1.　The default value of gamma is 0.5. When the condition log(p)/n < 1 holds,larger values of gamma result in selecting more variables, while smaller values lead to stricter feature selection criteria.
# option1: Boolean value (default: False). 
#         If True, displays detailed information about the training and testing data, 
#         including the number of samples, data dimensions, number of selected variables, gamma, and label distributions in both training data and predictions. Useful for debugging and analysis.
# option2: Boolean value (default: False). 
#         If True, displays detailed information about selected variables.
# OUTPUT
#predictions: Estimated labels based on FS-DQDA.
#######################################################################################

def FS_DQDA(train_X, train_y, test_X , gamma = 0.5, option1 = False,option2 = False):
    unique_labels = np.unique(train_y)
    class_scores = []
    diags = {}
    means = {}
    nums = {}
    num_classes = len(unique_labels)
    dim = train_X.shape[0]
    tests_num = test_X.shape[1]
    for label in unique_labels:
        data_in_class = train_X[:, train_y == label]
        num_data_in_class = data_in_class.shape[1]
        
        if num_data_in_class <= 1:
            raise ValueError("Each class must have more than one training data")
        mean_in_class = np.mean(data_in_class, axis=1).reshape(-1, 1)
        diag_in_class = np.sum((data_in_class - mean_in_class)**2, axis=1) / (num_data_in_class - 1)
        diags[label] = diag_in_class.reshape(-1,1)
        means[label] = mean_in_class
        nums[label] = num_data_in_class
    min_num = min(nums.values())
    theta = -1
    for label_i in unique_labels:
      for label_j in unique_labels:
        if label_i != label_j:
          theta += ((means[label_i] - means[label_j])**2 + diags[label_i])/ (num_classes * (num_classes-1) * diags[label_j])

    condition = theta > (np.log(dim) / min_num)**(gamma / 2)  
    D_hat = np.where(condition)[0]  

    # Prediction
    class_scores = {}
    for label in unique_labels:
        if np.any(diags[label][D_hat] == 0):
            raise ValueError("Zero division error occurred because some diagonal elements of the sample covariance matrix are zero.")  
        FS_W = np.sum(((test_X[D_hat, :] - means[label][D_hat])**2 / diags[label][D_hat]) - 1 / nums[label] + np.log(diags[label][D_hat]), axis=0)
        class_scores[label] = FS_W
    predictions = []
    for i in range(tests_num):
      predictions.append(min(class_scores, key=lambda k: class_scores[k][i]))
    
    if option1:
        print("FS_DQDA function called. Set option=False to hide this information.")
        print(f"Training data size: {len(train_y)}")
        print(f"Test data size: {test_X.shape[1]}")
        print(f"gamma: {gamma}")
        print(f"Data dimension: {test_X.shape[0]}")
        print(f"Number of selected variables: {len(D_hat)}\n")
        
            
        train_counts = Counter(train_y)
        predictions_counts = Counter(predictions)
        
        print("\n--- Training Data Label Counts ---")
        for label, count in train_counts.items():
            print(f"Label '{label}': {count} data points")
        
        print("\n--- Predicted Test Data Label Counts ---")
        for label, count in predictions_counts.items():
            print(f"Label '{label}': {count} data points")
        
        print("")
    if option2:
        print("--- Selected Variables ---")
        print("Set option2=FALSE to hide this information.")
        print(D_hat)
        print("")
        
    return predictions