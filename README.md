# ASTRA SAT Flight Analyzer

**Version 0.2 — Extended Flight Physics**

ASTRA SAT is a Python-based CanSat mission-logging and flight-analysis program. It accepts manually entered mission and flight data, validates inputs, calculates fundamental and extended physics quantities, identifies unsafe conditions, and produces a readable mission timesheet and final mission summary.

---

## Version 0.2 Features

- Validated mission setup  
- Repeated manual flight readings  
- Chronological mission-time validation  
- Basic physics calculations (weight, potential energy, kinetic energy, momentum)  
- Estimated landing time and wind drift  
- Safety warnings and landing classification  
- Mission timesheet and final mission summary  
- **New in 0.2:**  
  - Measured acceleration between readings  
  - Air-density estimation from pressure and temperature  
  - CanSat cross-sectional area  
  - Parachute area  
  - Drag-force estimation (CanSat vs parachute)  
  - Net vertical-force estimation  
  - Force-based acceleration from net force and mass  

---

## Physics Calculations

Gravity constant: **9.81 m/s²**

- Weight: F = m × g  
- Gravitational potential energy: Eg = m × g × h  
- Kinetic energy: Ek = ½ m v²  
- Momentum: p = m × v  
- Estimated landing time: t = h / |v| (only when descending)  
- Estimated wind drift: d = v_wind × t  
- Measured acceleration: Δv / Δt between consecutive readings  
- Air density: ρ = P / (R × T) using pressure and temperature  
- Drag force: Fd = ½ ρ v² Cd A  
- Net vertical force (simplified):  
  - Descent: F_net = weight − drag  
  - Ascent: F_net = weight + drag  
- Force-based acceleration: a = F_net / m  

---

## Mission Setup Inputs

- mission name  
- CanSat mass (kg) — must be > 0  
- CanSat diameter (m) — must be > 0  
- parachute diameter (m) — must be > 0  
- starting altitude (m) — must be ≥ 0  
- safe landing-speed limit (m/s) — must be > 0  
- maximum safe wind speed (m/s) — must be ≥ 0  
- minimum safe temperature (°C)  
- maximum safe temperature (°C) — must exceed minimum  
- starting battery percentage (%) — must be 0–100  
- CanSat drag coefficient (Cd) — must be ≥ 0  
- parachute drag coefficient (Cd) — must be ≥ 0  

All values are validated.

---

## Flight Reading Inputs

- mission time (s) — must be ≥ 0 and must increase each reading  
- altitude (m) — must be ≥ 0  
- vertical velocity (m/s) — positive = upward, negative = downward  
- wind speed (m/s) — must be ≥ 0  
- wind direction (degrees 0–360)  
- temperature (°C) — cannot be ≤ −273.15°C  
- air pressure (Pa) — must be > 0  
- battery level (%) — must be 0–100  
- parachute deployed (yes/no)  
- notes  

---

## Warning Conditions

- CRITICAL: battery below 10%  
- WARNING: battery below 20%  
- WARNING: wind exceeds safe limit  
- WARNING: temperature outside safe range  
- WARNING: unsafe descent speed  
- LANDING DETECTED  
- SAFE LANDING  
- UNSAFE LANDING  
- INVALID DATA: positive velocity at landing  

Warning counting only includes messages starting with:

- WARNING  
- CRITICAL  
- INVALID  

Landing messages are not counted as warnings.

---

## Mission Timesheet Display

Each reading shows:

- reading number  
- mission time  
- altitude  
- vertical velocity  
- wind speed  
- wind direction  
- temperature  
- pressure  
- battery  
- parachute status  
- warning/status text  

---

## Final Mission Summary

Includes:

- mission name  
- starting altitude  
- starting battery  
- total readings  
- final mission time  
- maximum altitude  
- minimum battery  
- maximum wind speed  
- maximum descent speed  
- final altitude  
- final battery  
- battery used  
- warnings issued  
- landing result  

---

## Input Sign Convention

- Positive velocity = upward  
- Negative velocity = downward  

Net force sign (simplified):

- Positive net force = downward  
- Negative net force = upward  

---

## How to Run

1. Install Python 3.  
2. Open the project folder in a terminal.  
3. Run:

```bash
python main.py
