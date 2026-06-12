"""Visualise the effect of the Design Variables on the Design Objective()."""

import numpy as np
import pandas as pd
import util as ut

## CONSTANTS

# Physical
rho_w = 1000  # kg/m3

# Design
draught = 1.2  # m
beam = 25  # m
turnSpeed = 0.7 * ut.kt2ms(8)  # m/s, % of cruising speed

## DESIGN VARIABLES
rudder_chord = []  # m
rudder_span = []  # m
thruster_power = []  # kW
LPP = [0, 60]  # m
hullCtlPt = [0, 1]  # % of draught
hull_thickness = [0, 1]  # mm
