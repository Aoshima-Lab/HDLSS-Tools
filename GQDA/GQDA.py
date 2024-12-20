import numpy as np
from collections import Counter
#######################################################################################
# INPUT: GQDA(train_X, train_y, test_X, option)
# train_X: p × n (=n_1+...+n_k) training data matrix where p is the dimension, k is the number of classes, n is the total sample size and n_i is the size of the i-th class in training data.
# train_y: n dimensional vector where n is the size of training data. The order of the label vector should correspond to training data matrix.
# test_X: p × N testing data matrix, where p is the dimension and N is the sample size of testing data.
# option: Boolean value (default: False). 
#         If True, displays detailed information about the training and testing data, 
#         including the number of samples, data dimensions, and label distributions 
#         in both training data and predictions. Useful for debugging and analysis.

# OUTPUT
#predictions: Estimated labels based on GQDA.
#######################################################################################

def GQDA(train_X, train_y, test_X, option = False):
    data_dim = train_X.shape[0]
    
    unique_labels = np.unique(train_y)
    class_scores = []
    
    for label in unique_labels:
      data_in_class = train_X[:, train_y == label]
      num_data_in_class = data_in_class.shape[1]
      mean_in_class = np.mean(data_in_class, axis=1).reshape(-1, 1)
    
      if num_data_in_class <= 1:
          raise ValueError("Each class must have more than one training data")
    
      trace_cov_matrix = np.sum((data_in_class - mean_in_class)**2) / (num_data_in_class - 1)
      score = data_dim * np.sum((test_X - mean_in_class)**2, axis=0)/trace_cov_matrix + data_dim * np.log(trace_cov_matrix) - data_dim / num_data_in_class
      class_scores.append(score)

    predictions = unique_labels[np.argmin(class_scores, axis=0)]

    if option:
        print("GQDA function called. Set option=False to hide this information.")
        print(f"Training data size: {len(train_y)}")
        print(f"Test data size: {test_X.shape[1]}")
        print(f"Data dimension: {test_X.shape[0]}\n")
        
        
        train_counts = Counter(train_y)
        predictions_counts = Counter(predictions)
        
        print("--- Training Data Label Counts ---")
        for label, count in train_counts.items():
            print(f"Label '{label}': {count} data points")
        
        print("\n--- Predicted Test Data Label Counts ---")
        for label, count in predictions_counts.items():
            print(f"Label '{label}': {count} data points")
            
        print("")
            
    return predictions