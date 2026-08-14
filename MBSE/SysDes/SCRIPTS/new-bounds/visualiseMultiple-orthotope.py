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
# wing_area_range = [31, 58]  # m2  ROUND 1
# wing_area_range = [45, 58]  # m2 ROUND 4
# wing_area_range = [45, 48]  # m2 ROUND 4
wing_area_range = [46, 48]  # m2 ROUND 5
form_drag_coeff_range = [0.03, 0.03]  # dimensionless
# max_lift_coeff_range = [1.64, 1.95]  # dimensionless ROUND 3
max_lift_coeff_range = [1.88, 1.95]
# fuel_mass_range = [3070, 6500]  # kg  ROUND 1
# fuel_mass_range = [4600, 6000]  # kg ROUND 2
fuel_mass_range = [5000, 5280]  # kg ROUND 2
payload_mass_range = [1000, 1000]  # kg
aspect_ratio_range = [5, 5]  # dimensionless
thrust_range = [200000, 200000]  # N
TSFC_range = [3e-5, 3e-5]  # kg/Ns
# cruise_speed_range = [137, 193]  # m/s ROUND 6
cruise_speed_range = [137, 182]  # m/s

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
R_min = 1500
v_stall_min = util.kt2ms(80)
r_turn_max = 400
ROC_min = 150


# Calculate the turning circles for the DV samples
sample_ranges = []
sample_stall_speeds = []
sample_turn_radii = []
sample_ROCs = []

for i in range(n_sample):
    dv_set = [dv[i] for dv in design_variables]
    sample_ranges.append(de.computeRange(dv_set))
    sample_stall_speeds.append(de.computeVstall(dv_set))
    sample_turn_radii.append(de.computeTurnRadius(dv_set))
    sample_ROCs.append(de.computeRateOfClimb(dv_set))

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
    "R[km]": sample_ranges,
    "VStall[m/s]": sample_stall_speeds,
    "rTurn[m]": sample_turn_radii,
    "ROC[m/s]": sample_ROCs,
}


design_space = pd.DataFrame(data=design_space_dict)
design_space_invalid = design_space[
    design_space["rTurn[m]"].isna()
].copy()  # keep track of invalid combinations
design_space = design_space[
    design_space["rTurn[m]"].notna()
].copy()  # valid combinations

feats = design_space.iloc[:, :-4]
obs = design_space.iloc[:, -4:]

pass_fail = np.where(
    (design_space["R[km]"] > R_min)
    & (design_space["VStall[m/s]"] < v_stall_min)
    & (design_space["rTurn[m]"] < r_turn_max)
    & (design_space["ROC[m/s]"] > ROC_min),
    "b",
    "r",
)

# RSTool
predict = util.rstool(feats, obs, n_obs=4)

# Plotting
pd.plotting.scatter_matrix(design_space, c=pass_fail, alpha=1)


plt.show()
