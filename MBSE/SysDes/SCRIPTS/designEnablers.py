"""Design Enablers."""

import numpy as np
import util

# DVs: W, S, CD0, CL, T, Pf, Pp, TSFC, AR


def computeRange(args):
    S_w, CD0, CL, m_f, m_p, A_inlet, f, AR, T, V = args

    W_non_struct = m_f + m_p
    W = W_non_struct / 0.6
    mdot_a = util.rho_a * A_inlet * V
    TSFC = (f * mdot_a) / T
    CD = CD0 + ((CL**2) / (np.pi * np.e * AR))
    W_final = W - m_f
    breguet_range = (V / TSFC) * (CL / CD) * np.log(W / W_final)
    return breguet_range


def computeVstall(args):
    S_w, CD0, CL, m_f, m_p, A_inlet, f, AR, T, V = args

    W_non_struct = m_f + m_p
    W = W_non_struct / 0.6
    S = S_w + A_inlet
    Vstall = np.sqrt((2 * W) / (util.rho_a * S * CL))
    return Vstall


def computeTurnRadius(args):
    S_w, CD0, CL, m_f, m_p, A_inlet, f, AR, T, V = args

    W_non_struct = m_f + m_p
    W = W_non_struct / 0.6
    L = 0.5 * util.rho_a * (V**2) * S_w * CL
    n = L / W
    r_turn = (V**2) / (util.g * np.sqrt((n**2) - 1))
    return r_turn


def computeRateOfClimb(args):
    S_w, CD0, CL, m_f, m_p, A_inlet, f, AR, T, V = args

    W_non_struct = m_f + m_p
    W = W_non_struct / 0.6
    S = S_w + A_inlet
    CD = CD0 + ((CL**2) / (np.pi * np.e * AR))
    D = 0.5 * util.rho_a * (V**2) * S * CD

    ROC = ((T - D) * V) / W
    return ROC
