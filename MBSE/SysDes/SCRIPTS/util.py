"""Utilities for Systems Design Coursework Simulation."""

import numpy as np
from numpy import typing as npt
from scipy import simpson
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


def ms2kt(V_ms: float) -> float:
    """Convert a speed in metres per second to knots."""
    return (900 * V_ms) / 463


def volumeOfDisplacement(
    T: float, B: float, LPP: float, hullProf: np.typing.arrayLike
) -> float:
    """Calculate the volume of fluid displaced by the vessel, given a profile, beam, and draught."""
    xSecA = (B * T) - simpson(hullProf)
    return LPP * xSecA


def wettedArea(v_of_D: float, T: float, LPP: float, c_R: float, b_R: float) -> float:
    """Find the wetted area of a vessel, including rudder."""
    S = (1.025 * ((v_of_D / T) + (1.7 * LPP * T))) + (c_R * b_R)
    return S
