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
wing_area_range = [25, 50]  # m
form_drag_coeff_range = [0.01, 0.04]  # m
lift_coeff_range = [0.1, 0.8]  # m
fuel_mass_range = [2000, 5000]  # degrees
payload_mass_range = [3000, 7000]  # kW
inlet_area_range = [0.3, 0.6]  # % of draught
fuel_air_ratio_range = [1 / 50, 1 / 150]  # mm
aspect_ratio_range = [2, 4]
thrust_range = [15000, 50000]
cruise_speed_range = [277, 555]

# Conversions

# DoE
# Number of samples
n_sample = 5000

# Generate sampels using Latin Hypercube Sampling
lhs_samples = doe.lhs(10, n_sample)

# Scale samples to match variable ranges
wing_area_samples = wing_area_range[0] + lhs_samples[:, 0] * (
    wing_area_range[1] - wing_area_range[0]
)
form_drag_coeff_samples = form_drag_coeff_range[0] + lhs_samples[:, 1] * (
    form_drag_coeff_range[1] - form_drag_coeff_range[0]
)
lift_coeff_samples = lift_coeff_range[0] + lhs_samples[:, 2] * (
    lift_coeff_range[1] - lift_coeff_range[0]
)
fuel_mass_samples = fuel_mass_range[0] + lhs_samples[:, 3] * (
    fuel_mass_range[1] - fuel_mass_range[0]
)
payload_mass_samples = payload_mass_range[0] + lhs_samples[:, 4] * (
    payload_mass_range[1] - payload_mass_range[0]
)
inlet_area_samples = inlet_area_range[0] + lhs_samples[:, 5] * (
    inlet_area_range[1] - inlet_area_range[0]
)
fuel_air_ratio_samples = fuel_air_ratio_range[0] + lhs_samples[:, 6] * (
    fuel_air_ratio_range[1] - fuel_air_ratio_range[0]
)
aspect_ratio_samples = aspect_ratio_range[0] + lhs_samples[:, 7] * (
    aspect_ratio_range[1] - aspect_ratio_range[0]
)
thrust_samples = thrust_range[0] + lhs_samples[:, 8] * (
    thrust_range[1] - thrust_range[0]
)
cruise_speed_samples = cruise_speed_range[0] + lhs_samples[:, 9] * (
    cruise_speed_range[1] - cruise_speed_range[0]
)

design_variables = [
    wing_area_samples,
    form_drag_coeff_samples,
    lift_coeff_samples,
    fuel_mass_samples,
    payload_mass_samples,
    inlet_area_samples,
    fuel_air_ratio_samples,
    aspect_ratio_samples,
    thrust_samples,
    cruise_speed_samples,
]

# Acceptance
ROC_min = 175

# Calculate the turning circles for the DV samples
sample_ROCs = []

for i in range(n_sample):
    dv_set = [dv[i] for dv in design_variables]
    sample_ROCs.append(de.computeRateOfClimb(dv_set))

# Create dataframe
design_space_dict = {
    "S_w": wing_area_samples,
    "CD0": form_drag_coeff_samples,
    "CL": lift_coeff_samples,
    "m_f": fuel_mass_samples,
    "m_p": payload_mass_samples,
    "A_inlet": inlet_area_samples,
    "f": fuel_air_ratio_samples,
    "AR": aspect_ratio_samples,
    "T": thrust_samples,
    "V": cruise_speed_samples,
    "ROC": sample_ROCs,
}

for item in design_space_dict:
    print(len(design_space_dict[item]))

design_space = pd.DataFrame(data=design_space_dict)
feats = design_space.iloc[:, :-1]
obs = design_space.iloc[:, -1:]


pass_fail = np.where(design_space["ROC"] > ROC_min, "b", "r")

# RSTool
predict = util.rstool(feats, obs)

# print(util.rstool(, sample_turning_circles, ))

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
