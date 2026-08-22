# ASTRA SAT Flight Analyzer

**Version 1.0 - Complete Manual Input Edition**

ASTRA SAT is a fully manual-input CanSat mission analyzer built for learning, experimentation and recreational flight analysis.
Version 1.0 is the final "manual edition" before the sensor integrated version takes shape.

It includes vector wind drift, horizontal displacement tracking, terminal-velocity estimation, mission phase classification, expanded warnings, and CSV, Summary, and a 10 graph export.

## Demo And Download
- Demo page: https://aamirkpathan.github.io/AstraSAT/
- Direct download: https://github.com/AamirKPathan/AstraSAT/archive/refs/heads/main.zip

---

# Local Setup and Run

## Prerequisites

- Python 3.10 or newer
- A terminal or command prompt

ASTRA SAT uses Python's standard library plus on external library
- matplotlib

## Get The Project

Download the ZIP from the demo page, unzip it, and open a terminal inside the project folder.

Or you can clone with Git:
```bash
git clone https://github.com/AamirKPathan/AstraSAT.git
cd AstraSAT
```
## Create a Virtual Environment
Windows:
python -m venv .venv
.\.venv\Scripts\Activate.ps1

Mac/Linux
python3 -m venv .venv
source .venv/bin/activate

## Install Dependencies
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

## Run The Analyzer
1. python main.py
2. Follow the prompts
3. All files and exports will be saved under data/

## Troubleshooting
- If python isn't recognized on Windows, try py main.py
- If matplotlib is missing, reinstall with python-m pip install -r requirements.txt
- If graph windows don't open the imagesa r