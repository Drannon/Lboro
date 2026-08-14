import numpy as np
import pandas as pd

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


wing_area_range = [46, 48]  # m2
form_drag_coeff_range = [0.01, 0.05]  # dimensionless
max_lift_coeff_range = [1.88, 1.95]  # dimensionless
fuel_mass_range = [5000, 5280]  # kg
payload_mass_range = [1000, 1000]  # kg
aspect_ratio_range = [5, 5]  # dimensionless
thrust_range = [200000, 200000]  # N
TSFC_range = [3e-5, 3e-5]  # kg/Ns
cruise_speed_range = [137, 182]  # m/s


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
    problem,
    algorithm,
    termination=("n_gen", 2000),
    seed=1,
    verbose=True,
)

valid = np.all(result.G <= 0, axis=1)

X_valid = result.X[valid]
F_valid = result.F[valid]
G_valid = result.G[valid]


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


# Only include variables that actually vary.

pareto_designs = pd.DataFrame(
    {
        "Wing Area (m²)": opt_S_ws,
        "CD0": opt_CD0s,
        "CLmax": opt_CL_maxs,
        "Fuel Mass (kg)": opt_m_f_0s,
        "Cruise Speed (m/s)": opt_Vs,
    }
)


# Add objectives as columns too, which is useful for analysis
pareto_results = pareto_designs.copy()

pareto_results["Range (km)"] = opt_Rs
pareto_results["Stall Speed (m/s)"] = opt_VSs
pareto_results["Turn Radius (km)"] = opt_RTs
pareto_results["Rate of Climb (m/s)"] = opt_ROCs

# Give every Pareto solution an ID
pareto_results.insert(
    0,
    "Solution",
    np.arange(len(pareto_results)),
)


print("\nPareto solutions:")
print(pareto_results)

best_range_idx = pareto_results["Range (km)"].idxmax()

print("\nDesign with greatest range:")
print(pareto_results.loc[best_range_idx])

fig = plt.figure(figsize=(9, 7))

ax = fig.add_subplot(111, projection="3d")

scatter = ax.scatter(
    opt_Rs,
    opt_VSs,
    opt_RTs,
    c=opt_ROCs,
    cmap="viridis",
    s=30,
    alpha=0.8,
)

ax.set_xlabel("Maximum Range (km)")
ax.set_ylabel("Stall Speed (m/s)")
ax.set_zlabel("Turn Radius (km)")

cbar = fig.colorbar(
    scatter,
    ax=ax,
    pad=0.1,
)

cbar.set_label("Rate of Climb (m/s)")

ax.set_title("Pareto Front")

variables = pareto_designs.columns
n_variables = len(variables)

fig, axes = plt.subplots(
    n_variables,
    n_variables,
    figsize=(15, 15),
)


for i, y_var in enumerate(variables):
    for j, x_var in enumerate(variables):
        ax = axes[i, j]

        if i == j:

            ax.hist(
                pareto_designs[x_var],
                bins=15,
                color="blue",
                edgecolor="black",
            )

        else:

            scatter = ax.scatter(
                pareto_designs[x_var],
                pareto_designs[y_var],
                c=opt_Rs,
                cmap="viridis",
                s=30,
                alpha=0.75,
                edgecolors="none",
            )

        if i == n_variables - 1:
            ax.set_xlabel(
                x_var,
                fontsize=10,
            )

        else:
            ax.set_xlabel("")

        if j == 0:
            ax.set_ylabel(
                y_var,
                fontsize=10,
            )

        else:
            ax.set_ylabel("")

        ax.grid(
            alpha=0.2,
            linestyle="--",
        )


fig.colorbar(
    scatter,
    ax=axes,
    label="Maximum Range (km)",
    shrink=0.5,
    # pad=0.02,
)

plt.show()
