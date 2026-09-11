"""This is a script that finds the hull profile of the boat (below the waterline) and calculates its area."""

import numpy as np

import matplotlib

import matplotlib.pyplot as plt

from scipy.integrate import simpson

matplotlib.use("gtk4agg")

fig1, ax1 = plt.subplots(1, 1)
fig2, ax2 = plt.subplots(1, 1)

ax1.grid()
ax2.grid()


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


# Ship Parameters

L = 60  # Length between perpendiculars
T = 1.2  # Draught
B_wl = 25  # Breadth at waterline
t_h = 0.1  # Hull thickness
t_d = 0.06  # Deck Plate thickness
VDFd = 4  # Vehicle Deck Freeboard
a = [i * T for i in np.linspace(0, 1, 11)]  # variable hull control point y position

P_E = 1000
P_Ds = []

us = [i * 0.5144444 for i in range(1, 13)]

v_dots = []

for u in us:
    print(f"--------U = {u / 0.51444444} m/s---------")

    v_dots_speed = []
    for i in a:
        # Hull control points
        h_0o = (0, T)
        h_1o = (0, i)
        h_2o = (0, 0)
        h_3o = ((0.2 * B_wl), 0)
        h_4o = h_3o  # Coincident
        h_5o = ((0.4 * B_wl), 0)
        h_6o = ((0.6 * B_wl), 0)
        h_7o = ((0.8 * B_wl), 0)
        h_8o = h_7o
        h_9o = (B_wl, 0)
        h_10o = (B_wl, i)
        h_11o = (B_wl, T)

        # Bezier curve calculation
        xs_1o, ys_1o = bezier_spline(1000, h_0o, h_1o, h_2o, h_3o)
        xs_2o, ys_2o = bezier_spline(1000, h_4o, h_5o, h_6o, h_7o)
        xs_3o, ys_3o = bezier_spline(1000, h_8o, h_9o, h_10o, h_11o)

        # Bezier spline creation
        xs_o = np.concatenate((xs_1o, xs_2o, xs_3o))
        ys_o = np.concatenate((ys_1o, ys_2o, ys_3o))

        # # Plotting
        # ax1.set_aspect("equal")
        # ax1.plot(xs_o, ys_o)

        # Geometric parameter calculation
        A_M = (T * B_wl) - simpson(
            y=ys_o, x=xs_o
        )  # Area amidships (bounding rectangle subtacting area under the hull)
        C_M = A_M / (T * B_wl)  # Midship coefficient
        V_d = A_M * L  # Volume of displacement assuming flat bow and stern for now
        m = V_d * 1000  # Deadweight assuming rho_water = 1000 kg/m3

        K = 19 * ((V_d / (L * B_wl * T)) * (B_wl / L)) ** 2
        A_s = 1.025 * ((V_d / T) + 1.7 * L * T)
        Re = (L * u) / 1.5e-6

        C_F = (1 + 0.1194) * (0.067 / (np.log10(Re) - 2) ** 2)

        C_V = C_F + (K * C_F)

        P_D = (0.5 * 1000 * (u**3) * A_s * C_V) / 1000  # kW
        P_Ds.append(P_D)
        v_dot = ((P_E * 1000) - (P_D * 1000)) / (u * m)
        v_dots_speed.append(v_dot)

        print(
            f"a = {round(i / T, 1)}T m, A_M: {round(A_M, 2)} m2, V_d: {round(V_d, 2)} m3, m: {round(m / 1000, 2)} t, P: {round(P_D, 2)} kW, v_dot: {v_dot} m/s2"
        )
    v_dots.append(sum(v_dots_speed) / len(v_dots_speed))

# ax2.plot(us, v_dots)
plt.show()
