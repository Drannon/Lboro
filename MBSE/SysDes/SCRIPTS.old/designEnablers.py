"""Design Enablers."""

import numpy as np
from util import draught, beam, turn_speed, price_steel, deck_thickness
import util


def computeTurningCircle(args: list) -> float:
    """
    ComputeTC.py.

    Computes the turning circle of a vessel based on its rudder area, deflection and the vessel's length between perpendiculars.
    Uses the empirical Nomoto Model to calculate this.
    The Nomoto Model found non-dimensional values for ship dynamics, and using the reference values the outputs can be dimensionalised.
    The reference rudder area was 20m2, and there the empirical coefficient was 0.08.
    Hull form and slenderness is neglected in this model.

    Arguments:
        delta_R: float - rudder deflection (degrees)
        A_R: float - rudder area (m2)
        LPP: float - length between perpendiculars (m)

    Returns:
        turning_circle: float - the sustained turning radius (NOT tactical radius) of the given vessel

    """
    LPP, b_R, c_R, delta_R, P_t, a, t = args
    U = util.turn_speed

    A_R = b_R * c_R  # m - profile (NACA 00xx series) increase assumed negligible
    l_0 = 67  # m
    T_0 = 5.7  # m
    A_R_ldm_denom_0 = 23.3  # n.d.
    A_R0 = (l_0 * T_0) / A_R_ldm_denom_0  # m2
    K_0 = 0.075  # coefficient

    turning_radius = (U * A_R0) / (delta_R * A_R * K_0)
    return turning_radius


def computeAboutTurn60Time(args: list) -> float:
    """
    ComputeAT.py.

    Computes the time taken for a vessel to turn on a point (about turn) through 60 degrees.
    Uses the incompressible drag equation derived from bernoulli's law.
    It relates linear velocity to angular velocity, and force to torque.
    It takes the power of the bow and stern thrusters and then finds the required angular velocity for the hydrodynamic drag to match the thruster power.
    Finally, it converts the angular velocity to the time taken to sweep 60 degrees.

    Arguments:
        delta_R: float - rudder deflection (degrees)
        A_R: float - rudder area (m2)
        LPP: float - length between perpendiculars (m)

    Returns:
        turning_circle: float - the sustained turning radius (NOT tactical radius) of the given vessel

    """

    LPP, b_R, c_R, delta_R, P_t, a, t = args

    rho_w = util.rho_w
    C_D = util.C_D
    LOA = LPP + b_R

    # Calculate the hull profiles for the samples of hull control points

    hull_X, hull_Y = util.hull_profile_gen(np.array(a), beam, draught, 1000)

    # Calculate volume of displacement for all combinations of samples
    v_of_D = util.volumeOfDisplacement(
        T=draught, B=beam, LPP=LPP, hullXs=hull_X, hullYs=hull_Y
    )

    # Calculate wetted areas for all combinations of samples
    S = util.wettedArea(v_of_D, draught, LPP, c_R, b_R)

    t_60 = (np.pi / 3) * (((rho_w * S * C_D * (LOA**4)) / (128 * P_t)) ** (1 / 3))
    return t_60


def computeTraverseSpeed(
    args: list,
) -> float:
    """
    ComputeTS.py.

    Computes the maximum transverse speed through water that the vessel can achieve.
    This uses the
    The Nomoto Model found non-dimensional values for ship dynamics, and using the reference values the outputs can be dimensionalised.
    The reference rudder area was 20m2, and there the empirical coefficient was 0.08.
    Hull form and slenderness is neglected in this model.

    Arguments:
        delta_R: float - rudder deflection (degrees)
        A_R: float - rudder area (m2)
        LPP: float - length between perpendiculars (m)

    Returns:
        turning_circle: float - the sustained turning radius (NOT tactical radius) of the given vessel

    """
    LPP, b_R, c_R, delta_R, P_t, a, t = args

    C_D = util.C_D

    # Calculate the hull profiles for the samples of hull control points

    hull_X, hull_Y = util.hull_profile_gen(a, beam, draught, 1000)

    # Calculate volume of displacement for all combinations of samples
    v_of_D = util.volumeOfDisplacement(
        T=draught, B=beam, LPP=LPP, hullXs=hull_X, hullYs=hull_Y
    )

    # Calculate wetted areas for all combinations of samples
    S = util.wettedArea(v_of_D, draught, LPP, c_R, b_R)

    V_ts_ms = ((2 * P_t) / (util.rho_w * S * C_D)) ** (1 / 3)
    V_ts = util.ms2kt(V_ts_ms)
    return V_ts


def computeCargoMass(
    v_of_D: float, rho_w: float, v_s: float, rho_s: float, m_eqt: float
) -> float:
    """
    ComputeCargoMass.py.

    Computes the maximum transverse speed through water that the vessel can achieve.
    This uses the
    The Nomoto Model found non-dimensional values for ship dynamics, and using the reference values the outputs can be dimensionalised.
    The reference rudder area was 20m2, and there the empirical coefficient was 0.08.
    Hull form and slenderness is neglected in this model.

    Arguments:
        delta_R: float - rudder deflection (degrees)
        A_R: float - rudder area (m2)
        LPP: float - length between perpendiculars (m)

    Returns:
        turning_circle: float - the sustained turning radius (NOT tactical radius) of the given vessel

    """
    cargoCap = (v_of_D * rho_w) - (v_s * rho_s) - m_eqt
    return cargoCap
