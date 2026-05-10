"""Utilities for Systems Design Coursework Simulation."""

import numpy as np
from numpy import typing as npt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline


def rstool(X: npt.ArrayLike, y: npt.ArrayLike, X_test: npt.ArrayLike) -> np.ndarray:
    """
    Predict response surface contours.

    This function uses ordinary least squares regression to find the effect of input independent variables on a dependent output variable.
    It creates a polynomial design matrix from the input training features, and fits a linear regression to that matrix. This creates a quatratic fit.
    """
    model = make_pipeline(
        PolynomialFeatures(degree=2, include_bias=False), LinearRegression()
    )

    model = model.fit(X, y)
    return model.predict([X_test])
