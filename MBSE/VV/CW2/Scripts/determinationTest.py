"""Determination Test."""

import numpy as np
import pandas as pd
from scipy.constants import g
from scipy.integrate import simpson
from matplotlib import use
from matplotlib import pyplot as plt
import utilities
from utilities import kts2ms, ms2kts

use("gtk4agg")
fig0, ax0 = plt.subplots(1, 1)
fig1, ax1 = plt.subplots(subplot_kw={"projection": "3d"})
# ax.set_aspect("equal")

# Constants
rho_w = 1000  # kg/m3 - density of freshwater
nu_w = 1.5e-6  # m2/s - Kinematic viscosity of freshwater

# Specificaitons
L = 60  # m - Length
B = 25  # m - Breadth
T = 1.2  # m - Draught
a = 0.5  # % - Hull Control Point Value
u_max = 12  # kts - Maximum speed
u_cruise = 8  # kts - Cruising speed
u_cruise_ex = 5  # kts - Cruising speed
P_m = 1e6  # W - Motor power
E_bat = 1  # MWh
P_charge = 0.5  # MWh

u_max = kts2ms(u_max)  # Conversion to m/s

# Power Required
# Factors: u, k

# Minimum speed to meed requirement of 3 mins:
u_min = 300 / (60 * 3)

u_range = np.linspace(u_min, u_max, 100)
Re_range = (u_range * L) / (nu_w)
ks = np.linspace(0, 1, 100)
V_d_range = np.empty((100, 1))

# Hull Profile Demo

hull0_xs, hull0_ys = utilities.hull_profile_gen(0, B, T, 100)
hull1_xs, hull1_ys = utilities.hull_profile_gen(0.5, B, T, 100)
hull2_xs, hull2_ys = utilities.hull_profile_gen(1, B, T, 100)

ax0.plot(hull0_xs, hull0_ys, "r", label="k = 0T (waterline)")
ax0.plot(hull1_xs, hull1_ys, "g", label="k = 0.5T")
ax0.plot(hull2_xs, hull2_ys, "b", label="k = T (keel)")

fig0.set_size_inches(16, 9)
ax0.set_aspect("equal")
ax0.grid()
ax0.set_xlabel("Breadth [m]")
ax0.set_ylabel("Draught [m]")
ax0.legend(bbox_to_anchor=(0.5, 1.5))

fig0.savefig(
    "/home/matth/Documents/Lboro/MBSE/VV/CW2/REPORT/UTIL/FIGS/hull_profile_demos.png",
    dpi=300,
)

for i, k in enumerate(ks):
    hull_xs, hull_ys = utilities.hull_profile_gen(k, B, T, 100)
    A_M = (T * B) - simpson(hull_ys, hull_xs)
    V_d = A_M * L
    V_d_range[i] = V_d

Re_range, V_d_range = np.meshgrid(Re_range, V_d_range)
P_ds = utilities.drag_power(V_d_range, L, B, T, Re_range, rho_w, nu_w)

# Requirement Plane
P_accept = 500 + 0 * Re_range + 0 * V_d_range

u_range, ks = np.meshgrid(u_range, ks)
S = ax1.plot_surface(
    ms2kts(u_range), ((V_d_range * rho_w) / 1000), P_ds / 1000, cmap="inferno"
)

ax1.grid()
ax1.set_xlabel("Top Speed [knots]")
ax1.set_ylabel("Displacement [tonnes]")
ax1.set_zlabel("Power [kW]")
ax1.view_init(elev=20, azim=140, roll=0)
cbar = fig1.colorbar(S, shrink=0.5, label="Power [kW]")

ax1.plot_surface(
    ms2kts(u_range),
    ((V_d_range * rho_w) / 1000),
    P_accept,
    color="Black",
    alpha=0.5,
)

fig1.set_size_inches(16, 9)

fig1.savefig(
    "/home/matth/Documents/Lboro/MBSE/VV/CW2/REPORT/UTIL/FIGS/u-k-P-iso.png",
    dpi=300,
)

ax1.view_init(elev=0, azim=180, roll=0)
ax1.set_xlabel("")
ax1.get_xaxis().set_visible(False)
fig1.savefig(
    "/home/matth/Documents/Lboro/MBSE/VV/CW2/REPORT/UTIL/FIGS/k-P.png", dpi=300
)

ax1.view_init(elev=0, azim=90, roll=0)
ax1.set_xlabel("Top Speed [knots]")
ax1.get_xaxis().set_visible(True)
ax1.set_ylabel("")
ax1.get_yaxis().set_visible(False)
ax1.set_yticks([])
fig1.savefig(
    "/home/matth/Documents/Lboro/MBSE/VV/CW2/REPORT/UTIL/FIGS/u-P.png", dpi=300
)

# Range Determination

# Sensitivity Analysis

P_accel = np.linspace(1e5, 1e6, 50)
u_cruise_range = np.linspace(1, 8, 50)
u_cruise_range = kts2ms(u_cruise_range)
k_range = np.linspace(0, 1, 10)
E_bat_range = np.linspace(0.5, 1.5, 50)
Temp_range = np.linspace(-10, 30, 50)

t_u_a_1s = []
a_bar_a_1s = []
t_u_d_1s = []
a_bar_d_1s = []

for i, u in enumerate(u_cruise_range):
    t_u_a_1, a_bar_a_1 = utilities.acceleration_time(
        u_cruise_range[0],
        u,
        100,
        P_m,
        V_d,
        L,
        B,
        T,
        (V_d * rho_w),
        rho_w,
        nu_w,
    )
    t_u_a_1s.append(t_u_a_1)
    a_bar_a_1s.append(a_bar_a_1)

    t_u_d_1, a_bar_d_1 = utilities.acceleration_time(
        u,
        u_cruise_range[0],
        100,
        P_m,
        V_d,
        L,
        B,
        T,
        (V_d * rho_w),
        rho_w,
        nu_w,
        mode=2,
    )
    t_u_d_1s.append(t_u_d_1)
    a_bar_d_1s.append(a_bar_d_1)

t_u_a_1s = np.array(t_u_a_1s)
a_bar_a_1s = np.array(a_bar_a_1s)
t_u_d_1s = np.array(t_u_d_1s)
a_bar_d_1s = np.array(a_bar_d_1s)

s_to_u_max_1 = u_cruise_range[0] * t_u_a_1s + a_bar_a_1s * t_u_a_1s**2
s_from_u_max_1 = u_cruise_range * t_u_d_1s + a_bar_d_1s * t_u_d_1s**2
s_cruise = 300 - s_to_u_max_1 - s_from_u_max_1

t_cruise_1 = s_cruise / (u_cruise_range)
t_total_1 = t_u_a_1s + t_u_d_1s + t_cruise_1
#t_range_1 = np.linspace(0, t_total_1, 50)

Re_cruise_1 = (L * u_cruise_range) / nu_w
P_cruise_1 = utilities.drag_power(V_d, L, B, T, Re_cruise_1, rho_w, nu_w)


profiles_1 = np.zeros((len(u_cruise_range), 2, len(P_cruise_1)))
for i, u in enumerate(u_cruise_range):
    t_range = np.linspace(1, t_total_1[i], len(u_cruise_range))
    profiles_1[i, 0, :] = t_range

    for pos, time in enumerate(t_range):
        if time <= t_u_a_1:
            profiles_1[i, 1, pos] = P_m
        elif time <= (time - t_u_d_1):
            profiles_1[i, 1, pos] = P_cruise_1[i]
        else:
            profiles_1[i, 1, pos] = P_m

for i in range(50):
    E_run = simpson(profiles_1[i, 1, :], profiles_1[i, 0, :])
    print(E_run)
    # this is working so far :)

plt.show()
