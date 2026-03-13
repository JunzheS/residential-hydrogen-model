import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from hydrogen_model import run_model


st.title("Residential Hydrogen Energy System Model")


# -----------------------------
# USER INPUT
# -----------------------------

st.sidebar.header("System parameters")

PV_capacity = st.sidebar.slider("PV capacity (kW)",1,20,5)

electricity_demand = st.sidebar.slider("Electricity demand (kWh/year)",1000,8000,3500)

heating_demand = st.sidebar.slider("Heating demand (kWh/year)",2000,20000,10000)

electricity_price = st.sidebar.slider("Electricity price €/kWh",0.05,0.40,0.25)

gas_price = st.sidebar.slider("Gas price €/kWh",0.05,0.30,0.10)

electrolyser_efficiency = st.sidebar.slider("Electrolyser consumption (kWh/kg)",45,60,52)


# -----------------------------
# RUN MODEL
# -----------------------------

results = run_model(
    PV_capacity,
    electricity_demand,
    heating_demand,
    electricity_price,
    gas_price,
    electrolyser_efficiency
)


# -----------------------------
# RESULTS
# -----------------------------

st.header("System results")

st.write("PV generation:",round(results["PV_generation"],1),"kWh/year")

st.write("Hydrogen production:",round(results["hydrogen_production"],2),"kg/year")

st.write("Heat from hydrogen:",round(results["heat_from_h2"],1),"kWh/year")

st.write("Hydrogen heat cost:",round(results["heat_cost_H2"],3),"€/kWh")

st.write("Gas heat cost:",round(results["heat_cost_gas"],3),"€/kWh")


# -----------------------------
# PV AREA
# -----------------------------

panel_efficiency = 0.20

PV_area = (PV_capacity*1000)/(panel_efficiency*1000)

st.write("Required PV area:",round(PV_area,1),"m²")


# -----------------------------
# STORAGE ANALYSIS
# -----------------------------

LHV_H2 = 33.33

boiler_efficiency = 0.9

H_required = heating_demand/(LHV_H2*boiler_efficiency)

st.write("Hydrogen required for heating:",round(H_required,1),"kg")


density = 23

volume = H_required/density

st.write("Tank volume (350 bar):",round(volume,2),"m³")


# -----------------------------
# ELECTRICITY PRICE SENSITIVITY
# -----------------------------

st.header("Electricity price sensitivity")

prices = np.linspace(0.05,0.4,40)

heat_cost_curve = []

for p in prices:

    r = run_model(
        PV_capacity,
        electricity_demand,
        heating_demand,
        p,
        gas_price,
        electrolyser_efficiency
    )

    heat_cost_curve.append(r["heat_cost_H2"])


fig, ax = plt.subplots()

ax.plot(prices,heat_cost_curve)

ax.set_xlabel("Electricity price €/kWh")

ax.set_ylabel("Hydrogen heating cost €/kWh")

st.pyplot(fig)


# -----------------------------
# PV SIZE SENSITIVITY
# -----------------------------

st.header("PV size vs hydrogen production")

PV_sizes = np.linspace(1,20,20)

hydrogen_curve = []

for pv in PV_sizes:

    r = run_model(
        pv,
        electricity_demand,
        heating_demand,
        electricity_price,
        gas_price,
        electrolyser_efficiency
    )

    hydrogen_curve.append(r["hydrogen_production"])


fig2, ax2 = plt.subplots()

ax2.plot(PV_sizes,hydrogen_curve)

ax2.set_xlabel("PV size (kW)")

ax2.set_ylabel("Hydrogen production (kg/year)")

st.pyplot(fig2)


# -----------------------------
# HYDROGEN COMPETITIVENESS MAP
# -----------------------------

st.header("Hydrogen competitiveness map")

electricity_prices = np.linspace(0.05,0.4,40)

gas_prices = np.linspace(0.05,0.25,40)

premium = np.zeros((40,40))


for i,g in enumerate(gas_prices):

    for j,e in enumerate(electricity_prices):

        r = run_model(
            PV_capacity,
            electricity_demand,
            heating_demand,
            e,
            g,
            electrolyser_efficiency
        )

        premium[i,j] = r["heat_cost_H2"] - r["heat_cost_gas"]


fig3, ax3 = plt.subplots()

im = ax3.imshow(
    premium,
    extent=[electricity_prices.min(),
            electricity_prices.max(),
            gas_prices.min(),
            gas_prices.max()],
    origin="lower",
    aspect="auto",
    cmap="coolwarm"
)

plt.colorbar(im,label="Green premium €/kWh")

ax3.set_xlabel("Electricity price €/kWh")

ax3.set_ylabel("Gas price €/kWh")

st.pyplot(fig3)
