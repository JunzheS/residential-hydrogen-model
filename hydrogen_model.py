"""
Residential Hydrogen Energy System Model
----------------------------------------

Purpose:
Techno-economic analysis of residential hydrogen energy systems
(PV + Electrolyser + Hydrogen storage + Hydrogen heating)

Author: Portfolio project
"""

import numpy as np


# =====================================================
# SYSTEM PARAMETERS
# =====================================================

# ----- PV SYSTEM -----

PV_capacity = 5                # kW installed PV capacity
PV_yield = 1100                # kWh/kW/year solar production

panel_efficiency = 0.20        # PV panel efficiency


# ----- HOUSE DEMAND -----

electricity_demand = 3500      # kWh/year household electricity
heating_demand = 10000         # kWh/year heating demand


# ----- ELECTROLYSER -----

electrolyser_capacity = 3      # kW

electrolyser_efficiency = 52   # kWh electricity per kg hydrogen

operating_hours = 2000         # hours per year electrolyser operation


# ----- HYDROGEN STORAGE -----

tank_capacity = 200            # kg hydrogen storage capacity
tank_CAPEX = 3000              # €


# ----- HYDROGEN BOILER -----

boiler_efficiency = 0.9        # hydrogen boiler efficiency


# ----- COST PARAMETERS -----

PV_CAPEX = 6000
electrolyser_CAPEX = 5000
boiler_CAPEX = 1500

OPEX = 300

discount_rate = 0.07
system_lifetime = 20
stack_lifetime = 8


# ----- ENERGY PRICES -----

electricity_price = 0.25       # €/kWh
gas_price = 0.10               # €/kWh
feed_in_tariff = 0.08          # €/kWh


# ----- EMISSION FACTORS -----

EF_grid = 0.3                  # kg CO2/kWh electricity
EF_gas = 0.202                 # kg CO2/kWh gas
EF_hydrogen = 1.5              # kg CO2/kg hydrogen


# Hydrogen properties
LHV_H2 = 33.33                 # kWh/kg hydrogen


# =====================================================
# PV AREA CALCULATION
# =====================================================

def pv_area_required(PV_capacity_kw, efficiency=0.20):
    """
    Calculate PV installation area.

    PV_capacity_kw : installed PV capacity
    efficiency : PV module efficiency
    """

    PV_power_w = PV_capacity_kw * 1000

    area = PV_power_w / (efficiency * 1000)

    return area


# =====================================================
# HYDROGEN PRODUCTION MODEL
# =====================================================

def hydrogen_production_model():

    """
    Calculate hydrogen production considering electrolyser capacity.
    """

    PV_generation = PV_capacity * PV_yield

    surplus_electricity = max(0, PV_generation - electricity_demand)

    max_electricity = electrolyser_capacity * operating_hours

    electricity_used = min(surplus_electricity, max_electricity)

    hydrogen = electricity_used / electrolyser_efficiency

    return hydrogen, PV_generation, surplus_electricity


# =====================================================
# HYDROGEN REQUIRED FOR HEATING
# =====================================================

def hydrogen_required_for_heating():

    H_required = heating_demand / (LHV_H2 * boiler_efficiency)

    return H_required


# =====================================================
# HYDROGEN STORAGE VOLUME
# =====================================================

def hydrogen_storage_volume(hydrogen_mass, density=23):

    """
    Calculate hydrogen storage volume

    density default = 23 kg/m3 (350 bar)
    """

    volume = hydrogen_mass / density

    return volume


# =====================================================
# STACK REPLACEMENT COST
# =====================================================

def stack_replacement_cost():

    replacements = int(system_lifetime / stack_lifetime)

    cost = replacements * electrolyser_CAPEX * 0.4

    return cost


# =====================================================
# LCOH CALCULATION
# =====================================================

def calculate_LCOH(hydrogen_production):

    def CRF(r,n):
        return r*(1+r)**n/((1+r)**n-1)

    crf = CRF(discount_rate,system_lifetime)

    replacement_cost = stack_replacement_cost()

    total_capex = PV_CAPEX + electrolyser_CAPEX + tank_CAPEX + boiler_CAPEX

    annual_capex = (total_capex + replacement_cost) * crf

    electricity_cost = feed_in_tariff * hydrogen_production * electrolyser_efficiency

    LCOH = (annual_capex + OPEX + electricity_cost) / hydrogen_production

    return LCOH


# =====================================================
# HEATING COST
# =====================================================

def heating_costs(LCOH):

    heat_cost_H2 = LCOH / (LHV_H2 * boiler_efficiency)

    gas_boiler_efficiency = 0.9

    heat_cost_gas = gas_price / gas_boiler_efficiency

    return heat_cost_H2, heat_cost_gas


# =====================================================
# MAIN MODEL EXECUTION
# =====================================================

def run_model(
    PV_capacity,
    electricity_demand,
    heating_demand,
    electricity_price,
    gas_price,
    electrolyser_efficiency
):

    PV_yield = 1100
    boiler_efficiency = 0.9
    LHV_H2 = 33.33

    PV_generation = PV_capacity * PV_yield

    surplus = max(0, PV_generation - electricity_demand)

    hydrogen_production = surplus / electrolyser_efficiency

    heat_from_h2 = hydrogen_production * LHV_H2 * boiler_efficiency

    heat_cost_H2 = electricity_price * electrolyser_efficiency / (LHV_H2*boiler_efficiency)

    heat_cost_gas = gas_price / 0.9

    results = {

        "PV_generation": PV_generation,
        "hydrogen_production": hydrogen_production,
        "heat_from_h2": heat_from_h2,
        "heat_cost_H2": heat_cost_H2,
        "heat_cost_gas": heat_cost_gas

    }

    return results


if __name__ == "__main__":

    results = run_model()

    print(results)
