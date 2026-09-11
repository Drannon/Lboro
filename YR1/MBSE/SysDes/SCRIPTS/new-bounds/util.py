"""Utilities for Systems Design Coursework Simulation."""

import numpy as np
from numpy import typing as npt
from scipy.integrate import simpson
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.inspection import partial_dependence
from matplotlib import pyplot as plt

# Physical constants
rho_a = 1.225  # kg/m3
g = 9.81


def rstool(
    X: npt.ArrayLike, y: npt.ArrayLike, X_test: npt.ArrayLike = 0, n_obs=1
) -> None:
    """
    Predict response surface contours.

    This function uses ordinary least squares regression to find the effect of input independent variables on a dependent output variable.
    It creates a polynomial design matrix from the input training features, and fits a linear regression to that matrix. This creates a quatratic fit.
    """
    rsfig, rsaxs = plt.subplots(
        n_obs,
        np.shape(X)[1],
        figsize=(12, 3 * n_obs),
        gridspec_kw={"wspace": 0},
    )

    models = [
        make_pipeline(
            PolynomialFeatures(degree=2, include_bias=False), LinearRegression()
        ).fit(X, y.iloc[:, obj])
        for obj in range(y.shape[1])
    ]

    for obj in range(y.shape[1]):
        for feat in range(X.shape[1]):

            pdp = partial_dependence(
                models[obj],
                X,
                features=[feat],
            )

            if y.shape[1] != 1:
                rsaxs[obj, feat].plot(
                    pdp["grid_values"][0],
                    pdp["average"][0],
                )

                rsaxs[obj, feat].grid(True)
            else:
                rsaxs[feat].plot(
                    pdp["grid_values"][0],
                    pdp["average"][0],
                )

    for obj in range(y.shape[1]):
        if y.shape[1] != 1:
            row_axes = rsaxs[obj, :]
        else:
            row_axes = rsaxs

        ymin = min(ax.lines[0].get_ydata().min() for ax in row_axes)
        ymax = max(ax.lines[0].get_ydata().max() for ax in row_axes)

        for axnum, ax in enumerate(row_axes):
            ax.set_ylim(ymin, ymax)
            ax.grid(False)
            if axnum != 0:
                ax.set_yticks([])
            else:
                ax.set_ylabel(y.iloc[:, obj].name)
            ax.set_xlabel(X.iloc[:, axnum].name)


def ms2kt(V_ms: float) -> float:
    """Convert a speed in metres per second to knots."""
    return (900 * V_ms) / 463


def kt2ms(V_kt: float) -> float:
    """Convert a speed in metres per second to knots."""
    return (463 * V_kt) / 900


def deg2rad(theta_deg: float) -> float:
    """Convert an angle in degrees to raidans."""
    return theta_deg * (np.pi / 180)


def rad2deg(theta_deg: float) -> float:
    """Convert an angle in radians to degrees."""
    return theta_deg * (180 / np.pi)

