# **Bias-Corrected Support Vector Machine (Python version)**

## Table of Contents

- [**Bias-Corrected Support Vector Machine (Python version)**](#bias-corrected-support-vector-machine-python-version)
  - [Table of Contents](#table-of-contents)
  - [Usage](#usage)
    - [Basic Example](#basic-example)
  - [Class API](#class-api)
    - [Main Arguments](#main-arguments)
    - [Methods \& Properties](#methods--properties)
    - [Output](#output)
  - [Notes](#notes)
      - [Basic Output Example](#basic-output-example)
      - [About `gamma` parameter](#about-gamma-parameter)
  - [Cross-Validation for gamma (`auto_cv`)](#cross-validation-for-gamma-auto_cv)
    - [Main keys for `cv_params`](#main-keys-for-cv_params)
      - [Example: How to use `cv_params`](#example-how-to-use-cv_params)
      - [Example: gamma search behavior](#example-gamma-search-behavior)
  - [License](#license)

This directory provides the Python implementation of the Bias-Corrected Support Vector Machine (BC-SVM) for high-dimensional, low-sample-size (HDLSS) data.

---

## Usage

> **Note:**  
> This implementation uses `sklearn.svm.SVC` for SVM training.  
> Data format: **(features, samples)** (rows: features, columns: samples)


### Basic Example

```python
from BC_SVM import BiasCorrectedSVM

# X: (features, samples), y: label vector (length = number of samples, 2 classes)
# gamma can be a float, 'auto', 'scale', or 'gamma_0'
# (Note: 'gamma_0' is only valid for rbf kernel)
bcsvm = BiasCorrectedSVM(kernel='rbf', gamma='gamma_0')
bcsvm.fit(X, y)
pred = bcsvm.predict(X_test)
score = bcsvm.score(X_test)
```

---

## Class API


```python
class BiasCorrectedSVM:
    def __init__(self, kernel='linear', C=1e12, gamma=1, degree=3, coef0=0, option=False, auto_cv=False, cv=5, n_points=5, search_range=None, random_state=None, cv_params=None, **kwargs):
        ...
    def fit(self, train_X, train_y):
        ...
    def predict(self, test_X):
        ...
    def score(self, test_X):
        ...
    def cross_validate_gamma(self, X, y, gamma, **cv_args):
        ...
    @property
    def gamma_value(self):
        ...
    @property
    def bc_term_value(self):
        ...
    @property
    def class_labels(self):
        ...
```

### Main Arguments

| Argument     | Description                                                                                 |
|--------------|--------------------------------------------------------------------------------------------|
| `kernel`     | 'linear', 'rbf', 'poly', 'laplacian', or any sklearn-compatible callable kernel function (e.g. `linear_kernel`, `rbf_kernel`, or your own custom pairwise kernel function)                        |
| `C`          | SVM regularization parameter (default: 1e12)                                               |
| `gamma`      | Kernel parameter for 'rbf' and 'laplacian' (**default: 1**). Accepts:<br> - float/int: direct value (e.g. 0.1)<br> - `'auto'`: 1 / n_features (same as sklearn)<br> - `'scale'`: 1 / (n_features * var(X)) (same as sklearn)<br> - `'gamma_0'`: data-driven value based on Nakayama et al. (2020) (only for 'rbf')<br> If `auto_cv=True`, the initial value is used as the center for CV search. |
| `degree`     | Degree for 'poly' kernel (default: 3)                                                      |
| `coef0`      | Offset for 'poly' kernel (default: 0)                                                      |
| `option`     | If True, print detailed info                                                               |
| `auto_cv`    | If True, perform cross-validation for gamma (rbf/laplacian only). [See details below](#cross-validation-for-gamma-auto_cv).  |
| `cv`         | Number of folds for cross-validation (default: 5)                                          |
| `n_points`   | Number of gamma values to search in CV (default: 5)                                        |
| `search_range`| Tuple (a, b): search gamma in [a × gamma, b × gamma] (default: (0.1, 10))                     |
| `random_state`| Random seed for CV split (default: None)                                                  |
| `cv_params`  | Dictionary for flexible CV parameter passing (overrides above if set)                      |
| `**kwargs`   | Additional keyword arguments for sklearn SVC (e.g. tol=1e-10)                              |

### Methods & Properties

- `fit(train_X, train_y)`: Train the model
- `predict(test_X)`: Predict class labels
- `score(test_X)`: Return bias-corrected decision scores
- `gamma_value`: Gamma value actually used after fit
- `bc_term_value`: Bias correction term after fit
- `class_labels`: Class labels after fit

### Output
- `predict` returns: numpy array of predicted labels
- `score` returns: numpy array of bias-corrected decision scores

---

## Notes
- Input data must be numpy arrays with shape (features, samples) and dtype float32 or float64.
- Label vector (`train_y`) must be a 1D array of length = number of samples, with exactly 2 unique values (binary classification only).
- If you specify an unsupported kernel or gamma (e.g. `gamma='gamma_0'` with `kernel='poly'`), a ValueError will be raised.
- For details on gamma/auto_cv options and advanced usage, see the source code and examples.

#### Basic Output Example
```python
print(pred.shape)  # (number of test samples,)
print(score.shape) # (number of test samples,)
print(pred[:5])    # e.g. array([0, 1, 1, 0, 0])
```


#### About `gamma` parameter
- **Default:** `1`
- `'auto'` and `'scale'` follow scikit-learn's SVC definition.
- `'gamma_0'` computes gamma based on the data, following the formula in Nakayama et al. (2020). Only available for `'rbf'` kernel. If used with other kernels, an error is raised.
- You can also pass a numeric value (float/int) for custom gamma.




## Cross-Validation for gamma (`auto_cv`)


If `auto_cv=True` and the kernel is `'rbf'` or `'laplacian'`, the gamma parameter is automatically optimized by cross-validation (CV).

- The initial gamma (numeric or string) is used as the center of the search range (default: [0.1 × gamma, 10 × gamma], log scale).
- The search range is divided into `n_points` values (default: 5), and CV is performed for each value.
- The gamma with the highest mean accuracy is automatically selected.
- All CV settings can be flexibly overridden via the `cv_params` dictionary.

### Main keys for `cv_params`

| Key           | Description / Default value                      |
|---------------|-------------------------------------------------|
| `cv`          | Number of folds (int, default: 5)               |
| `n_points`    | Number of gamma values to search (int, default: 5) |
| `search_range`| Search range (a, b): [a × gamma, b × gamma]         |
| `random_state`| Random seed for CV split (default: None)        |


*If a key is specified in both the constructor and `cv_params`, the value in `cv_params` takes precedence. All of the above parameters can be overridden by passing a dictionary to `cv_params`.*

*Scoring is always fixed to 'accuracy'. Stratified (class-balanced, shuffled) CV is always used.*

#### Example: How to use `cv_params`
```python
bcsvm = BiasCorrectedSVM(kernel='rbf', gamma=1, auto_cv=True, cv_params={'n_points': 7, 'search_range': (0.2, 5), 'cv': 3})
```
→ This searches 7 gamma values in [0.2 × gamma, 5 × gamma] (log scale), using 3-fold CV.

#### Example: gamma search behavior

- `gamma=1`, `auto_cv=True`: `[0.1, 0.316, 1.0, 3.16, 10.0]` (5 points, default range: [0.1 × gamma, 10 × gamma])
- `gamma=2`, `auto_cv=True`, `search_range=(0.5, 4)`: `[1.0, 1.682, 2.828, 4.756, 8.0]` (5 points, custom range: [0.5 × gamma, 4 × gamma])

You can flexibly control the search range and number of points using `search_range` and `n_points` (or via `cv_params`).

---

## License
See LICENSE file for details.
