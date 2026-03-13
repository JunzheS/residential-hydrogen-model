import numpy as np
import matplotlib.pyplot as plt
from hydrogen_model import run_model


def electricity_price_sensitivity():

    prices = np.linspace(0.05,0.4,30)

    LCOH_values = []

    for p in prices:

        LCOH_values.append(p*10)

    plt.plot(prices,LCOH_values)

    plt.xlabel("Electricity price €/kWh")
    plt.ylabel("LCOH €/kg")

    plt.title("Electricity price sensitivity")

    plt.show()