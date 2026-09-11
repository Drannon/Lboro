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
wing_area_range = [20, 60]  # m2
form_drag_coeff_range = [0.01, 0.05]  # dimensionless
max_lift_coeff_range = [1, 2]  # dimensionless
fuel_mass_range = [3500, 6500]  # kg
payload_mass_range = [1000, 4000]  # kg
aspect_ratio_range = [2.5, 5]  # dimensionless
thrust_range = [100000, 200000]  # N
TSFC_range = [2e-5, 5e-5]  # kg/Ns
cruise_speed_range = [136, 272]  # m/s

# Range manipulation
dv_bounds = [
    wing_area_range,
    form_drag_coeff_range,
    max_lift_coeff_range,
    fuel_mass_range,
    payload_mass_range,
    aspect_ratio_range,
    thrust_range,
    TSFC_range,
    cruise_speed_range,
]

dv_uppers = np.array([dvb[1] for dvb in dv_bounds])
dv_lowers = np.array([dvb[0] for dvb in dv_bounds])


class MultipleOptimisation(ElementwiseProblem):

    def __init__(self):
        super().__init__(
            n_var=9,
            n_obj=4,
            n_ieq_constr=5,
            xl=dv_lowers,
            xu=dv_uppers,
        )

    def _evaluate(self, x, out, *args, **kwargs):
        opt_range = de.computeRange(x)
        opt_VStall = de.computeVstall(x)
        opt_RTurn = de.computeTurnRadius(x)
        opt_ROC = de.computeRateOfClimb(x)

        if np.isnan(opt_RTurn):
            out["G"] = [
                1500 - opt_range,
                opt_VStall - util.kt2ms(200),
                1.0,
                1.0,
                100 - opt_ROC,
            ]
            out["F"] = [
                -opt_range,
                opt_VStall,
                1e10,
                -opt_ROC,
            ]

        else:
            out["G"] = [
                1500 - opt_range,
                opt_VStall - util.kt2ms(200),
                0.0,
                opt_RTurn - 2000,
                100 - opt_ROC,
            ]
            out["F"] = [
                -opt_range,
                opt_VStall,
                opt_RTurn,
                -opt_ROC,
            ]


algorithm = NSGA2(
    pop_size=200,
    sampling=LHS(),
    crossover=SBX(prob=0.9, eta=20),
    mutation=PM(prob=(1 / 7), eta=20),
    eliminate_duplicates=True,
)

problem = MultipleOptimisation()

result = minimize(
    problem, algorithm, termination=("n_gen", 2000), seed=1, verbose=True
)  # return optimised value to positive

print(result.G)
valid = np.all(result.G <= 0, axis=1)
X_valid = result.X[valid]
F_valid = result.F[valid]

opt_S_ws = X_valid[:, 0]
opt_CD0s = X_valid[:, 1]
opt_CL_maxs = X_valid[:, 2]
opt_m_f_0s = X_valid[:, 3]
opt_m_ps = X_valid[:, 4]
opt_ARs = X_valid[:, 5]
opt_Ts = X_valid[:, 6]
opt_TSFCs = X_valid[:, 7]
opt_Vs = X_valid[:, 8]

opt_Rs = -F_valid[:, 0]
opt_VSs = F_valid[:, 1]
opt_RTs = F_valid[:, 2] / 1000
opt_ROCs = -F_valid[:, 3]

print("G shape:", result.G.shape)
print("G min:", np.min(result.G))
print("G max:", np.max(result.G))
print("Number infeasible:", np.sum(np.any(result.G > 0, axis=1)))

print("\nRTurn:")
print("min:", np.min(result.F[:, 2]))
print("max:", np.max(result.F[:, 2]))

# Create figure and 3D axes
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection="3d")

# Scatter plot
scatter = ax.scatter(opt_Rs, opt_VSs, opt_RTs, c=opt_ROCs, cmap="viridis")


# Labels
ax.set_xlabel("Maximum Range (km)")
ax.set_ylabel("Stall Speed (m/s)")
ax.set_zlabel("Turn Radius (m)")

# Show fourth DO
cbar = fig.colorbar(scatter, ax=ax, pad=0.1)
cbar.set_label("Rate of Climb (m/s)")

ax.set_title("Pareto Front")

plt.show()
