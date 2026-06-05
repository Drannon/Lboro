"""Design Enablers."""

import numpy as np
from util import rho_w, ms2kt


def computeTurningCircle(delta_R: float, A_R: float, LPP: float) -> float:
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
    A_R0 = 20  # m2
    K_0 = 0.08  # coefficient

    turning_circle = (K_0 * A_R * LPP) / (A_R0 * delta_R)
    return turning_circle


def computeAboutTurn60Time(S: float, C_D: float, LOA: float, P_t: float) -> float:
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
    t_60 = (np.pi / 3) * (((rho_w * S * C_D * (LOA**4)) / (128 * P_t)) ** (1 / 3))
    return t_60


def computeTraverseSpeed(P_t: float, rho_w: float, S: float, C_D: float) -> float:
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
    V_ts_ms = ((2 * P_t) / (rho_w * S * C_D)) ** (1 / 3)
    V_ts = ms2kt(V_ts_ms)
    return V_ts
