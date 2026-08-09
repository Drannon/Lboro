import numpy as np
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.optimize import minimize
import designEnablers as de
import util

# DESIGN VARIABLES
wing_area_range = [25, 50]  # m2
form_drag_coeff_range = [0.01, 0.05]  # dimensionless
max_lift_coeff_range = [0.1, 0.9]  # dimensionless
base_fuel_mass_range = [2000, 5000]  # kg
payload_mass_range = [3000, 7000]  # kg
aspect_ratio_range = [2, 6]  # dimensionless
thrust_range = [30000, 100000]  # N
TSFC_range = [2.3e-5, 4.9e-5]  # kg/Ns
cruise_speed_range = [200, 340]  # m/s

# Range manipulation
dv_bounds = [
    wing_area_range,
    form_drag_coeff_range,
    max_lift_coeff_range,
    base_fuel_mass_range,
    payload_mass_range,
    aspect_ratio_range,
    thrust_range,
    TSFC_range,
    cruise_speed_range,
]

dv_uppers = np.array([dvb[1] for dvb in dv_bounds])
dv_lowers = np.array([dvb[0] for dvb in dv_bounds])


class ROCOptimisation(ElementwiseProblem):

    def __init__(self):
        super().__init__(
            n_var=9,
            n_obj=1,
            n_ieq_constr=0,
            xl=dv_lowers,
            xu=dv_uppers,
        )

    def _evaluate(self, x, out, *args, **kwargs):
        opt_ROC = de.computeRateOfClimb(x)
        out["F"] = -opt_ROC


algorithm = GA(pop_size=100)

problem = ROCOptimisation()

result = minimize(problem, algorithm, termination=("n_gen", 200), seed=1, verbose=True)

print(result.X)
print(-result.F)
