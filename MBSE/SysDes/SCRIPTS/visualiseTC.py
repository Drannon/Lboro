"""Visualise the effect of the Design Variables on the Design Objective()."""

import numpy as np
import pandas as pd
import pydoe as doe
import designEnablers as de
import util

## CONSTANTS

# Physical
rho_w = 1000  # kg/m3
rho_steel = 7850  # kg/m3, Grade S355G5

# Design
draught = 1.2  # m
beam = 25  # m
turnSpeed = 0.7 * ut.kt2ms(8)  # m/s, % of cruising speed
price_steel = 25  # £/kg, approximate for Grade S355G5
deck_thickness = 10  # mm

## DESIGN VARIABLES
LPP_range = [60, 80]  # m
rudder_chord_range = [1.5 * draught, 3 * draught]  # m
rudder_span_range = [0.8 * draught, draught]  # m
rudder_deflection_range = [20, 35]  # degrees
thruster_power_range = [5, 50]  # kW
hull_control_point_range = [0, 1]  # % of draught
hull_thickness_range = [5, 10]  # mm

## Conversions
# Convert rudder deflections to radians
rudder_deflection_rad_range = [util.deg2rad(i) for i in rudder_deflection_range]


## DoE
# Number of samples
n_sample = 50;

# Generate sampels using Latin Hypercube Sampling
lhs_samples = doe.lhs(6, nSample)

# Scale samples to match variable ranges
LPP_samples = LPP_range[0] + lhs_samples[:,0] * (LPP_range[1] - LPP_range[0])
rudder_chord_samples = rudder_chord_range[0] + lhs_samples[:,1] * (rudder_chord_range[1] - rudder_chord_range[0])
rudder_span_samples = rudder_span_range[0] + lhs_samples[:,2] * (rudder_span_range[1] - rudder_span_range[0])
thruster_power_samples = thruster_power_range[0] + lhs_samples[:,3] * (thruster_power_range[1] - thruster_power_range[0])
hull_control_point_samples = hull_control_point_range[0] + lhs_samples[:,4] * (hull_control_range[1] - hull_control_range[0])
hull_thickness_samples = hull_thickness_range[0] + lhs_samples[:,5] * (hull_thickness_range[1] - hull_thickness_range[0])

# Calculate Wetted Area for 