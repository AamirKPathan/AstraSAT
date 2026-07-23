# ASTRA SAT Flight Analyzer

**Version 0.3 — Data Export and Visualization**

ASTRA SAT is a Python-based CanSat mission-logging and flight-analysis program.  
It accepts manually entered mission and flight data, validates inputs, calculates physics values, identifies unsafe conditions, and produces a readable mission timesheet and final mission summary.

Version 0.3 adds **mission data export** and **graph generation**, allowing users to save results and visualize flight behavior.

---

# What’s New in Version 0.3

Version 0.3 introduces:

### ✔ CSV export of mission readings  
### ✔ Export of mission setup metadata  
### ✔ Altitude vs time graph  
### ✔ Vertical velocity vs time graph  
### ✔ Battery level vs time graph  
### ✔ Measured acceleration vs time graph  
### ✔ Graph folder (`data/graphs/`)  
### ✔ Export confirmation prompts  
### ✔ Graph generation confirmation prompts  

These features make ASTRA SAT more useful for analysis, reporting, and science fair or competition documentation.

---

# Mission Setup Inputs

- mission name  
- CanSat mass (kg)  
- CanSat diameter (m)  
- parachute diameter (m)  
- starting altitude (m)  
- safe landing speed (m/s)  
- maximum safe wind speed (m/s)  
- minimum safe temperature (°C)  
- maximum safe temperature (°C)  
- starting battery (%)  
- CanSat drag coefficient  
- parachute drag coefficient  

All values are validated.

---

# Flight Reading Inputs

- mission time (s) — must increase each reading  
- altitude (m)  
- vertical velocity (m/s)  
- wind speed (m/s)  
- wind direction (0–360°)  
- temperature (°C) — cannot be ≤ −273.15°C  
- air pressure (Pa)  
- battery level (%)  
- parachute deployed (yes/no)  
- notes  

---

# Physics Calculations (from Version 0.2)

- measured acceleration between readings  
- air density from pressure and temperature  
- CanSat and parachute cross-sectional areas  
- drag force using active configuration  
- net vertical force  
- force-based acceleration  
- potential energy  
- kinetic energy  
- momentum  
- estimated landing time  
- estimated wind drift  

---

# CSV Export (Version 0.3)

After the mission ends, the user may choose:

Export mission data? (yes/no):

If yes:

### A CSV file is created in:

