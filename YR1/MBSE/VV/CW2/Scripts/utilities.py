"""Utilities for Verification and Validation."""

import numpy as np
from scipy.integrate import simpson
from scipy.optimize import curve_fit


def kts2ms(u: float) -> float:
    """
    Knots to m/s conversion.

    Converts a given speed in knots to metres per second

    Parameters:
        u: float = Speed in knots

    Returns:
        float = Speed in m/s
    """
    return u * 0.51444444


def ms2kts(u: float) -> float:
    """
    Knots to m/s conversion.

    Converts a given speed in knots to metres per second

    Parameters:
        u: float = Speed in knots

    Returns:
        float = Speed in m/s
    """
    return u / 0.51444444


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


def drag_power(
    V_d: float, L: float, B: float, T: float, Re: float, rho: float, nu: float
) -> float:
    """
    Drag Power Calculator.

    This function calculates the power of drag on the hull at a given speed, and thus the power needed to overcome it.

    Parameters:
        V_d: float = Volume of displacement
        L: float = Length of hull
        B: float = Breadth of hull
        T: float = Draught
        Re: float = Reynolds number (u*L/nu) of the flow
        rho: float = Density of the fluid
        nu: float = Kinematic viscosity of the fluid

    Returns:
        P_d: float = Power of drag
    """
    A_s = 1.025 * ((V_d / T) + 1.7 * L * T)  # m2 - Wetted Area of Hull
    u = (Re * nu) / L

    K = 19 * ((V_d / (L * B * T)) * (B / L)) ** 2  # Form Factor Approximation
    C_F = 0.075 / ((np.log10(Re) - 2) ** 2)  # Coefficient of friction
    C_V = C_F + (K * C_F)  # Coefficient of viscous drag

    F_d = 0.5 * rho * (u**2) * A_s * C_V  # N - Drag Force
    P_d = F_d * u  # W - Drag Power

    return P_d


def acceleration_time(
    u_0: float,
    u_target: float,
    n: int,
    P_m: float,
    V_d: float,
    L: float,
    B: float,
    T: float,
    m: float,
    rho: float,
    nu: float,
    mode: float = 1,
) -> tuple[float, float]:
    """
    Acceleration Time Calculator.

    Finds the time taken for a vessel to reach a target speed given a (non zero) initial speed.
    The initial speed must be non-zero, as this does not model phenomena at rest.
    As such acceleration from rest would always infinite.
    Additionally, as velocity approaches zero, acceleration approaches infinity.
    As such, initial velocity should be suitably large.

    This function ignores wave and residual drag, so should only be used for suitably low Froud Numbers (Fr<0.25)

    Parameters:
        u_0: float = Initial Velocity
        u_target: float = Target Velocity
        n: int = Fidelity of model (number of points)
        P_m: float = Motor Power
        V_d: float = Volume of Displacement
        L: float = Length of hull
        B: float = Breadth of hull
        T: float = Draught
        m: float = Displacement
        rho: float = Density of fluid
        nu: float = Kinematic viscosity of fluid
        mode: int = Acceleration (1) or Decceleration (2) mode. Enables/Disables negative acceleration checking. Defaults to 1.

    Returns:
        t_u_target: float = Time to target velocity.
        a_bar: float = Average acceleration.
    """

    u_range_kts = np.linspace(u_0, u_target, n)
    u_range = u_range_kts * 0.5144444

    Re_range = (L * u_range) / nu
    P_range = drag_power(V_d, L, B, T, Re_range, rho, nu)
    delta_Ps = P_m - P_range

    # If accelerating, raise error if speed is unreachable
    if mode == 1:
        if np.any(np.less_equal(delta_Ps, 0)):
            raise (AttributeError("Max Speed not possible"))

    a_fs = (delta_Ps) / (m * u_range)

    if mode == 2:
        a_fs *= -a_fs

    a_bar = sum(a_fs) / len(a_fs)

    t_u_target = simpson(y=(1 / a_fs), x=u_range)
    return t_u_target, a_bar


def battery_model_find() -> np.typing.ArrayLike:
    """
    Battery Model Finder.

    Finds the function that maps temperatures to percentage of battery capacity, from the data presented in reference.

    Parameters:
        None

    Returns:
        params[0]: ArrayLike = Numpy array containing the parameters for the fitting function.
    """
    # Using data from reference
    data_temps = np.array([30, 20, 15, 12, 9, 3, 0, -2, -6, -8])
    data_actual_caps = np.array(
        [4.947, 4.8465, 4.7633, 4.7212, 4.6489, 4.4847, 4.4283, 4.2785, 4.1703, 4.1110]
    )
    data_cap_percents = data_actual_caps / 5  # Percentages from data nominal capacity
    params = curve_fit(
        lambda x, a, b, c: a * (x**2) + b * x + c, data_temps, data_cap_percents
    )
    return params[0]


def temp_cap(cap_nominal, temp) -> float:
    """
    Capacity calculator at temperature.

    Given the nominal capacity of a lithium ion battery and ambient temperature, return the actual (estimated) capacity of the battery at that temperature.

    Parameters:
        cap_nominal: float = Nominal capacity
        temp: float = Ambient temperature

    Returns:
        :float = Capacity of the battery at temp
    """
    af, bf, cf = battery_model_find()
    eff_at_temp = af * (temp**2) + bf * temp + cf
    return cap_nominal * eff_at_temp
