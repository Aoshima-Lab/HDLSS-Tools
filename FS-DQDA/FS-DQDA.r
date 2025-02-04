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


FS_DQDA <- function(train_X, train_y, test_X, gamma = 0.5, option1 = FALSE, option2 = FALSE) {

  test_X <- as.matrix(test_X)
  tests_num <- ncol(test_X)
  unique_labels <- unique(train_y)
  num_classes <- length(unique_labels)
  dim <- nrow(train_X)

  class_scores <- list()
  diags <- list()
  means <- list()
  nums <- list()
  

  for (label in unique_labels) {
    data_in_class <- train_X[, train_y == label, drop = FALSE]
    num_data_in_class <- ncol(data_in_class)

    if (num_data_in_class <= 1) {
      stop("Each class must have more than one training data")
    }

    mean_in_class <- rowMeans(data_in_class)
    diag_in_class <- rowSums((data_in_class - mean_in_class)^2) / (num_data_in_class - 1)

    diags[[as.character(label)]] <- diag_in_class
    means[[as.character(label)]] <- mean_in_class
    nums[[as.character(label)]] <- num_data_in_class
  }

  min_num <- min(unlist(nums))
  theta <- -1

  for (label_i in unique_labels) {
    for (label_j in unique_labels) {
      if (label_i != label_j) {
        mean_diff <- (means[[as.character(label_i)]] - means[[as.character(label_j)]])^2
        theta <- theta + (mean_diff + diags[[as.character(label_i)]]) / (num_classes * (num_classes - 1) * diags[[as.character(label_j)]])
      }
    }
  }

  condition <- theta > (log(dim) / min_num)^(gamma / 2)
  D_hat <- which(condition)

  # Prediction
  for (label in unique_labels) {
    diags_label <- diags[[as.character(label)]][D_hat]
    means_label <- means[[as.character(label)]][D_hat]
    label_mean_selected <- matrix(means[[as.character(label)]][D_hat])
    label_mean_selected <- matrix(label_mean_selected, nrow = length(label_mean_selected), ncol = tests_num, byrow = FALSE)
    FS_W <- colSums(((test_X[D_hat, ] - label_mean_selected)^2 / diags[[as.character(label)]][D_hat]) -1 / nums[[as.character(label)]] +log(diags[[as.character(label)]][D_hat]))
    class_scores[[as.character(label)]] <- FS_W
  }

  predictions <- sapply(1:tests_num, function(i) {
    which.min(sapply(class_scores, function(scores) scores[i]))
  })

  if (option1) {
    cat("FS_DQDA function called. Set option1=FALSE to hide this information.\n")
    cat("Training data size:", length(train_y), "\n")
    cat("Test data size:", ncol(test_X), "\n")
    cat("gamma:", gamma, "\n")
    cat("Data dimension:", nrow(test_X), "\n")
    cat("Number of selected variables:", length(D_hat), "\n\n")

    train_counts <- table(train_y)
    predictions_counts <- table(predictions)

   cat("\n--- Training Data Label Counts ---\n")
   for (label in names(train_counts)) {
    cat("Label '", label, "': ", train_counts[label], " data points\n", sep="")
}

    cat("\n--- Predicted Test Data Label Counts ---\n")
    for (label in names(predictions_counts)) {
    cat("Label '", label, "': ", predictions_counts[label], " data points\n", sep="")
}
    cat("\n\n")
  }
  if (option2) {
    cat("--- Selected Variables ---\n")
    cat("Set option2=FALSE to hide this information.\n")
    cat(D_hat,"\n\n")
  }

  return(predictions)
}