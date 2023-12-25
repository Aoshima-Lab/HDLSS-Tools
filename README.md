# Tools for HDLSS data <!-- omit in toc -->
We have published [**[R-code and manuals](#r-tools)**] for an analytical method developed and proposed in our laboratory for **High-Dimension, Low-Sample-Size (HDLSS) data**. Please read the following notes on usage and use it only if you agree. For more details on the analytical method, please refer to the relevant paper.

# Contents <!-- omit in toc -->
- [Instruction](#instruction)
- [R-Tools](#r-tools)
  - [Principal Component Analysis](#principal-component-analysis)
    - [**Noise-Reduction Methodology**](#noise-reduction-methodology)
    - [**Cross-Data-Matrix Methodology**](#cross-data-matrix-methodology)
    - [**Automatic Sparse PCA**](#automatic-sparse-pca)
  - [Correlation Test](#correlation-test)
    - [**Extended Cross-Data-Matrix Methodology**](#extended-cross-data-matrix-methodology)
  - [Clustering](#clustering)
  - [Covariance Structures Test](#covariance-structures-test)
- [License](#license)

# Instruction
1. Prior to using this R-code, install the statistical software "R". Please refer to [[HERE](https://www.r-project.org/)] on the installation of "R".
1. Click each method name in the "[[R-Tools](#r-tools)]" section above.

## Installation<!-- omit in toc -->
### From GitHub<!-- omit in toc -->
Use the following command in the terminal to install the package locally.
```console
git clone https://github.com/Aoshima-Lab/HDLSS-Tools.git
```

# R-Tools
## Principal Component Analysis
### **[Noise-Reduction Methodology](NRM/)**
   [[R-code](NRM/NRM.r)] [[Manual](NRM/NRM.pdf)]

   The "Noise-Reduction Methodology (NRM)" gives estimators of the eigenvalues, eigenvectors, and principal component scores.

   >   Reference : K. Yata, M. Aoshima, Effective PCA for High-Dimension, Low-Sample-Size Data with Noise Reduction via Geometric Representations, Journal of Multivariate Analysis, 105 (2012) 193-215.  
      DOI: [[10.1016/j.jmva.2011.09.002](https://www.sciencedirect.com/science/article/pii/S0047259X11001904)]

### **[Cross-Data-Matrix Methodology](CDM/)**
   [[R-code](CDM/CDM.r)] [[Manual](CDM/CDM.pdf)]

   The "Cross-Data-Matrix (CDM) Methodology" gives estimators of the eigenvalues, eigenvectors, and principal component scores.

   >   Reference : K. Yata, M. Aoshima, Effective PCA for High-Dimension, Low-Sample-Size Data with Singular Value Decomposition of Cross Data Matrix, Journal of Multivariate Analysis, 101 (2010) 2060-2077.  
      DOI: [[10.1016/j.jmva.2010.04.006](https://www.sciencedirect.com/science/article/pii/S0047259X10000904)]

### **[Automatic Sparse PCA](A-SPCA/)**
   [[R-code](A-SPCA/ASPCA.r)] [[Manual](A-SPCA/ASPCA.pdf)]

   The "Automatic Sparse PCA (A-SPCA)" gives estimators of the eigenvalues and eigenvectors.

   >  Reference : K. Yata, M. Aoshima, Automatic Sparse PCA for High-Dimensional Data, Statistica Sinica 35 (2025) (in press).  
      DOI: [[10.5705/ss.202022.0319](https://www3.stat.sinica.edu.tw/ss_newpaper/SS-2022-0319_na.pdf)] [[Supplement](https://www3.stat.sinica.edu.tw/preprint/supp/2022-0319_supp.pdf)]

## Correlation Test
### **[Extended Cross-Data-Matrix Methodology](ECDM/)**
   [[R-code](ECDM/ECDM.r)] [[Manual](ECDM/ECDM.pdf)]

   The "Extended Cross-Data-Matrix (ECDM) Methodology" gives an estimator of $\mathrm{Tr}(\Sigma^2)$, where $\Sigma$ is a  covariance matrix. This code tests the correlation coefficient matrix by the ECDM estimator.

   >   Reference : K. Yata, M. Aoshima, High-Dimensional Inference on Covariance Structures via the Extended Cross-Data-Matrix Methodology, Journal of Multivariate Analysis, 151 (2016) 151-166.  
      DOI: [[10.1016/j.jmva.2016.07.011](https://www.sciencedirect.com/science/article/pii/S0047259X16300550)]

## Clustering

## Covariance Structures Test

# License
```
Copyright (C) <2023> <Makoto Aoshima>

This work is licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International license.
To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-nd/4.0/ or
send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

Makoto Aoshima, University of Tsukuba
aoshima@math.tsukuba.ac.jp
https://www.math.tsukuba.ac.jp/~aoshima-lab/index.html
```
