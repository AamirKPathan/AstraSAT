"""
ASTRA SAT Flight Analyzer
Version 0.2 — Extended Flight Physics

ASTRA SAT accepts manually entered CanSat mission data,
performs fundamental flight-physics calculations, identifies
unsafe conditions, stores repeated readings in a mission
timesheet, and produces a final mission summary.
"""

import math

GRAVITY = 9.81
SPECIFIC_GAS_CONSTANT_AIR = 287.05

# ---------------------------------------------------------
# INPUT FUNCTIONS
# ---------------------------------------------------------

def get_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid number. Please try again.")

def get_float_in_range(prompt, minimum=None, maximum=None):
    while True:
        value = get_float(prompt)
        if minimum is not None and value < minimum:
            print(f"Value must be at least {minimum}.")
            continue
        if maximum is not None and value > maximum:
            print(f"Value must not exceed {maximum}.")
            continue
        return value

def get_yes_no(prompt):
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("yes", "y"):
            return True
        if answer in ("no", "n"):
            return False
        print("Please enter yes or no.")

# ---------------------------------------------------------
# MISSION SETUP
# ---------------------------------------------------------

def calculate_circle_area(diameter):
    radius = diameter / 2
    return math.pi * radius**2

def collect_mission_setup():
    print("=== ASTRA SAT Mission Setup ===")

    mission_name = input("Mission name: ")

    mass = get_float_in_range("CanSat mass (kg): ", minimum=0.0001)
    cansat_diameter = get_float_in_range("CanSat diameter (m): ", minimum=0.0001)
    parachute_diameter = get_float_in_range("Parachute diameter (m): ", minimum=0.0001)
    starting_altitude = get_float_in_range("Starting altitude (m): ", minimum=0)
    safe_landing_speed = get_float_in_range("Safe landing speed (m/s): ", minimum=0.0001)
    max_safe_wind = get_float_in_range("Maximum safe wind speed (m/s): ", minimum=0)
    min_safe_temp = get_float("Minimum safe temperature (°C): ")
    max_safe_temp = get_float("Maximum safe temperature (°C): ")

    while max_safe_temp <= min_safe_temp:
        print("Maximum temperature must exceed minimum temperature.")
        max_safe_temp = get_float("Maximum safe temperature (°C): ")

    starting_battery = get_float_in_range("Starting battery (%): ", minimum=0, maximum=100)

    cansat_drag_coefficient = get_float_in_range(
        "CanSat drag coefficient (Cd): ", minimum=0.0
    )
    parachute_drag_coefficient = get_float_in_range(
        "Parachute drag coefficient (Cd): ", minimum=0.0
    )

    setup = {
        "mission_name": mission_name,
        "mass": mass,
        "cansat_diameter": cansat_diameter,
        "parachute_diameter": parachute_diameter,
        "starting_altitude": starting_altitude,
        "safe_landing_speed": safe_landing_speed,
        "max_safe_wind": max_safe_wind,
        "min_safe_temp": min_safe_temp,
        "max_safe_temp": max_safe_temp,
        "starting_battery": starting_battery,
        "cansat_drag_coefficient": cansat_drag_coefficient,
        "parachute_drag_coefficient": parachute_drag_coefficient,
    }

    setup["cansat_area"] = calculate_circle_area(setup["cansat_diameter"])
    setup["parachute_area"] = calculate_circle_area(setup["parachute_diameter"])

    print("\n=== Mission Setup Complete ===")
    for key, value in setup.items():
        if "area" in key:
            print(f"{key.replace('_', ' ').title()}: {value:.4f} m²")
        else:
            print(f"{key.replace('_', ' ').title()}: {value}")
    print()

    return setup

# ---------------------------------------------------------
# FLIGHT READING INPUT
# ---------------------------------------------------------

def collect_flight_reading(previous_time=None):
    print("\n=== Enter Flight Reading ===")

    while True:
        mission_time = get_float_in_range("Mission time (s): ", minimum=0)
        if previous_time is None or mission_time > previous_time:
            break
        print(f"Mission time must be greater than {previous_time:.1f} seconds.")

    altitude = get_float_in_range("Altitude (m): ", minimum=0)
    vertical_velocity = get_float("Vertical velocity (m/s): ")
    wind_speed = get_float_in_range("Wind speed (m/s): ", minimum=0)
    wind_direction = get_float_in_range("Wind direction (0–360°): ", minimum=0, maximum=360)
    temperature = get_float("Temperature (°C): ")

    while temperature <= -273.15:
        print("Temperature cannot be at or below absolute zero (-273.15°C).")
        temperature = get_float("Temperature (°C): ")

    pressure = get_float_in_range("Air pressure (Pa): ", minimum=0.0001)
    battery_level = get_float_in_range("Battery level (%): ", minimum=0, maximum=100)
    parachute_deployed = get_yes_no("Parachute deployed (yes/no): ")
    notes = input("Notes: ")

    return {
        "mission_time": mission_time,
        "altitude": altitude,
        "vertical_velocity": vertical_velocity,
        "wind_speed": wind_speed,
        "wind_direction": wind_direction,
        "temperature": temperature,
        "pressure": pressure,
        "battery_level": battery_level,
        "parachute_deployed": parachute_deployed,
        "notes": notes,
    }

# ---------------------------------------------------------
# PHYSICS CALCULATIONS
# ---------------------------------------------------------

def calculate_weight(mass):
    return mass * GRAVITY

def calculate_potential_energy(mass, altitude):
    return mass * GRAVITY * altitude

def calculate_kinetic_energy(mass, velocity):
    return 0.5 * mass * velocity**2

def calculate_momentum(mass, velocity):
    return mass * velocity

def estimate_landing_time(altitude, vertical_velocity):
    if altitude <= 0:
        return 0.0
    if vertical_velocity >= 0:
        return None
    return altitude / abs(vertical_velocity)

def estimate_wind_drift(wind_speed, landing_time):
    if landing_time is None:
        return None
    return wind_speed * landing_time

def calculate_acceleration(previous_reading, current_reading):
    if previous_reading is None:
        return None

    change_in_velocity = (
        current_reading["vertical_velocity"]
        - previous_reading["vertical_velocity"]
    )
    change_in_time = (
        current_reading["mission_time"]
        - previous_reading["mission_time"]
    )

    if change_in_time <= 0:
        return None

    return change_in_velocity / change_in_time

def calculate_air_density(pressure, temperature_celsius):
    temperature_kelvin = temperature_celsius + 273.15
    if temperature_kelvin <= 0:
        return None
    return pressure / (SPECIFIC_GAS_CONSTANT_AIR * temperature_kelvin)

def calculate_drag_force(air_density, velocity, drag_coefficient, area):
    if air_density is None:
        return 0.0
    return 0.5 * air_density * velocity**2 * drag_coefficient * area

def calculate_net_vertical_force(weight, drag_force, vertical_velocity):
    if vertical_velocity < 0:
        return weight - drag_force
    elif vertical_velocity > 0:
        return weight + drag_force
    return weight

def calculate_force_based_acceleration(net_force, mass):
    return net_force / mass

def calculate_physics(setup, reading, previous_reading):
    mass = setup["mass"]
    altitude = reading["altitude"]
    velocity = reading["vertical_velocity"]
    wind_speed = reading["wind_speed"]

    weight = calculate_weight(mass)
    potential_energy = calculate_potential_energy(mass, altitude)
    kinetic_energy = calculate_kinetic_energy(mass, velocity)
    momentum = calculate_momentum(mass, velocity)
    landing_time = estimate_landing_time(altitude, velocity)
    wind_drift = estimate_wind_drift(wind_speed, landing_time)

    measured_acceleration = calculate_acceleration(previous_reading, reading)
    air_density = calculate_air_density(reading["pressure"], reading["temperature"])

    if reading["parachute_deployed"]:
        active_area = setup["parachute_area"]
        drag_coefficient = setup["parachute_drag_coefficient"]
    else:
        active_area = setup["cansat_area"]
        drag_coefficient = setup["cansat_drag_coefficient"]

    drag_force = calculate_drag_force(
        air_density,
        velocity,
        drag_coefficient,
        active_area,
    )

    net_force = calculate_net_vertical_force(weight, drag_force, velocity)
    force_acceleration = calculate_force_based_acceleration(net_force, mass)

    return {
        "weight": weight,
        "potential_energy": potential_energy,
        "kinetic_energy": kinetic_energy,
        "momentum": momentum,
        "landing_time": landing_time,
        "wind_drift": wind_drift,
        "measured_acceleration": measured_acceleration,
        "air_density": air_density,
        "active_area": active_area,
        "active_drag_coefficient": drag_coefficient,
        "drag_force": drag_force,
        "net_force": net_force,
        "force_acceleration": force_acceleration,
    }

# ---------------------------------------------------------
# WARNINGS
# ---------------------------------------------------------

def generate_warnings(setup, reading):
    warnings = []

    battery = reading["battery_level"]
    velocity = reading["vertical_velocity"]
    altitude = reading["altitude"]

    if battery < 10:
        warnings.append("CRITICAL: Battery below 10%")
    elif battery < 20:
        warnings.append("WARNING: Battery below 20%")

    if reading["wind_speed"] > setup["max_safe_wind"]:
        warnings.append("WARNING: Wind exceeds safe limit")

    if not (setup["min_safe_temp"] <= reading["temperature"] <= setup["max_safe_temp"]):
        warnings.append("WARNING: Temperature outside safe range")

    if velocity < 0 and abs(velocity) > setup["safe_landing_speed"]:
        warnings.append("WARNING: Unsafe descent speed")

    if altitude <= 0:
        warnings.append("LANDING DETECTED")

        if velocity > 0:
            warnings.append("INVALID DATA: Positive velocity at landing")
        elif abs(velocity) <= setup["safe_landing_speed"]:
            warnings.append("SAFE LANDING")
        else:
            warnings.append("UNSAFE LANDING")

    return warnings

# ---------------------------------------------------------
# DISPLAY FUNCTIONS
# ---------------------------------------------------------

def display_analysis(physics, warnings):
    print("\n=== Flight Analysis ===")
    print(f"Weight: {physics['weight']:.2f} N")
    print(f"Potential Energy: {physics['potential_energy']:.2f} J")
    print(f"Kinetic Energy: {physics['kinetic_energy']:.2f} J")
    print(f"Momentum: {physics['momentum']:.2f} kg·m/s")

    if physics["landing_time"] is None:
        print("Estimated Landing Time: N/A (ascending)")
        print("Estimated Wind Drift: N/A")
    else:
        print(f"Estimated Landing Time: {physics['landing_time']:.2f} s")
        print(f"Estimated Wind Drift: {physics['wind_drift']:.2f} m")

    if physics["measured_acceleration"] is None:
        print("Measured Acceleration: N/A")
    else:
        print(
            f"Measured Acceleration: "
            f"{physics['measured_acceleration']:.2f} m/s²"
        )

    if physics["air_density"] is None:
        print("Air Density: N/A")
    else:
        print(
            f"Air Density: "
            f"{physics['air_density']:.3f} kg/m³"
        )

    print(
        f"Active Area: "
        f"{physics['active_area']:.4f} m²"
    )
    print(
        f"Active Drag Coefficient: "
        f"{physics['active_drag_coefficient']:.2f}"
    )
    print(
        f"Drag Force: "
        f"{physics['drag_force']:.2f} N"
    )
    print(
        f"Net Vertical Force: "
        f"{physics['net_force']:.2f} N"
    )
    print(
        f"Force-Based Acceleration: "
        f"{physics['force_acceleration']:.2f} m/s²"
    )

    print("\nWarnings:")
    if warnings:
        for w in warnings:
            print(f"- {w}")
    else:
        print("None")

def display_timesheet(timesheet):
    print("\n=== ASTRA SAT Mission Timesheet ===")

    for entry in timesheet:
        reading = entry["reading"]
        status = "; ".join(entry["warnings"]) if entry["warnings"] else "NORMAL"
        parachute = "Deployed" if reading["parachute_deployed"] else "Not deployed"

        print(f"\n--- Reading {entry['reading_number']} ---")
        print(f"Mission Time: {reading['mission_time']:.1f} s")
        print(f"Altitude: {reading['altitude']:.1f} m")
        print(f"Vertical Velocity: {reading['vertical_velocity']:.1f} m/s")
        print(f"Wind Speed: {reading['wind_speed']:.1f} m/s")
        print(f"Wind Direction: {reading['wind_direction']:.1f}°")
        print(f"Temperature: {reading['temperature']:.1f} °C")
        print(f"Pressure: {reading['pressure']:.1f} Pa")
        print(f"Battery: {reading['battery_level']:.1f}%")
        print(f"Parachute: {parachute}")
        print(f"Status: {status}")

def display_mission_summary(setup, timesheet):
    readings = [entry["reading"] for entry in timesheet]
    final_reading = readings[-1]

    maximum_altitude = max(r["altitude"] for r in readings)
    minimum_battery = min(r["battery_level"] for r in readings)
    maximum_wind = max(r["wind_speed"] for r in readings)

    descent_speeds = [
        abs(r["vertical_velocity"])
        for r in readings
        if r["vertical_velocity"] < 0
    ]
    maximum_descent_speed = max(descent_speeds) if descent_speeds else 0

    warning_count = sum(
        1
        for entry in timesheet
        for message in entry["warnings"]
        if message.startswith(("WARNING", "CRITICAL", "INVALID"))
    )

    battery_used = setup["starting_battery"] - final_reading["battery_level"]

    final_statuses = timesheet[-1]["warnings"]

    if "SAFE LANDING" in final_statuses:
        landing_result = "Safe landing"
    elif "UNSAFE LANDING" in final_statuses:
        landing_result = "Unsafe landing"
    elif any(msg.startswith("INVALID DATA") for msg in final_statuses):
        landing_result = "Invalid landing data"
    else:
        landing_result = "Mission ended before landing"

    print("\n=== ASTRA SAT Mission Summary ===")
    print(f"Mission Name: {setup['mission_name']}")
    print(f"Readings Recorded: {len(timesheet)}")
    print(f"Final Mission Time: {final_reading['mission_time']:.1f} s")
    print(f"Configured Starting Altitude: {setup['starting_altitude']:.1f} m")
    print(f"Maximum Recorded Altitude: {maximum_altitude:.1f} m")
    print(f"Final Altitude: {final_reading['altitude']:.1f} m")
    print(f"Starting Battery: {setup['starting_battery']:.1f}%")
    print(f"Final Battery: {final_reading['battery_level']:.1f}%")
    print(f"Battery Used: {battery_used:.1f}%")
    print(f"Minimum Battery: {minimum_battery:.1f}%")
    print(f"Maximum Wind Speed: {maximum_wind:.1f} m/s")
    print(f"Maximum Descent Speed: {maximum_descent_speed:.1f} m/s")
    print(f"Warnings Issued: {warning_count}")
    print(f"Mission Result: {landing_result}")

# ---------------------------------------------------------
# MAIN PROGRAM LOOP
# ---------------------------------------------------------

def main():
    setup = collect_mission_setup()
    mission_timesheet = []

    while True:
        previous_time = mission_timesheet[-1]["reading"]["mission_time"] if mission_timesheet else None
        previous_reading = mission_timesheet[-1]["reading"] if mission_timesheet else None

        reading = collect_flight_reading(previous_time)

        physics = calculate_physics(setup, reading, previous_reading)
        warnings = generate_warnings(setup, reading)

        entry = {
            "reading_number": len(mission_timesheet) + 1,
            "reading": reading,
            "physics": physics,
            "warnings": warnings,
        }

        mission_timesheet.append(entry)

        display_analysis(physics, warnings)

        if reading["altitude"] <= 0:
            break

        if not get_yes_no("Enter another flight reading? (yes/no): "):
            break

    display_timesheet(mission_timesheet)
    display_mission_summary(setup, mission_timesheet)

if __name__ == "__main__":
    main()
