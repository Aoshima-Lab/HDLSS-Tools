# Tools for HDLSS data <!-- omit in toc -->
Our laboratory provides [**[Tools](#tools)**] for **high-dimension, low-sample-size (HDLSS) data**.
 Please read [**[License](#license)**] and use tools only if you agree. For more details on the analytical method, please refer to relevant manuals and papers.

# Contents <!-- omit in toc -->
- [Package Installation](#package-installation)
- [Tools](#tools)
  - [Principal Component Analysis](#principal-component-analysis)
    - [**Noise-Reduction Methodology**](#noise-reduction-methodology)
    - [**Cross-Data-Matrix Methodology**](#cross-data-matrix-methodology)
    - [**Automatic Sparse PCA**](#automatic-sparse-pca)
  - [Correlation Test](#correlation-test)
    - [**Extended Cross-Data-Matrix Methodology**](#extended-cross-data-matrix-methodology)
  - [Sparse Estimation](#sparse-estimation)
    - [**Automatic Sparse Estimation**](#automatic-sparse-estimation)
  - [Outlier Detection](#outlier-detection)
    - [**PC-scores-based Outlier Detection**](#pc-scores-based-outlier-detection)
  - [Discriminant Analysis](#discriminant-analysis)
    - [**Bias-Corrected Support Vector Machine**](#bias-corrected-support-vector-machine)
    - [**Distance-Based Discriminant Analysis**](#distance-based-discriminant-analysis)
    - [**Geometrical quadratic discriminant analysis**](#geometrical-quadratic-discriminant-analysis)
  - [Data Transformation](#data-transformation)
    - [**Data Transformation**](#data-transformation-1)
  - [Clustering](#clustering)
  - [Covariance Structures Test](#covariance-structures-test)
- [License](#license)

# Package Installation
### From GitHub<!-- omit in toc -->
Use the following command in the terminal to install packages locally.
```console
git clone https://github.com/Aoshima-Lab/HDLSS-Tools.git
```

# Tools
## Principal Component Analysis
### **[Noise-Reduction Methodology](NRM/)**
   [[R](NRM/NRM.r)] [[Python](NRM/NRM.py)] [[Manual](NRM/NRM.pdf)]

   The "Noise-Reduction Methodology (NRM)" gives estimators of the eigenvalues, eigenvectors, and principal component scores.

   >   Reference : K. Yata, M. Aoshima, Effective PCA for High-Dimension, Low-Sample-Size Data with Noise Reduction via Geometric Representations, Journal of Multivariate Analysis, 105 (2012) 193-215.  
      DOI: [[10.1016/j.jmva.2011.09.002](https://www.sciencedirect.com/science/article/pii/S0047259X11001904)]

### **[Cross-Data-Matrix Methodology](CDM/)**
   [[R](CDM/CDM.r)] [[Python](CDM/CDM.py)] [[Manual](CDM/CDM.pdf)]

   The "Cross-Data-Matrix (CDM) Methodology" gives estimators of the eigenvalues, eigenvectors, and principal component scores.

   >   Reference : K. Yata, M. Aoshima, Effective PCA for High-Dimension, Low-Sample-Size Data with Singular Value Decomposition of Cross Data Matrix, Journal of Multivariate Analysis, 101 (2010) 2060-2077.  
      DOI: [[10.1016/j.jmva.2010.04.006](https://www.sciencedirect.com/science/article/pii/S0047259X10000904)]

### **[Automatic Sparse PCA](A-SPCA/)**
   [[R](A-SPCA/ASPCA.r)] [[Python](A-SPCA/ASPCA.py)] [[Manual](A-SPCA/ASPCA.pdf)]

   The "Automatic Sparse PCA (A-SPCA)" gives estimators of the eigenvalues and eigenvectors.

   >  Reference : K. Yata, M. Aoshima, Automatic Sparse PCA for High-Dimensional Data, Statistica Sinica, 35 (2025) 1069-1090.
      DOI: [[10.5705/ss.202022.0319](https://www3.stat.sinica.edu.tw/ss_newpaper/SS-2022-0319_na.pdf)] [[Supplement](https://www3.stat.sinica.edu.tw/preprint/supp/2022-0319_supp.pdf)]

## Correlation Test
### **[Extended Cross-Data-Matrix Methodology](ECDM/)**
   [[R](ECDM/ECDM.r)] [[Python](ECDM/ECDM.py)] [[Manual](ECDM/ECDM.pdf)]

   The "Extended Cross-Data-Matrix (ECDM) Methodology" gives an estimator of $\mathrm{Tr}(\Sigma^2)$, where $\Sigma$ is a  covariance matrix. This code tests the correlation coefficient matrix by the ECDM estimator.

   >   Reference : K. Yata, M. Aoshima, High-Dimensional Inference on Covariance Structures via the Extended Cross-Data-Matrix Methodology, Journal of Multivariate Analysis, 151 (2016) 151-166.  
      DOI: [[10.1016/j.jmva.2016.07.011](https://www.sciencedirect.com/science/article/pii/S0047259X16300550)]

## Sparse Estimation
### **[Automatic Sparse Estimation](Automatic-Sparse-Estimation/)**
   [[R](Automatic-Sparse-Estimation/Automatic_sparse_estimation.r)] [[Python](Automatic-Sparse-Estimation/Automatic_sparse_estimation.py)] [[Manual](Automatic-Sparse-Estimation/README.md)]

   The "Automatic Sparse Estimation" provides sparse estimators of cross-covariance matrices and mean vectors. This method automatically determines the sparsification threshold.

   >   Reference : T. Umino, K. Yata and M. Aoshima, Automatic sparse estimation of the high-dimensional cross-covariance matrix, Journal of Multivariate Analysis, (2025) (in press).  
      DOI: [[10.1016/j.jmva.2025.105590](https://doi.org/10.1016/j.jmva.2025.105590)]

## Outlier Detection
### **[PC-scores-based Outlier Detection](PC-OD/)**
   [[R](PC-OD/PC_OD.r)] [[Python](PC-OD/PC_OD.py)] [[Manual](PC-OD/PC_OD.pdf)]

   The "PC-scores-based Outlier Detection (PC-OD)" identifies outliers based on the PC scores. The algorithm is provided in section 3.2 of Nakayama et al. (2024).

   >   Reference : Y. Nakayama, K. Yata and M. Aoshima, Test for High-Dimensional Outliers with Principal Component Analysis, Japanese Journal of Statistics and Data Science, 7 (2024) 739–766.  
    DOI : [[10.1007/s42081-024-00255-0](https://link.springer.com/article/10.1007/s42081-024-00255-0)]

## Discriminant Analysis

### **[Bias-Corrected Support Vector Machine](BC-SVM/)**
   [[Python](BC-SVM/python/BC_SVM.py)] [[Manual](BC-SVM/BC_SVM.pdf)]

   The "Bias-Corrected Support Vector Machine (BC-SVM)" provides bias-corrected classification for high-dimensional, low-sample-size data. The algorithm is described in the following references:

   >   Reference : Y. Nakayama, K. Yata, and M. Aoshima, Support vector machine and its bias correction in high-dimension, low-sample-size settings, Journal of Statistical Planning and Inference, 191 (2017) 88–100.  
   >   DOI: [[10.1016/j.jspi.2017.05.005](https://doi.org/10.1016/j.jspi.2017.05.005)]
   >
   >   Y. Nakayama, K. Yata, and M. Aoshima, Bias-corrected support vector machine with Gaussian kernel in high-dimension, low-sample-size settings, Annals of the Institute of Statistical Mathematics, 72 (2020) 1257–1286.  
   >   DOI: [[10.1007/s10463-019-00727-1](https://link.springer.com/article/10.1007/s10463-019-00727-1)]

### **[Distance-Based Discriminant Analysis](DBDA/)**
   [[R](DBDA/DBDA.r)] [[Python](DBDA/DBDA.py)] [[Manual](DBDA/DBDA.pdf)]

   The "Distance-Based Discriminant Analysis (DBDA)" provides high-dimensional discriminant analysis for multiclass data. The algorithm is provided in Aoshima and Yata (2014).

   >   Reference : M. Aoshima and K. Yata, A distance-based, misclassification rate adjusted classifier for multiclass, high-dimensional data, Annals of the Institute of Statistical Mathematics (2014).  
    DOI : [[10.1007/s10463-013-0435-8](https://link.springer.com/article/10.1007/s10463-013-0435-8)]

### **[Geometrical quadratic discriminant analysis](GQDA/)**
   [[R](GQDA/GQDA.R)] [[Python](GQDA/GQDA.py)] [[Manual](GQDA/GQDA.pdf)]
   
   The "Geometrical quadratic discriminant analysis(GQDA)" provides high-dimensional discriminant analysis for multiclass data. The algorithm is provided in Aoshima and Yata (2015).
   >   Reference : M. Aoshima and K. Yata, Geometric Classifier for Multiclass, High-Dimensional Data, Sequential Anal, 34, 279-294. (2015).  
    DOI : [[10.1080/07474946.2015.1063256](https://www.tandfonline.com/doi/full/10.1080/07474946.2015.1063256)]

## Data Transformation

### **[Data Transformation](Data_transformation/)**
[[R](Data_transformation/data_transform.R)] [[Python](Data_transformation/data_transform.py)] [[Manual](Data_transformation/data_transform.pdf)]

The "Data Transformation" method provides tools for transforming high-dimensional data and estimating the spiked eigenvalues in HDLSS settings.
The algorithm is provided in Aoshima and Yata (2018).

>   Reference : M. Aoshima, K. Yata, Two-Sample Tests for High-Dimension, Strongly Spiked Eigenvalue Models, Statistica Sinica, 28 (2018), 43-62  
    DOI: [[10.5705/ss.202016.0063](https://doi.org/10.5705/ss.202016.0063)]

## Clustering

## Covariance Structures Test


# License
```
Copyright (C) <2025> <Makoto Aoshima>

This work is licensed under the Creative Commons Attribution-NoDerivatives 4.0 International license.
To view a copy of this license, visit https://creativecommons.org/licenses/by-nd/4.0/ or
send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

Makoto Aoshima, University of Tsukuba
aoshima@math.tsukuba.ac.jp
https://www.math.tsukuba.ac.jp/~aoshima-lab/index.html
```