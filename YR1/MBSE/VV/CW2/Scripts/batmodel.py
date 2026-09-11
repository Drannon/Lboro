import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("gtk4agg")


def estimateBatteryEfficiency(T_a):
    """Estimates battery efficiency."""
    T_opt = 25
    E_a = []

    for T in T_a:
        if T >= T_opt:
            dT = T - T_opt
            E = 100 - (20 / (20**2)) * dT**2
        else:
            s = 40
            E = 100 * np.exp(-((T - T_opt) ** 2) / (2 * s**2))

        E = max(0, min(E, 100))
        E_a.append(E)
    return E_a


Ts = np.linspace(-40, 50, 1000)

Es = estimateBatteryEfficiency(Ts)

plt.plot(Ts, Es)
plt.grid()
plt.show()
