"""
ComputeAT.py

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

import numpy as np
from util import rho_w


def computeAboutTurn60Time(S: float, C_D: float, LOA: float, P_t: float) -> float:
    t_60 = (np.pi / 3) * (((rho_w * S * C_D * (LOA**4)) / (128 * P_t)) ** (1 / 3))
    return t_60
