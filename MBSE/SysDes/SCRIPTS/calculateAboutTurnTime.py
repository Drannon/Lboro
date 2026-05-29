import numpy as np

rho_w
B_r
c_r
LPP
T
C_D
P_t

LOA = LPP + c_r

hullProfile = util.hullProfile(0)
v_of_d = util.displacementVol(T, B, LPP, hullProfile)
S = util.wettedArea(B_r, c_r, LPP, T, v_of_d)

t_60 = (np.pi / 3) * ((rho_w * S * C_D * (LOA**4))/(128*P_t))
