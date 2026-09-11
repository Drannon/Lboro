"""Visualise the effect of the Design Variables on the Design Objective()."""

import numpy as np
import pandas as pd
import pydoe as doe
import designEnablers as de
import util
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("gtk4agg")

# DESIGN VARIABLES
wing_area_range = [20, 60]  # m2
form_drag_coeff_range = [0.01, 0.05]  # dimensionless
max_lift_coeff_range = [1, 2]  # dimensionless
fuel_mass_range = [3500, 6500]  # kg
payload_mass_range = [1000, 4000]  # kg
aspect_ratio_range = [2.5, 5]  # dimensionless
thrust_range = [100000, 200000]  # N
TSFC_range = [2e-5, 5e-5]  # kg/Ns
cruise_speed_range = [136, 272]  # m/s

# Conversions

# DoE
# Number of samples
n_sample = 1000

# Generate sampels using Latin Hypercube Sampling
lhs_samples = doe.lhs(9, n_sample)

# Scale samples to match variable ranges
wing_area_samples = wing_area_range[0] + lhs_samples[:, 0] * (
    wing_area_range[1] - wing_area_range[0]
)
form_drag_coeff_samples = form_drag_coeff_range[0] + lhs_samples[:, 1] * (
    form_drag_coeff_range[1] - form_drag_coeff_range[0]
)
max_lift_coeff_samples = max_lift_coeff_range[0] + lhs_samples[:, 2] * (
    max_lift_coeff_range[1] - max_lift_coeff_range[0]
)
fuel_mass_samples = fuel_mass_range[0] + lhs_samples[:, 3] * (
    fuel_mass_range[1] - fuel_mass_range[0]
)
payload_mass_samples = payload_mass_range[0] + lhs_samples[:, 4] * (
    payload_mass_range[1] - payload_mass_range[0]
)
aspect_ratio_samples = aspect_ratio_range[0] + lhs_samples[:, 5] * (
    aspect_ratio_range[1] - aspect_ratio_range[0]
)
thrust_samples = thrust_range[0] + lhs_samples[:, 6] * (
    thrust_range[1] - thrust_range[0]
)
TSFC_samples = TSFC_range[0] + lhs_samples[:, 7] * (TSFC_range[1] - TSFC_range[0])
cruise_speed_samples = cruise_speed_range[0] + lhs_samples[:, 8] * (
    cruise_speed_range[1] - cruise_speed_range[0]
)

design_variables = [
    wing_area_samples,
    form_drag_coeff_samples,
    max_lift_coeff_samples,
    fuel_mass_samples,
    payload_mass_samples,
    aspect_ratio_samples,
    thrust_samples,
    TSFC_samples,
    cruise_speed_samples,
]

# Acceptance
V_stall_max = util.kt2ms(80)  # F-5

# Calculate the turning circles for the DV samples
sample_stall_speeds = []

for i in range(n_sample):
    dv_set = [dv[i] for dv in design_variables]
    sample_stall_speeds.append(de.computeVstall(dv_set))

# Create dataframe
design_space_dict = {
    "S_w[m2]": wing_area_samples,
    "CD0": form_drag_coeff_samples,
    "CL_max": max_lift_coeff_samples,
    "m_f[kg]": fuel_mass_samples,
    "m_p[kg]": payload_mass_samples,
    "AR": aspect_ratio_samples,
    "T[N]": thrust_samples,
    "TSFC[kg/Ns]": TSFC_samples,
    "V[m/s]": cruise_speed_samples,
    "VStall[m/s]": sample_stall_speeds,
}

design_space = pd.DataFrame(data=design_space_dict)
feats = design_space.iloc[:, :-1]
obs = design_space.iloc[:, -1:]

pass_fail = np.where(design_space["VStall[m/s]"] < V_stall_max, "b", "r")

# RSTool
predict = util.rstool(feats, obs)

# Plotting
pd.plotting.scatter_matrix(design_space, c=pass_fail, alpha=1)

namecol = np.linspace(1, n_sample, n_sample)

ds_normalised = pd.DataFrame()
for col in design_space.columns:
    ds_normalised[col] = design_space[col] / design_space[col].max()

ds_normalised["Iteration"] = namecol
design_space["Iteration"] = namecol
# pd.plotting.parallel_coordinates(ds_normalised, "Iteration", ax=axes[0, 1])
# pd.plotting.parallel_coordinates(design_space, "Iteration")


plt.show()
