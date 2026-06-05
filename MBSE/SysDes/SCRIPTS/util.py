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


def kt2ms(V_kt: float) -> float:
    """Convert a speed in metres per second to knots."""
    return (463 * V_kt) / 900


def bezier_point_calc(
    t: float,
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float],
    p4: tuple[float, float],
) -> tuple[float, float]:
    """
    Bezier Point Calculation.

    Gives the cartesian coordinates of a point along a cubic Bezier curve
    at a given t.

    Parameters:
        t: float = Value of t for calculated point
        p1: tuple(float) = Cartesian coordinates of the first control point
        p2: tuple(float) = Cartesian coordinates of the second control point
        p3: tuple(float) = Cartesian coordinates of the third control point
        p4: tuple(float) = Cartesian coordinates of the fourth control point

    Returns:
        Tuple of:
        x: float = x coordinate of curve point
        y: float = y coordinate of curve point
    """
    x = (
        (((1 - t) ** 3) * p1[0])
        + (3 * t * ((1 - t) ** 2) * p2[0])
        + (3 * (t**2) * (1 - t) * p3[0])
        + ((t**3) * p4[0])
    )

    y = (
        (((1 - t) ** 3) * p1[1])
        + (3 * t * ((1 - t) ** 2) * p2[1])
        + (3 * (t**2) * (1 - t) * p3[1])
        + ((t**3) * p4[1])
    )

    return (x, y)


def bezier_spline(
    n: int,
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float],
    p4: tuple[float, float],
) -> tuple[float, float]:
    """
    Bezier Spline Funciton.

    Calculates n cartesian coordinates of a cubic Bezier curve.

    Parameters:
        n: int = Number of samples
        p1: tuple(float) = Cartesian coordinates of the first control point
        p2: tuple(float) = Cartesian coordinates of the second control point
        p3: tuple(float) = Cartesian coordinates of the third control point
        p4: tuple(float) = Cartesian coordinates of the fourth control point

    Returns:
        np.array of:
        : tuple = bezier_point_calc return coordinates
    """
    ts = np.linspace(0, 1, n)

    return bezier_point_calc(ts, p1, p2, p3, p4)


def hull_profile_gen(a: float, B_wl: float, T: float, n: int) -> np.typing.ArrayLike:
    """
    Hull Profile Generator.

    This function generates a cross-sectional profile of a flat-bottomed hull based on the hull's design envelope,
    and a control point that affects the blocking coefficient of the hull.
    It does this by defining a cubic bezier spline, who's second point is moved in the y direction between the base and the waterline.

    Parameters:
        a: float = Hull Profile Control Value
        B_wl: float = Breadth at waterline
        T: float = Draught
        n: Number of samples along the spline

    Returns:
        Tuple of:
            xs: ArrayLike = x values of the hull
            ys: ArrayLike = y values of the hull
    """
    h_0 = (0, T)
    h_1 = (0, (a * T))
    h_2 = (0, 0)
    h_3 = ((0.2 * B_wl), 0)
    h_4 = h_3  # Coincident
    h_5 = ((0.4 * B_wl), 0)
    h_6 = ((0.6 * B_wl), 0)
    h_7 = ((0.8 * B_wl), 0)
    h_8 = h_7
    h_9 = (B_wl, 0)
    h_10 = (B_wl, (a * T))
    h_11 = (B_wl, T)

    # Bezier curve calculation
    xs_1, ys_1 = bezier_spline(n, h_0, h_1, h_2, h_3)
    xs_2, ys_2 = bezier_spline(n, h_4, h_5, h_6, h_7)
    xs_3, ys_3 = bezier_spline(n, h_8, h_9, h_10, h_11)

    # Bezier spline creation
    xs = np.concatenate((xs_1, xs_2, xs_3))
    ys = np.concatenate((ys_1, ys_2, ys_3))

    return xs, ys


def volumeOfDisplacement(
    T: float,
    B: float,
    LPP: float,
    hullXs: np.typing.ArrayLike,
    hullYs: np.typing.ArrayLike,
) -> float:
    """Calculate the volume of fluid displaced by the vessel, given a profile, beam, and draught."""
    xSecA = (B * T) - simpson(hullXs, hullYs)
    return LPP * xSecA


def wettedArea(v_of_D: float, T: float, LPP: float, c_R: float, b_R: float) -> float:
    """Find the wetted area of a vessel, including rudder."""
    S = (1.025 * ((v_of_D / T) + (1.7 * LPP * T))) + (c_R * b_R)
    return S
