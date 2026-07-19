# ASTRA SAT Flight Analyzer

**Version 0.1 — Manual CanSat Mission Logger**

Astra SAT is a Python-based CanSat mission‑logging and flight‑analysis program designed for manual data entry, physics calculations, safety evaluation, and mission reporting. It provides a structured workflow for entering repeated flight readings, validating mission data, analyzing descent behavior, detecting unsafe conditions, and generating a complete mission summary.

This release finalizes all Version 0.1 requirements, including validation, warnings, landing classification, chronological time enforcement, improved timesheet formatting, and a complete test suite.

---

# Project Purpose

ASTRA SAT helps students, hobbyists, and CanSat teams analyze manually collected flight data.  
It is built for:

- learning basic flight physics  
- practicing mission logging  
- validating sensor readings  
- understanding descent behavior  
- identifying unsafe conditions  
- producing readable mission summaries  

It is intentionally simple, focusing on clarity and correctness rather than advanced physics.

---

# Features (Version 0.1 FINAL)

### ✔ Validated mission setup  
All mission parameters are checked for correctness before the mission begins.

### ✔ Validated flight readings  
Every reading is checked for numerical correctness and physical plausibility.

### ✔ Chronological mission‑time enforcement  
Mission time must always increase — no repeats, no backwards time.

### ✔ Physics calculations  
Weight, potential energy, kinetic energy, momentum, landing time, and wind drift.

### ✔ Safety warnings  
Battery, wind, temperature, descent speed, landing classification, invalid landing velocity.

### ✔ Landing classification  
Safe, unsafe, invalid, or mission ended before landing.

### ✔ Improved mission timesheet  
Readable, structured, and includes all relevant fields.

### ✔ Improved mission summary  
Includes mission name, starting values, final values, battery usage, descent behavior, and landing result.

### ✔ Warning filtering  
Only true hazards count as warnings.

### ✔ Complete test suite  
Normal descent, positive velocity, hazards, safe landing, unsafe landing, invalid landing, and all edge cases.

---

# Mission Setup Inputs

The following values are collected at the start of the mission:

| Input | Requirement |
|-------|-------------|
| Mission name | Any text |
| Mass (kg) | > 0 |
| CanSat diameter (m) | > 0 |
| Parachute diameter (m) | > 0 |
| Starting altitude (m) | ≥ 0 |
| Safe landing speed (m/s) | > 0 |
| Maximum safe wind speed (m/s) | ≥ 0 |
| Minimum safe temperature (°C) | Any number |
| Maximum safe temperature (°C) | Must exceed minimum |
| Starting battery (%) | 0–100 |

All values are validated. Invalid entries are rejected until corrected.

---

# Flight Reading Inputs

Each reading includes:

- mission time (s) — must increase each reading  
- altitude (m) — must be ≥ 0  
- vertical velocity (m/s) — positive = ascending, negative = descending  
- wind speed (m/s) — must be ≥ 0  
- wind direction (°) — must be 0–360  
- temperature (°C)  
- air pressure (Pa) — must be > 0  
- battery level (%) — must be 0–100  
- parachute deployed (yes/no)  
- notes  

Invalid entries are rejected immediately.

---

# Physics Calculations

Gravity constant: **9.81 m/s²**

ASTRA SAT calculates:

### Weight
F = m × g

### Gravitational Potential Energy
Eg = m × g × h

### Kinetic Energy
Ek = ½ m v²

### Momentum
p = m × v

### Estimated Landing Time
Only calculated when descending:
t = h / |v|

### Wind Drift
d = v_wind × t

If ascending, landing time and drift are unavailable.

---

# Warning Conditions

ASTRA SAT identifies:

### Battery
- CRITICAL: below 10%  
- WARNING: below 20%

### Wind
- WARNING: wind exceeds safe limit

### Temperature
- WARNING: outside safe range

### Descent Speed
- WARNING: unsafe descent speed (descending faster than safe limit)

### Landing Classification
- LANDING DETECTED  
- SAFE LANDING  
- UNSAFE LANDING  
- INVALID DATA: positive velocity at landing  

### Warning Counting
Only messages starting with:

- WARNING  
- CRITICAL  
- INVALID  

are counted as warnings.

Landing statuses are **not** counted as warnings.

---

# Mission Timesheet Display

Each reading is shown in a readable block:

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
- warnings and statuses  

This replaces raw dictionary output.

---

# Final Mission Summary

The summary includes:

- mission name  
- readings recorded  
- final mission time  
- configured starting altitude  
- maximum recorded altitude  
- final altitude  
- starting battery  
- final battery  
- battery used  
- minimum battery  
- maximum wind speed  
- maximum descent speed  
- warnings issued  
- landing result  

Landing result may be:

- Safe landing  
- Unsafe landing  
- Invalid landing data  
- Mission ended before landing  

---

# Input Sign Convention

- **Positive velocity** → upward motion  
- **Negative velocity** → downward motion  

---

# How to Run

1. Install Python 3  
2. Open the project folder  
3. Run:

python main.py


4. Enter mission setup  
5. Enter flight readings in chronological order  
6. Continue until landing or manually end the mission  

---

# Example Mission


Mission Time: 40 s
Altitude: 850 m
Velocity: -7 m/s
Wind: 5 m/s
Direction: 100°
Temperature: 8°C
Pressure: 92000 Pa
Battery: 91%
Parachute: yes
Notes: stable descent


Expected:

- landing time calculated  
- wind drift calculated  
- no warnings  

---

# Current Limitations

- All data is entered manually  
- Landing time assumes constant vertical velocity  
- Wind drift assumes constant wind speed  
- Wind direction is recorded but not used for vector drift  
- Drag and air density are not included  
- No real sensor integration  
- No CSV export  
- No graphs  
- No GUI  

---

# Future Development (Version 0.2+)

Planned improvements:

- acceleration between readings  
- air-density estimation  
- parachute area and drag force  
- vector-based wind displacement  
- CSV export  
- flight-data graphs  
- real sensor integration  
- mission replay visualization  

---

# Repository

Recommended GitHub repository name:

astra-sat-flight-analyzer