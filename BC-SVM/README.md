# **Bias-Corrected Support Vector Machine**

The **Bias-Corrected Support Vector Machine (BC-SVM)** is designed to adjust the bias in SVM classifiers, especially for high-dimensional, low-sample-size data. The method is based on the following references:

- Y. Nakayama, K. Yata, and M. Aoshima, Support vector machine and its bias correction in high-dimension, low-sample-size settings, Journal of Statistical Planning and Inference, 191 (2017) 88–100.  
  DOI: [10.1016/j.jspi.2017.05.005](https://doi.org/10.1016/j.jspi.2017.05.005)
- Y. Nakayama, K. Yata, and M. Aoshima, Bias-corrected support vector machine with Gaussian kernel in high-dimension, low-sample-size settings, Annals of the Institute of Statistical Mathematics, 72 (2020) 1257–1286.  
  DOI: [10.1007/s10463-019-00727-1](https://link.springer.com/article/10.1007/s10463-019-00727-1)

---

## Quick Start (Python)

> **Note:**  
> This implementation uses `sklearn.svm.SVC` for SVM training.  
> For details and advanced usage, see [python/README.md](python/README.md).

```python
from BC_SVM import BiasCorrectedSVM

# X: (features, samples), y: label vector (length = number of samples, 2 classes)
bcsvm = BiasCorrectedSVM(kernel='rbf', gamma='gamma_0')
bcsvm.fit(X, y)
pred = bcsvm.predict(X_test)
```

---

## Directory Structure

- `python/` : Python implementation and detailed manual
- `R/`      : R implementation (planned)
---

For detailed usage, arguments, and advanced options, please see the README in each language's directory.