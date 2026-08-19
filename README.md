# ASTRA SAT Flight Analyzer  
**Version 1.0 — Complete Manual Input Edition**

ASTRA SAT is a fully manual-input CanSat mission analyzer designed for recreational and educational use.  
Version 1.0 represents the complete and final “manual edition” before the sensor‑integrated version will begin.

This edition includes major capabilities such as vector wind drift, horizontal displacement tracking, terminal‑velocity estimation, mission‑phase classification, expanded warnings, full CSV export, full summary export, and a complete 10‑graph visualization suite.

No hardware, sensors, radios, GPS, or telemetry are used in this edition.

## Demo and Download

- Demo/download page: https://aamirkpathan.github.io/AstraSAT/
- Direct package download: https://github.com/AamirKPathan/AstraSAT/archive/refs/heads/main.zip

---

# Local Setup and Run

## Prerequisites

- Python 3.10 or newer
- pip, included with most Python installations
- A terminal or command prompt

The analyzer uses Python standard-library modules plus one third-party package:

- matplotlib

## Get the Project

Download the package from the demo page, unzip it, and open a terminal in the project folder.

If you prefer Git:

```bash
git clone https://github.com/AamirKPathan/AstraSAT.git
cd AstraSAT
```

## Create a Virtual Environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Install Dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Run Locally

```bash
python main.py
```

Follow the terminal prompts to enter mission setup values and flight readings.

Generated CSV files, mission summaries, and graphs are saved under:

```text
data/
```

## Troubleshooting

- If `python` is not found on Windows, try `py main.py`.
- If matplotlib is missing, rerun `python -m pip install -r requirements.txt` inside the activated virtual environment.
- If graph windows do not open, the graph image files are still saved in `data/graphs/`.

---

# What’s in Version 1.0

### ✔ Vector-based wind drift (north/east components)  
### ✔ Cumulative horizontal position tracking  
### ✔ Horizontal displacement and landing-direction estimate  
### ✔ Terminal-velocity estimation (body + parachute)  
### ✔ Mission-phase classification  
### ✔ Expanded safety warnings  
### ✔ Expanded data-integrity warnings  
### ✔ Full mission summary export  
### ✔ Complete CSV export (all physics + positions + phases)  
### ✔ 10-graph visualization set  
### ✔ Polished menus and program flow  
### ✔ Complete documentation and test campaign  

This is the final feature-complete manual-input version.

---

# Manual Edition Scope

### Included:
- All v0.1–v0.3 features  
- Vector wind drift  
- Horizontal displacement coordinates  
- Mission-phase classification  
- Terminal velocity  
- Improved warnings  
- Data consistency checks  
- Final landing-location estimate  
- Complete CSV export  
- Complete graph set  
- Polished menus and output  
- Documentation, tests, and release  

### Not Included (reserved for sensor edition):
- Physical sensors  
- Arduino / Raspberry Pi  
- GPS hardware  
- Radio telemetry  
- Live data streaming  
- GUI  
- Database or cloud storage  

---

# Mission Setup Inputs

- Mission name  
- CanSat mass (kg)  
- CanSat diameter (m)  
- Parachute diameter (m)  
- Starting altitude (m)  
- Safe landing speed (m/s)  
- Maximum safe wind speed (m/s)  
- Minimum safe temperature (°C)  
- Maximum safe temperature (°C)  
- Recommended minimum parachute altitude (m)  
- Starting battery (%)  
- CanSat drag coefficient  
- Parachute drag coefficient  

All values are validated.

---

# Flight Reading Inputs

Each reading includes:

- Mission time (s)  
- Altitude (m)  
- Vertical velocity (m/s)  
- Wind speed (m/s)  
- Wind direction (0–360°)  
- Temperature (°C)  
- Pressure (Pa)  
- Battery level (%)  
- Parachute deployed (yes/no)  
- Notes  

Mission time must increase each reading.

---

# Physics Calculations

### Core physics:
- Weight  
- Potential energy  
- Kinetic energy  
- Momentum  
- Air density  
- Drag force  
- Net vertical force  
- Force-based acceleration  
- Measured acceleration  
- Estimated landing time  

### Wind physics:
- North wind velocity  
- East wind velocity  
- North drift  
- East drift  
- Total wind drift  

### Horizontal position:
- Cumulative north position  
- Cumulative east position  
- Total horizontal displacement  

### Terminal velocity:
- CanSat body terminal velocity  
- Parachute terminal velocity  
- Safety check against landing-speed limit  

---

# Mission Phase Classification

Each reading is classified as:

- Pre-launch  
- Ascending  
- Apogee  
- Descending  
- Parachute descent  
- Stationary  
- Landed  
- Invalid data  

Displayed after every reading and exported to CSV.

---

# Warnings

Warnings are grouped into:

### Safety warnings:
- Unsafe descent speed  
- Unsafe wind  
- Unsafe temperature  
- Low battery  
- Parachute terminal velocity unsafe  
- Parachute not deployed below recommended altitude  

### Data warnings:
- Mission time not increasing  
- Battery increasing  
- Contradictory altitude/velocity  
- Parachute deployed during ascent  
- Extreme acceleration  
- Unrealistic velocity change  
- Pressure outside typical range  
- Temperature near unrealistic values  

### Mission status:
- Landing detected  
- Safe landing  
- Unsafe landing  

All warnings appear in the timesheet, summary, and CSV.

---

# Mission Timesheet

Each reading includes:

- Reading number  
- Mission time  
- Altitude  
- Vertical velocity  
- Wind speed + direction  
- Temperature  
- Pressure  
- Battery  
- Parachute status  
- Mission phase  
- North/East position  
- Horizontal displacement  
- Warnings  
- Notes  

---

# Final Mission Summary

Includes:

- Mission name  
- Total readings  
- Total mission time  
- Maximum altitude  
- Apogee time  
- Maximum ascent speed  
- Maximum descent speed  
- Maximum measured acceleration  
- Average wind speed  
- Maximum wind speed  
- Minimum battery  
- Battery consumed  
- Maximum drag force  
- Maximum net force  
- Estimated terminal velocity  
- Final north position  
- Final east position  
- Total horizontal displacement  
- Estimated landing direction  
- Total safety warnings  
- Total data warnings  
- Final mission result  

Also exported to:

```
data/<mission_name>_summary.txt
```

---

# CSV Export

CSV includes:

- All reading inputs  
- All physics values  
- All wind components  
- All drifts  
- All positions  
- Mission phase  
- Terminal velocity  
- Horizontal displacement  
- All warnings  
- Notes  

Saved as:

```
data/<mission_name>.csv
```

---

# Graph Set (10 Graphs)

Generated graphs:

1. Altitude vs time  
2. Vertical velocity vs time  
3. Measured acceleration vs time  
4. Battery vs time  
5. Temperature vs time  
6. Pressure vs time  
7. Air density vs time  
8. Drag force vs time  
9. Net vertical force vs time  
10. Horizontal flight path (east vs north)

Saved in:

```
data/graphs/
```

Graphs skip gracefully if insufficient data exists.

---

# Program Flow

1. Welcome screen  
2. Mission setup  
3. Setup confirmation  
4. Repeated flight readings  
5. Analysis after each reading  
6. Automatic landing detection or manual end  
7. Mission timesheet  
8. Final mission summary  
9. Export prompt  
10. Graph-generation prompt  
11. Completion message  

---

# Known Limitations

- Manual input only  
- No real sensors  
- No GPS  
- No radio telemetry  
- No GUI  
- No real-time tracking  
- No database or cloud storage  

These belong to the future **sensor-integrated edition**.

---

# Sensor Edition Roadmap (Next Project)

- Real sensor input  
- Arduino / Raspberry Pi integration  
- GPS tracking  
- Radio telemetry  
- Live graphing  
- Real-time landing prediction  
- Onboard data logging  
- GUI dashboard  

---

# License

Educational use permitted.  
Not intended for real aerospace navigation or safety-critical deployment.

