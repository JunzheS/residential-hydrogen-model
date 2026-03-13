import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

from hydrogen_model import run_model

st.title("Residential Hydrogen Energy Model")

results = run_model()

st.subheader("System results")

st.write("PV generation:",results["PV_generation"],"kWh/year")

st.write("PV area:",round(results["PV_area"],1),"m²")

st.write("Hydrogen production:",round(results["hydrogen_production"],2),"kg/year")

st.write("Hydrogen needed for heating:",round(results["hydrogen_required"],2),"kg")

st.write("Tank volume:",round(results["storage_volume"],2),"m³")

st.write("LCOH:",round(results["LCOH"],2),"€/kg")

st.write("Hydrogen heat cost:",round(results["heat_cost_H2"],3),"€/kWh")

st.write("Gas heat cost:",round(results["heat_cost_gas"],3),"€/kWh")


st.subheader("Sensitivity example")

prices = np.linspace(0.05,0.4,30)

LCOH_curve = prices*10

fig, ax = plt.subplots()

ax.plot(prices,LCOH_curve)

ax.set_xlabel("Electricity price €/kWh")
ax.set_ylabel("LCOH €/kg")

st.pyplot(fig)