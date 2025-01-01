# Coolant Heat Reuse Project

This project demonstrates how to reuse heat from a cooling system in a silicon manufacturing or data-center context. The goal is to capture the otherwise wasted heat from a coolant (like water) and convert or transfer it for useful work—such as heating, low-temperature processes, or even electricity generation.

![Python Version](https://img.shields.io/badge/Python-3.8+-blue.svg)
<!-- ![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg) -->

---

## Table of Contents

- [Coolant Heat Reuse Project](#coolant-heat-reuse-project)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Key Features](#key-features)
  - [Files \& Folders](#files--folders)
  - [Development Log](#development-log)
    - [2024-12-31 – Version 0.1.0](#2024-12-31--version-010)
    - [2025-01-01 – Version 0.2.0](#2025-01-01--version-020)
    - [2025-01-02 - Version 0.3.0](#2025-01-02---version-030)

---

## Overview
This project demonstrates how to reuse heat from a cooling system in a silicon manufacturing. The goal is to capture the otherwise wasted heat from a coolant (like water) and convert or transfer it for useful work—such as heating, low-temperature processes, or even electricity generation.

<!-- In high-intensity computing (such as data centers, or silicon manufacturing processes), the cooling systems generate large amounts of **low-grade heat** (typically around 30 °C). Rather than venting that heat away, this project proposes:
1. Calculating potential **heat recovery** from a reservoir (e.g., water-based coolant at 30 °C).  
2. Exploring **methods** to utilize or convert that heat—like low-temp **Organic Rankine Cycles**, or direct reuse in district heating.  
3. Providing Python-based **simulation scripts** to estimate the feasibility and economics of various approaches.

**Why does this matter?**  
- Energy costs and environmental impact can be reduced by reusing waste heat.  
- It can enable more **sustainable** data centers and manufacturing facilities. -->

---

## Key Features

1. **Thermal Modeling**: Estimate cooling power via convection, involing natural and forced ones.
2. **Benefit Estimation**: Estimate the total energy that could be reused.
3. **Heat Reuse Options**: [TODO] Provide examples of using captured heat for building HVAC, greenhouses, etc.  
4. **Simulation and Charts**: Generate graphs illustrating heat flows and potential power output.

---

## Files & Folders

Below is a simplified flow diagram :
coolant_heat_reuse/
├── heat_transfer.py   # Contains a System class with methods for thermal calculation
├── weather.py   # Contains a Weather class with methods for weather information extraction
├── main.py                # Entry point or script that ties everything together
├── environment.yml       # Dependencies
├── README.md              # Project documentation
└── data/
    ├── air_properties/   # Properties of Air
    │   ├── kinematic_viscosity.csv
    │   ├── thermal_conductivity.csv
    │   ├── thermal_diffusivity.csv
    │   └── thermal_expansion_coefficient.csv
    └── weather.xls  # Weather information

---

## Development Log

### 2024-12-31 – Version 0.1.0
- **Initial repository setup**: Created project structure, added `reference/`, and `data/`.

### 2025-01-01 – Version 0.2.0
- **Feature: System**  
  - Introduced a new `heat_transfer.py` for setting up the thermal system, and calculating the power of heat transferred.
- **Documentation**: Added basic instructions to `README.md`.
- **Data Visualization**: Implemented code to visualize the annual benefit w.r.t. air temperature and wind speed.
- **Results**: Depicted `annual_benefit.png`, indicating the annual benefit with respect to ambient temperature and wind speed.

### 2025-01-02 - Version 0.3.0
- **Feature: Weather**
  - Introduced a new `weather.py` for analyzing local weather information, involving average temperature, wind speed.
- **Feature: Main**
  - Introduced a new `main.py` for invoking functions in `heat_transfer.py` and `weather.py` to estimate seasonal power to be reused based on average temperature and wind speed returned by `weather.py`.
  - Printed out the seasonal information including days, average temperature, wind speed, and heat diffusion estimated power.
- **Results**: Output `seasonal_info.txt`, involving the results mentioned above.