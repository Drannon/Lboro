import numpy as np
from pydoe import lhs
from util import rstool
import matplotlib.pyplot as plt


def test_func(xs):
    x1, x2, x3 = xs
    return x1**2 + x2 * x1 + x3


sample = lhs(3, 100)
print(np.shape(sample)[1])
observations = test_func(np.transpose(sample))

print(rstool(sample, observations, [0.4, 0.3, 0.5]))

plt.show()
