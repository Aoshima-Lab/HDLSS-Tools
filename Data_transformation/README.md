# Data Transformation

[[R](data_transform.R)] [[Python](data_transform.py)]

This module provides a data transformation methodology and estimates the number of strongly spiked eigenvalues for high-dimensional, low-sample-size (HDLSS) data.

## Contents

- [Functions](#functions)
- [R](#r)
- [Python](#python)
- [Reference](#reference)

## Functions

### `check_sse`
Estimates the number of strongly spiked eigenvalues using the cross-data matrix methodology.

### `NRM_trans`
Performs a data transformation based on the noise-reduction methodology.

---

### R

**Quick start (R)**

> **Note:** `X` is a matrix with dimensions d × n (d features, n samples).

```r
# Function signatures (illustrative)
check_sse(X, centering = FALSE, random = FALSE, seed = NULL)
NRM_trans(X, centering = FALSE, sse_point = NULL, random = FALSE, seed = NULL)
```

**Arguments**

- `X`: d × n numeric matrix (d features, n samples)
- `centering`: logical, whether to center the data before further processing (default: FALSE)
- `random`: logical, whether to use a randomized split for the cross-data-matrix procedure (default: FALSE). If FALSE, the data is split into first and second halves
- `seed`: integer or NULL, random seed used when `random = TRUE` to ensure reproducibility
- `sse_point`: integer or NULL, number of strongly spiked eigenvalues (if NULL, estimated by `check_sse`)

**Returns**

- `check_sse`: integer — estimated number of spikes
- `NRM_trans`: list with elements
  - `X_trans`: matrix, transformed data (k × n)
  - `nrmvec`: matrix, eigenvectors estimated by the noise-reduction method (d × k)

**Example (minimal):**

```r
source("data_transform.R")

# X: d by n matrix
# Let NRM_trans estimate the spike count automatically
nrm_result <- NRM_trans(X)

# If you prefer to supply the estimated k explicitly:
# k <- check_sse(X)
# nrm_result <- NRM_trans(X, sse_point = k)

X_trans <- nrm_result$X_trans
nrmvec <- nrm_result$nrmvec
```

---

### Python

**Quick start (Python)**

> **Note:** `X` is a NumPy array with shape (d, n) — d features × n samples.

```python
# Function signatures (illustrative)
def check_sse(X, centering=False, random=False, seed=None) -> int: ...
def NRM_trans(X, centering=False, sse_point=None, random=False, seed=None) -> dict: ...
```

**Arguments**

- `X` : numpy.ndarray with shape (d, n)
- `centering` : bool, whether to center the data before further processing (default: False)
- `random` : bool, whether to use a randomized split for the cross-data-matrix procedure (default: False). If False, the data is split into first and second halves
- `seed` : int or None, random seed used when `random = True` to ensure reproducibility
- `sse_point` : int or None, number of strongly spiked eigenvalues (if None, estimated by `check_sse`)

**Returns**

- `check_sse` -> int : estimated number of spikes
- `NRM_trans` -> dict with keys
  - `'X_trans'` : ndarray, transformed data with shape (k, n)
  - `'nrmvec'` : ndarray, eigenvectors estimated by the noise-reduction method with shape (d, k)

**Example (minimal):**

```python
from data_transform import check_sse, NRM_trans
import numpy as np

# X: numpy array with shape (d, n)
# Let NRM_trans estimate the spike count automatically
nrm_result = NRM_trans(X)

# If you prefer to supply the estimated k explicitly:
# k = check_sse(X)
# nrm_result = NRM_trans(X, sse_point=k)

X_trans = nrm_result['X_trans']
nrmvec = nrm_result['nrmvec']
```

---

## Reference
>   Reference : M. Aoshima, K. Yata, Two-Sample Tests for High-Dimension, Strongly Spiked Eigenvalue Models, Statistica Sinica, 28 (2018), 43-62  
  DOI: [[10.5705/ss.202016.0063](https://doi.org/10.5705/ss.202016.0063)]