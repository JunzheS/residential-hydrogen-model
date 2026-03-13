import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from model.hydrogen_model import run_model


st.title("Residential Hydrogen Energy Model")


# 用户输入参数

PV_capacity = st.slider("PV capacity (kW)",1,20,5)

electricity_demand = st.slider("Electricity demand (kWh/year)",1000,8000,3500)

heating_demand = st.slider("Heating demand (kWh/year)",2000,20000,10000)

electricity_price = st.slider("Electricity price €/kWh",0.05,0.40,0.25)

gas_price = st.slider("Gas price €/kWh",0.05,0.30,0.10)

electrolyser_efficiency = st.slider("Electrolyser consumption (kWh/kg)",45,60,52)

results = run_model(
    PV_capacity,
    electricity_demand,
    heating_demand,
    electricity_price,
    gas_price,
    electrolyser_efficiency
)

st.subheader("Results")

st.write("PV generation:",round(results["PV_generation"],1),"kWh/year")

st.write("Hydrogen production:",round(results["hydrogen_production"],2),"kg/year")

st.write("Heat from hydrogen:",round(results["heat_from_h2"],1),"kWh/year")

st.write("Hydrogen heat cost:",round(results["heat_cost_H2"],3),"€/kWh")

st.write("Gas heat cost:",round(results["heat_cost_gas"],3),"€/kWh")

st.subheader("Electricity price sensitivity")

prices = np.linspace(0.05,0.4,40)

LCOH_curve = []

for p in prices:

    r = run_model(
        PV_capacity,
        electricity_demand,
        heating_demand,
        p,
        gas_price,
        electrolyser_efficiency
    )

    LCOH_curve.append(r["heat_cost_H2"])

fig, ax = plt.subplots()

ax.plot(prices,LCOH_curve)

ax.set_xlabel("Electricity price €/kWh")

ax.set_ylabel("Hydrogen heat cost €/kWh")

st.pyplot(fig)

panel_efficiency = 0.2

PV_area = (PV_capacity*1000)/(panel_efficiency*1000)

st.write("Required PV area:",round(PV_area,1),"m²")


LHV_H2 = 33.33

boiler_efficiency = 0.9

H_required = heating_demand/(LHV_H2*boiler_efficiency)

st.write("Hydrogen needed for heating:",round(H_required,1),"kg")


density = 23

volume = H_required/density

st.write("Hydrogen tank volume:",round(volume,2),"m³")
