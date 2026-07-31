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
LPP_range = [60, 80]  # m
rudder_chord_range = [1.5 * util.draught, 3 * util.draught]  # m
rudder_span_range = [0.8 * util.draught, util.draught]  # m
rudder_deflection_range = [20, 35]  # degrees
thruster_power_range = [5, 50]  # kW
hull_control_point_range = [0, 1]  # % of draught
hull_thickness_range = [5, 10]  # mm

# Conversions
# Convert rudder deflections to radians
rudder_deflection_rad_range = [
    util.deg2rad(i) for i in rudder_deflection_range
]  # think about using this for calc but not display


# DoE
# Number of samples
n_sample = 5000

# Generate sampels using Latin Hypercube Sampling
lhs_samples = doe.lhs(7, n_sample)

# Scale samples to match variable ranges
LPP_samples = LPP_range[0] + lhs_samples[:, 0] * (LPP_range[1] - LPP_range[0])
rudder_chord_samples = rudder_chord_range[0] + lhs_samples[:, 1] * (
    rudder_chord_range[1] - rudder_chord_range[0]
)
rudder_span_samples = rudder_span_range[0] + lhs_samples[:, 2] * (
    rudder_span_range[1] - rudder_span_range[0]
)
rudder_deflection_samples = rudder_deflection_rad_range[0] + lhs_samples[:, 3] * (
    rudder_deflection_rad_range[1] - rudder_deflection_rad_range[0]
)
thruster_power_samples = thruster_power_range[0] + lhs_samples[:, 4] * (
    thruster_power_range[1] - thruster_power_range[0]
)
hull_control_point_samples = hull_control_point_range[0] + lhs_samples[:, 5] * (
    hull_control_point_range[1] - hull_control_point_range[0]
)
hull_thickness_samples = hull_thickness_range[0] + lhs_samples[:, 6] * (
    hull_thickness_range[1] - hull_thickness_range[0]
)

design_variables = [
    LPP_samples,
    rudder_span_samples,
    rudder_chord_samples,
    rudder_deflection_samples,
    thruster_power_samples,
    hull_control_point_samples,
    hull_thickness_samples,
]

# Acceptance
r_TC_max_samples = LPP_samples * 4

# Calculate the turning circles for the DV samples
sample_turning_circles = []

for i in range(n_sample):
    dv_set = [dv[i] for dv in design_variables]
    sample_turning_circles.append(de.computeTurningCircle(dv_set))

# Create dataframe
design_space_dict = {
    "LPP": LPP_samples,
    "b_R": rudder_span_samples,
    "c_R": rudder_chord_samples,
    "delta_R": util.rad2deg(rudder_deflection_samples),
    "P_t": thruster_power_samples,
    "a": hull_control_point_samples,
    "t": hull_thickness_samples,
    "r_TC": sample_turning_circles,
}

design_space = pd.DataFrame(data=design_space_dict)
feats = design_space.iloc[:, :-1]
obs = design_space.iloc[:, -1:]


pass_fail = np.where(design_space["r_TC"] < r_TC_max_samples, "b", "r")

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
