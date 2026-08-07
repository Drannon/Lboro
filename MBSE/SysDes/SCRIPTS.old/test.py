import numpy as np
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.optimize import minimize


def testFunc(x):
    f = (x[0] - 2) ** 2 + (x[1] + 1) ** 2
    return f


class MyProblem(ElementwiseProblem):

    def __init__(self):
        super().__init__(
            n_var=2,
            n_obj=1,
            n_ieq_constr=0,
            xl=np.array([-5, 5]),
            xu=np.array([5, 5]),
        )

    def _evaluate(self, x, out, *args, **kwargs):
        output = testFunc(x)
        out["F"] = output


algorithm = GA(pop_size=100)

problem = MyProblem()

result = minimize(problem, algorithm, termination=("n_gen", 200), seed=1, verbose=True)

print(result.X)
print(result.F)
