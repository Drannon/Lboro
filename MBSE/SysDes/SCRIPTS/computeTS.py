"""
ComputeTS.py

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


def computeTurningCircle(delta_R: float, A_R: float, LPP: float) -> float:
    A_R0 = 20  # m2
    K_0 = 0.08  # coefficient

    turning_circle = (K_0 * A_R * LPP) / (A_R0 * delta_R)
    return turning_circle
