import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import use as mpluse
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.optimize import minimize
import designEnablers as de
import util

mpluse("GTK4AGG")

# NUMBER OF GA RUNS

n_runs = 20

# DESIGN VARIABLES
LPP_range = [60, 80]  # m
rudder_chord_range = [1.5 * util.draught, 3 * util.draught]  # m
rudder_span_range = [0.8 * util.draught, util.draught]  # m
rudder_deflection_range = [20, 35]  # degrees
thruster_power_range = [5, 50]  # kW
hull_control_point_range = [0, 1]  # % of draught
hull_thickness_range = [5, 10]  # mm

# Range manipulation
dv_bounds = [
    LPP_range,
    rudder_span_range,
    rudder_chord_range,
    rudder_deflection_range,
    thruster_power_range,
    hull_control_point_range,
    hull_thickness_range,
]

dv_names = ["LPP", "b_R", "c_R", "delta_R", "P_t", "a", "t", "AT"]

dv_uppers = np.array([dvb[1] for dvb in dv_bounds])
dv_lowers = np.array([dvb[0] for dvb in dv_bounds])


class AboutTurnOptimisation(ElementwiseProblem):

    def __init__(self):
        super().__init__(
            n_var=7,
            n_obj=1,
            n_ieq_constr=0,
            xl=dv_lowers,
            xu=dv_uppers,
        )

    def _evaluate(self, x, out, *args, **kwargs):
        turn_time = de.computeAboutTurn60Time(x)
        out["F"] = turn_time


algorithm = GA(pop_size=100)

problem = AboutTurnOptimisation()

data = np.zeros((n_runs, len(dv_names)))

for i in range(n_runs):
    ga_output = minimize(problem, algorithm, termination=("n_gen", 200), verbose=True)
    result = np.append(ga_output.X, ga_output.F[0])
    data[i] = result

optimalResults = pd.DataFrame(data, columns=dv_names)

# Plotting
pd.plotting.scatter_matrix(optimalResults)

plt.show()
