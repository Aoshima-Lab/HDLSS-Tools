import numpy as np
from sklearn.svm import SVC
from sklearn.metrics.pairwise import rbf_kernel, laplacian_kernel, polynomial_kernel, linear_kernel
from collections import Counter

class BiasCorrectedSVM:
    def __init__(
        self,
        kernel='linear',
        C=1e12,
        gamma=1,
        degree=3,
        coef0=0,
        option=False,
        auto_cv=False,
        cv=5,
        n_points=5,
        search_range=None,
        random_state=None,
        cv_params=None,
        **kwargs
    ):
        self.kernel = kernel
        self.C = C
        self.gamma = gamma
        self.degree = degree
        self.coef0 = coef0
        self.option = option
        self.auto_cv = auto_cv
        self.cv = cv
        self.n_points = n_points
        self.search_range = search_range
        self.random_state = random_state
        self.scoring = 'accuracy'
        self.cv_params = cv_params or {}
        self.kwargs = kwargs
        self.model = None
        self.bc_term_ = None
        self.unique_labels_ = None
        self.X1_ = None
        self.X2_ = None
        self.n1_ = None
        self.n2_ = None
        self._gamma_optimized = False

    def _split_by_class(self, X, y):
        labels = np.unique(y)
        if len(labels) != 2:
            raise ValueError("Only binary classification is supported.")
        self.unique_labels_ = labels
        self.X1_ = X[:, y == labels[0]]
        self.X2_ = X[:, y == labels[1]]
        self.n1_ = self.X1_.shape[1]
        self.n2_ = self.X2_.shape[1]

    def _get_kernel_func(self):
        if callable(self.kernel):
            return self.kernel
        elif self.kernel == 'linear':
            return linear_kernel
        elif self.kernel == 'rbf':
            return lambda X, Y: rbf_kernel(X, Y, gamma=self._gamma_value)
        elif self.kernel == 'laplacian':
            return lambda X, Y: laplacian_kernel(X, Y, gamma=self._gamma_value)
        elif self.kernel == 'poly':
            return lambda X, Y: polynomial_kernel(X, Y, degree=self.degree, coef0=self.coef0, gamma=self._gamma_value)
        else:
            raise ValueError("Unsupported kernel type. Use 'linear', 'rbf', 'laplacian', 'poly', or pass a callable.")

    def _estimate_gamma0(self, X=None, y=None):
        if self.kernel != 'rbf':
            raise ValueError(f"gamma='gamma_0' is only supported for rbf kernel, but got kernel='{self.kernel}'")

        if X is not None and y is not None:
            labels = np.unique(y)
            X1 = X[:, y == labels[0]]
            X2 = X[:, y == labels[1]]
        else:
            X1 = self.X1_
            X2 = self.X2_
            if X1 is None or X2 is None:
                raise RuntimeError("Specify X, y or call fit/_split_by_class first.")

        n1, n2 = X1.shape[1], X2.shape[1]
        x_bar1 = np.mean(X1, axis=1)
        x_bar2 = np.mean(X2, axis=1)
        trace_S1 = np.sum((X1 - x_bar1[:, None]) ** 2 / (n1 - 1)) if n1 > 1 else 0.0
        trace_S2 = np.sum((X2 - x_bar2[:, None]) ** 2 / (n2 - 1)) if n2 > 1 else 0.0
        Delta_star_hat = np.sum((x_bar1 - x_bar2) ** 2)
        Delta_Sigma_hat = np.abs(trace_S1 - trace_S2)

        def F(gamma):
            if gamma <= 0:
                return np.inf
            theta1 = np.exp(-Delta_star_hat / gamma)
            theta2 = np.exp(-Delta_Sigma_hat / gamma)
            numerator = 4 * theta1 * theta2
            denominator = (1 + theta2 ** 2 - 2 * theta1 * theta2)
            if abs(denominator) < 1e-12:
                return np.inf
            return (1 + numerator / denominator) / gamma

        from scipy.optimize import minimize_scalar
        result = minimize_scalar(F, bounds=(1e-6, 1e6), method='bounded')
        if not result.success or result.x <= 0:
            raise RuntimeError("minimize_scalar failed: could not find gamma_0")
        gamma_sklearn = 1.0 / result.x
        return gamma_sklearn

    def cross_validate_gamma(self, X, y, gamma, **cv_args):
        from sklearn.model_selection import StratifiedKFold
        from sklearn.metrics import accuracy_score

        if self.kernel not in ['rbf', 'laplacian']:
            raise ValueError("cross_validate_gamma is only for rbf/laplacian kernels.")

        # Use cv_args or fallback to self attributes
        cv = cv_args.get('cv', self.cv)
        n_points = cv_args.get('n_points', self.n_points)
        search_range = cv_args.get('search_range', self.search_range)
        random_state = cv_args.get('random_state', self.random_state)

        # If search_range is a tuple of (a, b), interpret as (a*gamma, b*gamma)
        if search_range is None:
            search_range = (gamma / 10, gamma * 10)
        elif isinstance(search_range, (tuple, list)) and len(search_range) == 2:
            search_range = (search_range[0] * gamma, search_range[1] * gamma)
        else:
            raise ValueError("search_range must be a tuple or list of length 2, e.g. (0.1, 10)")
        gammas = np.logspace(np.log10(search_range[0]), np.log10(search_range[1]), n_points)
        best_gamma = None
        best_score = -np.inf

        skf = StratifiedKFold(n_splits=cv, shuffle=True, random_state=random_state)
        for g in gammas:
            scores = []
            for train_idx, test_idx in skf.split(X.T, y):
                train_X, test_X = X[:, train_idx], X[:, test_idx]
                train_y, test_y = y[train_idx], y[test_idx]
                model = BiasCorrectedSVM(
                    kernel=self.kernel,
                    gamma=g,
                    C=self.C,
                    degree=self.degree,
                    coef0=self.coef0,
                    option=False,
                    auto_cv=False,  # Explicitly disable auto_cv to avoid infinite recursion
                    **self.kwargs
                )
                model.fit(train_X, train_y)
                preds = model.predict(test_X)
                # scoring is always accuracy
                score = accuracy_score(test_y, preds)
                scores.append(score)
            mean_score = np.mean(scores)
            if mean_score > best_score:
                best_score = mean_score
                best_gamma = g

        if self.option:
            print(f"CV best gamma: {best_gamma:.4g}, mean accuracy: {best_score:.4f}")
        self._gamma_optimized = True
        return best_gamma

    def bc_term(self):
        """Calculate and return the bias correction term (call after fit)"""
        if self.X1_ is None or self.X2_ is None:
            raise RuntimeError("Call fit() before bc_term().")
        kernel_func = self._get_kernel_func()
        gram1 = kernel_func(self.X1_.T, self.X1_.T)
        gram2 = kernel_func(self.X2_.T, self.X2_.T)
        gram12 = kernel_func(self.X1_.T, self.X2_.T)
        eta1 = np.sum(np.diag(gram1)) / (self.n1_ - 1) - np.sum(gram1) / (self.n1_ * (self.n1_ - 1))
        eta2 = np.sum(np.diag(gram2)) / (self.n2_ - 1) - np.sum(gram2) / (self.n2_ * (self.n2_ - 1))
        delta = eta1 / self.n1_ - eta2 / self.n2_
        capital_delta = (
            np.sum(gram1) / (self.n1_ ** 2)
            + np.sum(gram2) / (self.n2_ ** 2)
            - 2 * np.sum(gram12) / (self.n1_ * self.n2_)
        )
        bc = delta / capital_delta if abs(capital_delta) > 1e-10 else 0
        return bc

    def _resolve_gamma(self, train_X):
        n_features = train_X.shape[0]  # X: (features, samples)

        if self.gamma == 'gamma_0':
            gamma_central = self._estimate_gamma0()
        elif isinstance(self.gamma, (float, int)):
            gamma_central = float(self.gamma)
        elif self.gamma == 'auto':
            gamma_central = 1.0 / n_features
        elif self.gamma == 'scale':
            gamma_central = 1.0 / (n_features * np.var(train_X, ddof=0))
        else:
            gamma_central = self.gamma  # fallback, e.g. if callable

        # Prepare CV parameters (priority: explicit > cv_params > __init__ defaults)
        cv_args = dict(
            cv=self.cv,
            n_points=self.n_points,
            search_range=self.search_range,
            random_state=self.random_state,
            scoring=self.scoring,
        )
        cv_args.update(self.cv_params)

        # CV is only for rbf/laplacian
        if self.kernel in ['rbf', 'laplacian'] and self.auto_cv and not self._gamma_optimized:
            gamma_val = self.cross_validate_gamma(
                train_X, self._last_train_y, gamma=gamma_central, **cv_args
            )
            if self.option:
                print("auto_cv=True: Performed gamma CV with custom/default settings.")
            return gamma_val
        # Otherwise, use as is
        return gamma_central

    def fit(self, train_X, train_y):
        self._split_by_class(train_X, train_y)
        self._last_train_y = train_y  # for cross_validate_gamma
        self._gamma_value = self._resolve_gamma(train_X)
        kernel_func = self._get_kernel_func()
        self.model = SVC(kernel=kernel_func, C=self.C, **self.kwargs)
        self.model.fit(train_X.T, train_y)
        # Check if the class label order matches between SVC and unique_labels_
        assert np.array_equal(self.model.classes_, self.unique_labels_), (
            f"Label order mismatch: SVC classes {self.model.classes_} vs unique_labels_ {self.unique_labels_}")
        self.bc_term_ = self.bc_term()
        if self.option:
            print("BC_SVM fit called. Set option=False to hide this information.")
            print(f"Training data size: {len(train_y)}")
            print(f"Data dimension: {train_X.shape[0]}\n")
            train_counts = Counter(train_y)
            print("--- Training Data Label Counts ---")
            for label, count in train_counts.items():
                print(f"Label '{label}': {count} data points")
            print("")

    def score(self, test_X):
        """Return bias-corrected decision score"""
        if self.model is None or self.bc_term_ is None:
            raise RuntimeError("Call fit() before score().")
        pred_score = self.model.decision_function(test_X.T)
        return pred_score - self.bc_term_

    def predict(self, test_X):
        """Return predicted labels using the score function"""
        if self.unique_labels_ is None:
            raise RuntimeError("Call fit() before predict().")
        score = self.score(test_X)
        label1, label2 = self.unique_labels_
        predictions = np.where(score < 0, label1, label2)
        if self.option:
            print(f"Test data size: {test_X.shape[1]}")
            predictions_counts = Counter(predictions)
            print("--- Predicted Test Data Label Counts ---")
            for label, count in predictions_counts.items():
                print(f"Label '{label}': {count} data points")
            print("")
        return predictions

    @property
    def gamma_value(self):
        """Return the gamma value actually used after fit"""
        return self._gamma_value

    @property
    def bc_term_value(self):
        """Return the bias correction term actually used after fit"""
        return self.bc_term_

    @property
    def class_labels(self):
        """Return the class labels used after fit"""
        return self.unique_labels_