"""Design Enablers."""

import numpy as np
import util

# DVs: W, S, CD0, CL, T, Pf, Pp, TSFC, AR


def computeRange(args):
    S_w, CD0, CL_max, m_f_0, m_p, AR, T, TSFC, V = args

    m_f = util.calculateFuelMassMod(args)  # Account for TSFC & CD0 impact
    m_non_struct = m_f + m_p
    W_non_struct = m_non_struct * util.g
    p_struct = util.calculateMassFraction(args)  # Account for structural increase
    W = W_non_struct / (1 - p_struct)

    CL = (2 * W) / (util.rho_a * (V**2) * S_w)  # Calculate CL at given W and V
    CD = CD0 + ((CL**2) / (np.pi * 0.8 * AR))  # Drag Polar
    W_final = W - (m_f * util.g)  # Weight at empty, i.e. no fuel remaining

    c_T = TSFC * util.g  # breguet requires TSFC multiplied by g
    breguet_range = (V / c_T) * (CL / CD) * np.log(W / W_final)  # m
    return breguet_range / 1000  # km


def computeVstall(args):
    S_w, CD0, CL_max, m_f_0, m_p, AR, T, TSFC, V = args

    m_f = util.calculateFuelMassMod(args)
    m_non_struct = m_f + m_p
    W_non_struct = m_non_struct * util.g
    p_struct = util.calculateMassFraction(args)
    W = W_non_struct / (1 - p_struct)

    Vstall = np.sqrt((2 * W) / (util.rho_a * S_w * CL_max))
    return Vstall


def computeTurnRadius(args):
    S_w, CD0, CL_max, m_f_0, m_p, AR, T, TSFC, V = args

    m_f = util.calculateFuelMassMod(args)
    m_non_struct = m_f + m_p
    W_non_struct = m_non_struct * util.g
    p_struct = util.calculateMassFraction(args)
    W = W_non_struct / (1 - p_struct)

    L_max = 0.5 * util.rho_a * (V**2) * S_w * CL_max
    n_max = L_max / W
    r_turn = (V**2) / (util.g * np.sqrt((n_max**2) - 1))
    return r_turn


def computeRateOfClimb(args):
    S_w, CD0, CL_max, m_f_0, m_p, AR, T, TSFC, V = args

    m_f = util.calculateFuelMassMod(args)
    m_non_struct = m_f + m_p
    W_non_struct = m_non_struct * util.g
    p_struct = util.calculateMassFraction(args)
    W = W_non_struct / (1 - p_struct)

    CL = (2 * W) / (util.rho_a * (V**2) * S_w)
    CD = CD0 + ((CL**2) / (np.pi * 0.8 * AR))  # Oswald Efficiency set to 0.8
    D = 0.5 * util.rho_a * (V**2) * S_w * CD

    ROC = ((T - D) * V) / W
    return ROC
