import numpy as np
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize
from pymoo.operators.sampling.lhs import LHS
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from matplotlib import use as mpluse
import matplotlib.pyplot as plt
import designEnablers as de
import util

mpluse("gtk4agg")

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

dv_uppers = np.array([dvb[1] for dvb in dv_bounds])
dv_lowers = np.array([dvb[0] for dvb in dv_bounds])


class MultipleOptimisation(ElementwiseProblem):

    def __init__(self):
        super().__init__(
            n_var=7,
            n_obj=3,
            n_ieq_constr=0,
            xl=dv_lowers,
            xu=dv_uppers,
        )

    def _evaluate(self, x, out, *args, **kwargs):
        turning_circle = de.computeTurningCircle(x)
        about_turn = de.computeAboutTurn60Time(x)
        traverse_speed = de.computeTraverseSpeed(x)
        out["F"] = [
            turning_circle,
            about_turn,
            -traverse_speed,
        ]  # use negative to "maximise" with minimise


algorithm = NSGA2(
    pop_size=200,
    sampling=LHS(),
    crossover=SBX(prob=0.9, eta=20),
    mutation=PM(prob=(1 / 7), eta=20),
    eliminate_duplicates=True,
)

problem = MultipleOptimisation()

result = minimize(
    problem, algorithm, termination=("n_gen", 1000), seed=1, verbose=True
)  # return optimised value to positive

print(result.X)
print(result.F)

opt_LPPs = [front_point[0] for front_point in result.X]
opt_b_Rs = [front_point[1] for front_point in result.X]
opt_c_Rs = [front_point[2] for front_point in result.X]
opt_delta_Rs = [front_point[3] for front_point in result.X]
opt_P_ts = [front_point[4] for front_point in result.X]
opt_as = [front_point[5] for front_point in result.X]
opt_ts = [front_point[6] for front_point in result.X]

opt_tcs = [front_point[0] for front_point in result.F]
opt_ats = [front_point[1] for front_point in result.F]
opt_tss = [-front_point[2] for front_point in result.F]

# Create figure and 3D axes
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection="3d")

# Scatter plot
ax.scatter(opt_tcs, opt_ats, opt_tss)

# Labels
ax.set_xlabel("Turning Circle (m)")
ax.set_ylabel("About Turn time through 60 deg (s)")
ax.set_zlabel("Traverse Speed (kts)")
ax.set_title("Pareto Front")

plt.show()
