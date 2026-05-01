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
fig_hp_demo, ax_hp_demo = plt.subplots(1, 1)
fig_surf_umax, ax_surf_umax = plt.subplots(subplot_kw={"projection": "3d"})
fig_uc, ax_uc = plt.subplots()
fig_hp, ax_hp = plt.subplots()
fig_temp, ax_temp = plt.subplots()
fig_batcap, ax_batcap = plt.subplots()
fig_surf_end, ax_surf_end = plt.subplots(subplot_kw={"projection": "3d"})

ax_hp_demo.set_title("Example Hull Profiles", pad=20)
ax_surf_umax.set_title("Variance of Power Required with Top Speed and Hull Profile")
ax_uc.set_title("Effect of Cruise Speed on Endurance")
ax_hp.set_title("Effect of Hull Profile on Endurance")
ax_temp.set_title("Effect of Ambient Temperature on Endurance")
ax_batcap.set_title("Effect of Battery Capacity on Endurance and Battery Mass")
ax_surf_end.set_title("")
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
u_cruise = kts2ms(u_cruise)
u_cruise_ex = 5  # kts - Cruising speed
P_m = 1e6  # W - Motor power
E_bat = 1  # MWh
rho_bat = 3e-4  # MWh/kg
P_charge = 0.5  # MWh

u_max = kts2ms(u_max)  # Conversion to m/s

# Power Required
# Factors: u, k

# Minimum speed to meed requirement of 3 mins:
u_min = 300 / (60 * 3)

u_range = np.linspace(u_min, u_max, 100)
Re_range = (u_range * L) / (nu_w)
ks = np.linspace(0, 1, 100)
V_d_range = np.empty((100))

# Hull Profile Demo

hull0_xs, hull0_ys = utilities.hull_profile_gen(0, B, T, 100)
hull1_xs, hull1_ys = utilities.hull_profile_gen(0.5, B, T, 100)
hull2_xs, hull2_ys = utilities.hull_profile_gen(1, B, T, 100)

ax_hp_demo.plot(hull0_xs, hull0_ys, "r", label="k = 0T (keel)")
ax_hp_demo.plot(hull1_xs, hull1_ys, "g", label="k = 0.5T")
ax_hp_demo.plot(hull2_xs, hull2_ys, "b", label="k = T (waterline)")

fig_hp_demo.set_size_inches(16, 9)
ax_hp_demo.set_aspect("equal")
ax_hp_demo.grid()
ax_hp_demo.set_xlabel("Breadth [m]")
ax_hp_demo.set_ylabel("Draught [m]")
ax_hp_demo.legend(bbox_to_anchor=(0.5, 1.5))

fig_hp_demo.savefig(
    "/home/matth/Documents/Lboro/MBSE/VV/CW2/REPORT/UTIL/FIGS/hull_profile_demos.png",
    dpi=300,
)

for i, k_i in enumerate(ks):
    hull_xs, hull_ys = utilities.hull_profile_gen(k_i, B, T, 100)
    A_M = (T * B) - simpson(hull_ys, hull_xs)
    V_d = A_M * L
    V_d_range[i] = V_d

Re_range, V_d_range = np.meshgrid(Re_range, V_d_range)
P_ds = utilities.drag_power(V_d_range, L, B, T, Re_range, rho_w, nu_w)

# Requirement Plane
P_accept = 500 + 0 * Re_range + 0 * V_d_range

u_range, ks = np.meshgrid(u_range, ks)
S = ax_surf_umax.plot_surface(
    ms2kts(u_range), ((V_d_range * rho_w) / 1000), P_ds / 1000, cmap="inferno"
)

ax_surf_umax.grid()
ax_surf_umax.set_xlabel("Top Speed [knots]")
ax_surf_umax.set_ylabel("Displacement [tonnes]")
ax_surf_umax.set_zlabel("Power [kW]")
ax_surf_umax.view_init(elev=20, azim=140, roll=0)
cbar = fig_surf_umax.colorbar(S, shrink=0.5, label="Power [kW]")

ax_surf_umax.plot_surface(
    ms2kts(u_range),
    ((V_d_range * rho_w) / 1000),
    P_accept,
    color="Black",
    alpha=0.5,
)

fig_surf_umax.set_size_inches(16, 9)

fig_surf_umax.savefig(
    "/home/matth/Documents/Lboro/MBSE/VV/CW2/REPORT/UTIL/FIGS/u-k-P-iso.png",
    dpi=300,
)

ax_surf_umax.view_init(elev=0, azim=180, roll=0)
ax_surf_umax.set_xlabel("")
ax_surf_umax.get_xaxis().set_visible(False)
fig_surf_umax.savefig(
    "/home/matth/Documents/Lboro/MBSE/VV/CW2/REPORT/UTIL/FIGS/k-P.png", dpi=300
)

ax_surf_umax.view_init(elev=0, azim=90, roll=0)
ax_surf_umax.set_xlabel("Top Speed [knots]")
ax_surf_umax.get_xaxis().set_visible(True)
ax_surf_umax.set_ylabel("")
ax_surf_umax.get_yaxis().set_visible(False)
ax_surf_umax.set_yticks([])
fig_surf_umax.savefig(
    "/home/matth/Documents/Lboro/MBSE/VV/CW2/REPORT/UTIL/FIGS/u-P.png", dpi=300
)

# Range Determination

# Sensitivity Analysis
# Range definitions

u_cruise_range = np.linspace(1, 8, 500)
u_cruise_range = kts2ms(u_cruise_range)
u_initial = 0.5
k_range = np.linspace(0, 1, 500)
k = 0.5
E_bat_range = np.linspace(0.5, 1.5, 500)
Temp_range = np.linspace(-10, 30, 500)


# Varying u_cruise --------------
hull_xs_1, hull_ys_1 = utilities.hull_profile_gen(k, B, T, 500)
A_M_1 = (T * B) - simpson(hull_ys_1, hull_xs_1)
V_d_1 = A_M_1 * L

t_u_a_1s = []
a_bar_a_1s = []
t_u_d_1s = []
a_bar_d_1s = []

for i, u in enumerate(u_cruise_range):
    t_u_a_1, a_bar_a_1 = utilities.acceleration_time(
        u_initial,
        u,
        500,
        P_m,
        V_d_1,
        L,
        B,
        T,
        (V_d_1 * rho_w),
        rho_w,
        nu_w,
    )
    t_u_a_1s.append(t_u_a_1)
    a_bar_a_1s.append(a_bar_a_1)

    t_u_d_1, a_bar_d_1 = utilities.acceleration_time(
        u,
        u_initial,
        500,
        P_m,
        V_d_1,
        L,
        B,
        T,
        (V_d_1 * rho_w),
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

s_to_u_max_1 = (u_initial * t_u_a_1s) + (0.5 * a_bar_a_1s * t_u_a_1s**2)
s_from_u_max_1 = (u_cruise_range * t_u_d_1s) + (0.5 * a_bar_d_1s * t_u_d_1s**2)

s_cruise = 300 - s_to_u_max_1 - s_from_u_max_1

t_cruise_1 = s_cruise / (u_cruise_range)
t_total_1 = t_u_a_1s + t_u_d_1s + t_cruise_1

Re_cruise_1 = (L * u_cruise_range) / nu_w
P_cruise_1 = utilities.drag_power(V_d, L, B, T, Re_cruise_1, rho_w, nu_w)

profiles_1 = np.zeros((len(u_cruise_range), 2, len(P_cruise_1)))
for i, u in enumerate(u_cruise_range):
    t_range = np.linspace(0, t_total_1[i], len(u_cruise_range))
    profiles_1[i, 0, :] = t_range

    for pos, time in enumerate(t_range):
        if time <= t_u_a_1s[i]:
            profiles_1[i, 1, pos] = P_m

        elif time <= (t_total_1[i] - t_u_d_1s[i]):
            profiles_1[i, 1, pos] = P_cruise_1[i]

        else:
            profiles_1[i, 1, pos] = P_m

E_runs = []
for i in range(500):
    E_run = simpson(profiles_1[i, 1, :], profiles_1[i, 0, :])
    E_runs.append(E_run)

E_runs = np.array(E_runs)  # Ws
E_runs /= 3600  # Wh
E_runs /= 1e6  # MWh
N_runs = E_bat / E_runs
ts_end_1 = N_runs * t_total_1  # s
ts_end_1 /= 3600  # h

# Find minimum acceptable speed to meet requirement
min_accept_u_pos = np.size(u_cruise_range) - np.size(np.where(u_cruise_range > (5 / 2)))

# Plot all values above that
ax_uc.plot(ms2kts(u_cruise_range[min_accept_u_pos:]), ts_end_1[min_accept_u_pos:])
ax_uc.set_xlabel("Cruising Speed [kts]")
ax_uc.set_ylabel("Endurance [h]")
ax_uc.grid()

fig_uc.savefig(
    "/home/matth/Documents/Lboro/MBSE/VV/CW2/REPORT/UTIL/FIGS/uc-sense.png", dpi=300
)


# Varying k ----------------------
t_u_a_2s = []
a_bar_a_2s = []
t_u_d_2s = []
a_bar_d_2s = []
V_d_k_range = np.empty(len(k_range))

for i, k_i in enumerate(k_range):
    hull_xs, hull_ys = utilities.hull_profile_gen(k_i, B, T, 500)
    A_M_i = (T * B) - simpson(hull_ys, hull_xs)
    V_d_i = A_M_i * L
    V_d_k_range[i] = V_d_i

    t_u_a_2, a_bar_a_2 = utilities.acceleration_time(
        u_initial,
        u_cruise,
        500,
        P_m,
        V_d_i,
        L,
        B,
        T,
        (V_d * rho_w),
        rho_w,
        nu_w,
    )
    t_u_a_2s.append(t_u_a_2)
    a_bar_a_2s.append(a_bar_a_2)

    t_u_d_2, a_bar_d_2 = utilities.acceleration_time(
        u_cruise,
        u_initial,
        500,
        P_m,
        V_d_i,
        L,
        B,
        T,
        (V_d * rho_w),
        rho_w,
        nu_w,
        mode=2,
    )
    t_u_d_2s.append(t_u_d_2)
    a_bar_d_2s.append(a_bar_d_2)

t_u_a_2s = np.array(t_u_a_2s)
a_bar_a_2s = np.array(a_bar_a_2s)
t_u_d_2s = np.array(t_u_d_2s)
a_bar_d_2s = np.array(a_bar_d_2s)

s_to_u_max_2 = (u_initial * t_u_a_2s) + (0.5 * a_bar_a_2s * t_u_a_2s**2)
s_from_u_max_2 = (u_cruise * t_u_d_2s) + (0.5 * a_bar_d_2s * t_u_d_2s**2)
s_cruise = 300 - s_to_u_max_2 - s_from_u_max_2

t_cruise_2 = s_cruise / (u_cruise)
t_total_2 = t_u_a_2s + t_u_d_2s + t_cruise_2

Re_cruise_2 = (L * u_cruise) / nu_w
P_cruise_2 = utilities.drag_power(V_d_k_range, L, B, T, Re_cruise_2, rho_w, nu_w)

profiles_2 = np.zeros((len(V_d_k_range), 2, len(P_cruise_2)))
for i, V_d_k in enumerate(V_d_k_range):
    t_range = np.linspace(1, t_total_2[i], len(P_cruise_2))
    profiles_2[i, 0, :] = t_range

    for pos, time in enumerate(t_range):
        if time <= t_u_a_2:
            profiles_2[i, 1, pos] = P_m
        elif time <= (t_total_2[i] - t_u_d_2):
            profiles_2[i, 1, pos] = P_cruise_2[i]
        else:
            profiles_2[i, 1, pos] = P_m

E_runs_2 = []

for i, _ in enumerate(V_d_k_range):
    E_run_2 = simpson(profiles_2[i, 1, :], profiles_2[i, 0, :])
    E_runs_2.append(E_run_2)

E_runs_2 = np.array(E_runs_2)
E_runs_2 /= 3600  # Wh
E_runs_2 /= 1e6  # MWh
N_runs_2 = E_bat / E_runs_2
ts_end_2 = N_runs_2 * t_total_2  # s
ts_end_2 /= 3600  # h

ax_hp.plot(k_range, ts_end_2)
ax_hp.set_xlabel("Hull Profile Control Point Location")
ax_hp.set_ylabel("Endurance [h]")
ax_hp.grid()

fig_hp.savefig(
    "/home/matth/Documents/Lboro/MBSE/VV/CW2/REPORT/UTIL/FIGS/hp-sense.png", dpi=300
)

# Varying temperature

hull_xs_3, hull_ys_3 = utilities.hull_profile_gen(k_i, B, T, 500)
A_M_3 = (T * B) - simpson(hull_ys_3, hull_xs_3)
V_d_3 = A_M_3 * L

t_u_a_3, a_bar_a_3 = utilities.acceleration_time(
    u_initial,
    u_cruise,
    500,
    P_m,
    V_d_3,
    L,
    B,
    T,
    (V_d_3 * rho_w),
    rho_w,
    nu_w,
)

t_u_d_3, a_bar_d_3 = utilities.acceleration_time(
    u_cruise,
    u_initial,
    500,
    P_m,
    V_d_3,
    L,
    B,
    T,
    (V_d_3 * rho_w),
    rho_w,
    nu_w,
    mode=2,
)

s_to_u_max_3 = (u_initial * t_u_a_3) + (0.5 * a_bar_a_3 * t_u_a_3**2)
s_from_u_max_3 = (u_cruise * t_u_d_3) + (0.5 * a_bar_d_3 * t_u_d_3**2)
s_cruise = 300 - s_to_u_max_3 - s_from_u_max_3

t_cruise_3 = s_cruise / (u_cruise)
t_total_3 = t_u_a_3 + t_u_d_3 + t_cruise_3

Re_cruise_3 = (L * u_cruise) / nu_w
P_cruise_3 = utilities.drag_power(V_d_3, L, B, T, Re_cruise_3, rho_w, nu_w)

t_range = np.linspace(1, t_total_3, 500)
profiles_3 = np.empty((2, len(t_range)))
profiles_3[0, :] = t_range

for pos, time in enumerate(t_range):
    if time <= t_u_a_3:
        profiles_3[1, pos] = P_m
    elif time <= (t_total_3 - t_u_d_3):
        profiles_3[1, pos] = P_cruise_3
    else:
        profiles_3[1, pos] = P_m

E_run_3 = simpson(profiles_3[1, :], profiles_3[0, :])
E_bats = utilities.temp_cap(E_bat, Temp_range)

E_run_3 = np.array(E_run_3)
E_run_3 /= 3600  # Wh
E_run_3 /= 1e6  # MWh
N_runs_3 = E_bats / E_run_3
t_ends_3 = N_runs_3 * t_total_3  # s
t_ends_3 /= 3600  # h

ax_temp.plot(Temp_range, t_ends_3)
ax_temp.set_xlabel("Ambient Temperature [°C]")
ax_temp.set_ylabel("Endurance [h]")
ax_temp.grid()

fig_temp.savefig(
    "/home/matth/Documents/Lboro/MBSE/VV/CW2/REPORT/UTIL/FIGS/temp-sense.png", dpi=300
)


# Varying Battery Capacity

hull_xs_4, hull_ys_4 = utilities.hull_profile_gen(k_i, B, T, 500)
A_M_4 = (T * B) - simpson(hull_ys_4, hull_xs_4)
V_d_4 = A_M_4 * L

t_u_a_4, a_bar_a_4 = utilities.acceleration_time(
    u_initial,
    u_cruise,
    500,
    P_m,
    V_d_4,
    L,
    B,
    T,
    (V_d_4 * rho_w),
    rho_w,
    nu_w,
)

t_u_d_4, a_bar_d_4 = utilities.acceleration_time(
    u_cruise,
    u_initial,
    500,
    P_m,
    V_d_4,
    L,
    B,
    T,
    (V_d_4 * rho_w),
    rho_w,
    nu_w,
    mode=2,
)

s_to_u_max_4 = (u_initial * t_u_a_4) + (0.5 * a_bar_a_4 * t_u_a_4**2)
s_from_u_max_4 = (u_cruise * t_u_d_4) + (0.5 * a_bar_d_4 * t_u_d_4**2)
s_cruise = 300 - s_to_u_max_4 - s_from_u_max_4

t_cruise_4 = s_cruise / (u_cruise)
t_total_4 = t_u_a_4 + t_u_d_4 + t_cruise_4

Re_cruise_4 = (L * u_cruise) / nu_w
P_cruise_4 = utilities.drag_power(V_d_4, L, B, T, Re_cruise_4, rho_w, nu_w)

t_range = np.linspace(1, t_total_4, 500)
profiles_4 = np.empty((2, len(t_range)))
profiles_4[0, :] = t_range

for pos, time in enumerate(t_range):
    if time <= t_u_a_4:
        profiles_4[1, pos] = P_m
    elif time <= (t_total_4 - t_u_d_4):
        profiles_4[1, pos] = P_cruise_4
    else:
        profiles_4[1, pos] = P_m

E_run_4 = simpson(profiles_4[1, :], profiles_4[0, :])

E_run_4 = np.array(E_run_4)
E_run_4 /= 3600  # Wh
E_run_4 /= 1e6  # MWh
N_runs_4 = E_bat_range / E_run_4
t_ends_4 = N_runs_4 * t_total_4  # s
t_ends_4 /= 3600  # h
masses = E_bat_range / rho_bat  # kg
masses /= 1000  # tonnes

ax_batcap.plot(E_bat_range, t_ends_4, label="Endurance Trend")
ax_batcap.plot(E_bat_range, masses, label="Mass Trend")
ax_batcap.set_xlabel("Nominal Battery Capacity [MWh]")
ax_batcap.set_ylabel("Endurance [h]")
ax_batcap.legend()
ax5_1 = ax_batcap.twinx()
ax5_1.set_ylabel("Battery Mass [Tonnes]")
ax_batcap.grid()

fig_batcap.savefig(
    "/home/matth/Documents/Lboro/MBSE/VV/CW2/REPORT/UTIL/FIGS/temp-batcap.png", dpi=300
)

plt.show()
