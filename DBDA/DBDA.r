#######################################################################################
# INPUT: DBDA(train_X, train_y, test_X, option)
# train_X: p × n (=n_1+...+n_k) training data matrix where p is the dimension, k is the number of classes, n is the total sample size and n_i is the size of the i-th class in training data.
# train_y: n dimensional vector where n is the size of training data. The order of the label vector should correspond to training data matrix.
# test_X: p × N testing data matrix, where p is the dimension and N is the sample size of testing data.
# option: Boolean value (default: FALSE). 
#         If TRUE, displays detailed information about the training and testing data, 
#         including the number of samples, data dimensions, and label distributions 
#         in both training data and predictions. Useful for debugging and analysis.

# OUTPUT
#predictions: Estimated labels based on DBDA.
#######################################################################################

DBDA <- function(train_X, train_y, test_X, option=FALSE){
  test_X <- as.matrix(test_X)
  test_num <- dim(test_X)[2]
  unique_labels <- unique(train_y)
  num_classes <- length(unique_labels)
  class_scores <- matrix(0, test_num, num_classes)

  for (k in 1:num_classes){
    label <- unique_labels[k]
    data_in_class <- train_X[, train_y == label]
    num_data_in_class <- dim(data_in_class)[2]
    mean_in_class <- rowMeans(data_in_class)
    trace_cov_matrix <- sum((data_in_class - mean_in_class)^2) / (num_data_in_class - 1)
    score <- colSums((test_X - mean_in_class)^2) - trace_cov_matrix / num_data_in_class
    class_scores[,k] <- score
  }
  predictions <- unique_labels[apply(class_scores, 1, which.min)]

  if (option) {
  cat("DBDA function called. Set option=FALSE to hide this information.\n")
  cat(sprintf("Training data size: %d\n", length(train_y)))
  cat(sprintf("Test data size: %d\n", ncol(test_X)))
  cat(sprintf("Data dimension: %d\n\n", nrow(test_X)))
  
  train_counts <- table(train_y)
  predictions_counts <- table(predictions)
  
  cat("--- Training Data Label Counts ---\n")
  for (label in names(train_counts)) {
    cat(sprintf("Label '%s': %d data points\n", label, train_counts[[label]]))
  }
  
  cat("\n--- Predicted Test Data Label Counts ---\n")
  for (label in names(predictions_counts)) {
    cat(sprintf("Label '%s': %d data points\n", label, predictions_counts[[label]]))
  }
  
  cat("\n")
}
  return(predictions)
}