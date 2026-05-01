"""Demonstration test."""

import numpy as np
import pandas as pd
from scipy.constants import g
from scipy.integrate import simpson
from matplotlib import use
import utilities
from utilities import kts2ms

use("gtk4agg")

print("====ROUV Demonstration Test====")

# Constants
rho_w = 1000  # kg/m3 - density of freshwater
nu_w = 1.5e-6  # m2/s - Kinematic viscosity of freshwater

# Specificaitons
L = 60  # m - Length
B = 25  # m - Breadth
T = 1.2  # m - Draught
k = 0.5  # % - Hull Control Point Value
u_max = 12  # kts - Maximum speed
u_cruise = 8  # kts - Cruising speed
u_cruise_ex = 5  # kts - Cruising speed
P_m = 1e6  # W - Motor power
E_bat = 1  # MWh
P_charge = 0.5  # MWh

# Conversion to m/s
u_max = kts2ms(u_max)
u_cruise = kts2ms(u_cruise)
u_crusie_ex = kts2ms(u_cruise_ex)

# Hull Profile
hull_xs, hull_ys = utilities.hull_profile_gen(k, B, T, 1000)

# Non-Dimensional Numbers
Re = (L * u_max) / nu_w
Fr = u_max / np.sqrt(g * L)

print(f"Re = {Re}, Fr = {Fr}")
print("---------------------")

# Geometric Parameters
A_M = (T * B) - simpson(hull_ys, hull_xs)  # m2 - Area amidships
V_d = A_M * L  # Volume of displacement

A_s = 1.025 * ((V_d / T) + 1.7 * L * T)  # m2 - Wetted Area of Hull

# Top Speed Test
P_d_u_max = utilities.drag_power(V_d, L, B, T, Re, rho_w, nu_w)

delta_P_u_max = (
    P_m - P_d_u_max
)  # W - Difference between propulsive power and drag power

if delta_P_u_max >= 0:
    passing = True
elif delta_P_u_max < 0:
    passing = False
else:
    raise (RuntimeError)

print(f"Power surplus = {delta_P_u_max} Watts.")
print(f"Requirement ID 1.1.1.3 Pass: {passing}")
print("--------------------------------------")


# Forward Acceleration
m = V_d * rho_w  # kg - Displacement

t_u_max, a_bar_accel = utilities.acceleration_time(
    1, u_cruise, 1000, P_m, V_d, L, B, T, m, rho_w, nu_w
)

if (t_u_max <= 60) and (t_u_max > 0):
    accel_passing = True
elif t_u_max > 60:
    accel_passing = False
else:
    raise (RuntimeError)

print(f"Time to cruise: {t_u_max} Seconds.")
print(f"Requirement ID 1.1.1.1 Pass: {accel_passing}")
print("--------------------------------------")

# Decceleration
t_u_0, a_bar_decel = utilities.acceleration_time(
    u_cruise, 1, 1000, -P_m, V_d, L, B, T, m, rho_w, nu_w, mode=2
)

if t_u_0 <= 60:
    decel_passing = True
elif t_u_max > 60:
    decel_passing = False
else:
    raise (RuntimeError)

print(f"Time to stop: {t_u_0} Seconds.")
print(f"Requirement ID 1.1.1.2 Pass: {decel_passing}")
print("--------------------------------------")

# Power Profile
s_to_u_max = 1 * t_u_max + 0.5 * a_bar_accel * t_u_max**2  # u_0 t + 1/2 a t^2
s_from_u_max = 1 * t_u_0 + 0.5 * a_bar_decel * t_u_0**2
s_cruise = 300 - s_to_u_max - s_from_u_max

t_cruise = s_cruise / u_cruise
t_total = t_u_max + t_cruise + t_u_0

Re_cruise = (L * u_cruise) / nu_w
P_cruise = utilities.drag_power(V_d, L, B, T, Re_cruise, rho_w, nu_w)

t_range = np.linspace(0, t_total, 1000)
profile = pd.DataFrame()
profile["Time"] = t_range
profile["Power"] = None

for pos, time in enumerate(profile["Time"]):
    if time <= t_u_max:
        profile.loc[pos, "Power"] = P_m
    elif time <= (t_total - t_u_0):
        profile.loc[pos, "Power"] = P_cruise
    else:
        profile.loc[pos, "Power"] = P_m

E_run = simpson(profile["Power"], profile["Time"])  # Ws
E_run /= 60**2  # Wh
E_run /= 1e6  # MWh

E_bat_normal = utilities.temp_cap(E_bat, 20)

N_runs = E_bat_normal / E_run
t_end = N_runs * t_total
t_end /= 60**2

if t_end >= 1.5:
    end_passing = True
elif t_end < 1.5:
    end_passing = False

print(f"Endurance: {t_end} hours.")
print(f"Requirement ID 2.1.1 Pass: {end_passing}")
print("--------------------------------------")

# Extreme Endurace
t_u_ex_max, a_bar_ex_accel = utilities.acceleration_time(
    1, u_cruise_ex, 1000, P_m, V_d, L, B, T, m, rho_w, nu_w
)

t_u_ex_0, a_bar_ex_decel = utilities.acceleration_time(
    u_cruise_ex, 1, 1000, -P_m, V_d, L, B, T, m, rho_w, nu_w, mode=2
)

s_to_u_ex_max = 1 * t_u_ex_max + 0.5 * a_bar_ex_accel * t_u_max**2
s_from_u_ex_max = 1 * t_u_ex_0 + 0.5 * a_bar_ex_decel * t_u_0**2
s_cruise_ex = 300 - s_to_u_max - s_from_u_max

t_cruise_ex = s_cruise_ex / u_cruise_ex
t_total_ex = t_u_ex_max + t_cruise_ex + t_u_ex_0

Re_cruise_ex = (L * u_cruise_ex) / nu_w
P_cruise_ex = utilities.drag_power(V_d, L, B, T, Re_cruise, rho_w, nu_w)

profile_ex = pd.DataFrame()
profile_ex["Time"] = t_range
profile_ex["Power"] = None

for pos, time in enumerate(profile_ex["Time"]):
    if time <= t_u_max:
        profile_ex.loc[pos, "Power"] = P_m
    elif time <= (t_total - t_u_0):
        profile_ex.loc[pos, "Power"] = P_cruise_ex
    else:
        profile_ex.loc[pos, "Power"] = P_m

E_run_ex = simpson(profile_ex["Power"], profile_ex["Time"])  # Ws
E_run_ex /= 60**2  # Wh
E_run_ex /= 1e6  # MWh

E_bat_ex = utilities.temp_cap(E_bat, -10)

N_runs_ex = E_bat_ex / E_run_ex
t_end_ex = N_runs_ex * t_total_ex
t_end_ex /= 60**2

print(t_end_ex)
if t_end_ex >= 1:
    end_ex_passing = True
elif t_end_ex < 1:
    end_ex_passing = False
else:
    raise (RuntimeError)
print(f"Extreme Endurance: {t_end_ex} Hours.")
print(f"Requirement ID 2.1.1.1 Pass: {end_ex_passing}")
print("--------------------------------------")

# Charging
charge_range = 0.6 * E_bat
t_charge = charge_range / P_charge

if t_charge <= 1:
    charge_passing = True
elif t_charge > 1:
    charge_passing = False
else:
    raise (RuntimeError)

print(f"Charging Time: {t_charge}")
print(f"Requirement ID 2.2.1 Pass: {charge_passing}")
