"""
ASTRA SAT Flight Analyzer
Version 1.0 — Complete Manual Input Edition

Includes:
- All v0.1–v0.3 features (manual mission setup, physics, CSV export, graphs)
- Vector-based wind drift (north/east components)
- Cumulative horizontal position tracking
- Terminal-velocity estimation (body + parachute)
- Mission-phase classification
- Data-integrity and safety warnings
- Final landing-location estimate
- Complete CSV export and summary export
- Extended graph set
- Polished menus and output flow
"""

import math
import csv
import os
import matplotlib.pyplot as plt

GRAVITY = 9.81
SPECIFIC_GAS_CONSTANT_AIR = 287.05
ABSOLUTE_ZERO_C = -273.15

# ---------------------------------------------------------
# INPUT FUNCTIONS
# ---------------------------------------------------------

def get_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("INPUT ERROR: Please enter a valid number.")


def get_float_in_range(prompt, minimum=None, maximum=None):
    while True:
        value = get_float(prompt)
        if minimum is not None and value < minimum:
            print(f"INPUT ERROR: Value must be at least {minimum}.")
            continue
        if maximum is not None and value > maximum:
            print(f"INPUT ERROR: Value must not exceed {maximum}.")
            continue
        return value


def get_yes_no(prompt):
    while True:
        ans = input(prompt).strip().lower()
        if ans in ("yes", "y"):
            return True
        if ans in ("no", "n"):
            return False
        print("INPUT ERROR: Please enter yes or no.")


# ---------------------------------------------------------
# WIND VECTOR FUNCTIONS
# ---------------------------------------------------------

def calculate_wind_components(wind_speed, wind_direction_degrees):
    """
    0° = North
    90° = East
    180° = South
    270° = West
    """
    direction_radians = math.radians(wind_direction_degrees)

    north_velocity = wind_speed * math.cos(direction_radians)
    east_velocity = wind_speed * math.sin(direction_radians)

    return north_velocity, east_velocity


# ---------------------------------------------------------
# TERMINAL VELOCITY
# ---------------------------------------------------------

def calculate_terminal_velocity(mass, gravity, air_density, drag_coefficient, area):
    denominator = air_density * drag_coefficient * area
    if denominator <= 0:
        return None
    return math.sqrt((2 * mass * gravity) / denominator)


# ---------------------------------------------------------
# MISSION SETUP
# ---------------------------------------------------------

def calculate_circle_area(diameter):
    radius = diameter / 2
    return math.pi * radius**2


def show_welcome_banner():
    print("========================================")
    print("       ASTRA SAT FLIGHT ANALYZER")
    print("       Manual Input Edition v1.0")
    print("========================================\n")


def collect_mission_setup():
    show_welcome_banner()
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
        print("INPUT ERROR: Maximum temperature must exceed minimum.")
        max_safe_temp = get_float("Maximum safe temperature (°C): ")

    starting_battery = get_float_in_range("Starting battery (%): ", minimum=0, maximum=100)

    cansat_drag_coefficient = get_float_in_range(
        "CanSat drag coefficient: ", minimum=0.0001
    )
    parachute_drag_coefficient = get_float_in_range(
        "Parachute drag coefficient: ", minimum=0.0001
    )

    parachute_min_altitude = get_float_in_range(
        "Recommended minimum altitude for parachute deployment (m): ", minimum=0
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
        "parachute_min_altitude": parachute_min_altitude,
    }

    setup["cansat_area"] = calculate_circle_area(cansat_diameter)
    setup["parachute_area"] = calculate_circle_area(parachute_diameter)

    print("\n=== Mission Setup Complete ===")
    print(f"Mission Name: {mission_name}")
    print(f"CanSat Area: {setup['cansat_area']:.4f} m²")
    print(f"Parachute Area: {setup['parachute_area']:.4f} m²")
    print(f"CanSat Drag Coefficient: {cansat_drag_coefficient}")
    print(f"Parachute Drag Coefficient: {parachute_drag_coefficient}")
    print(f"Safe Landing Speed: {safe_landing_speed:.2f} m/s")
    print(f"Max Safe Wind: {max_safe_wind:.2f} m/s")
    print(f"Safe Temperature Range: {min_safe_temp:.1f} to {max_safe_temp:.1f} °C")
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
        print("DATA WARNING: Mission time must be greater than previous reading.")

    altitude = get_float_in_range("Altitude (m): ", minimum=0)
    vertical_velocity = get_float("Vertical velocity (m/s): ")
    wind_speed = get_float_in_range("Wind speed (m/s): ", minimum=0)
    wind_direction = get_float_in_range("Wind direction (0–360°): ", minimum=0, maximum=360)

    temperature = get_float_in_range(
        "Temperature (°C): ",
        minimum=ABSOLUTE_ZERO_C + 0.01
    )

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
# PHYSICS (BASE + v0.2 + v1.0)
# ---------------------------------------------------------

def calculate_measured_acceleration(previous_reading, current_reading):
    if previous_reading is None:
        return None

    dv = current_reading["vertical_velocity"] - previous_reading["vertical_velocity"]
    dt = current_reading["mission_time"] - previous_reading["mission_time"]

    if dt <= 0:
        return None

    return dv / dt


def calculate_air_density(pressure, temp_c):
    temp_k = temp_c + 273.15
    if temp_k <= 0:
        return None
    return pressure / (SPECIFIC_GAS_CONSTANT_AIR * temp_k)


def calculate_drag_force(air_density, velocity, drag_coefficient, area):
    if air_density is None:
        return 0.0
    return 0.5 * air_density * velocity**2 * drag_coefficient * area


def calculate_net_vertical_force(weight, drag_force, velocity):
    if velocity < 0:
        return weight - drag_force
    if velocity > 0:
        return weight + drag_force
    return weight


def calculate_force_based_acceleration(net_force, mass):
    return net_force / mass


def classify_mission_phase(reading, previous_reading=None):
    altitude = reading["altitude"]
    velocity = reading["vertical_velocity"]
    parachute = reading["parachute_deployed"]

    if altitude <= 0:
        return "Landed"

    if previous_reading is None and altitude == 0 and velocity == 0:
        return "Pre-launch"

    if velocity > 0:
        if parachute:
            return "Invalid data"
        return "Ascending"

    if velocity < 0 and parachute:
        return "Parachute descent"

    if velocity < 0:
        return "Descending"

    if previous_reading is not None:
        previous_velocity = previous_reading["vertical_velocity"]
        if previous_velocity > 0 and velocity == 0:
            return "Apogee"

    return "Stationary"


def calculate_physics(setup, reading, previous_reading, previous_physics):
    mass = setup["mass"]
    altitude = reading["altitude"]
    velocity = reading["vertical_velocity"]
    wind_speed = reading["wind_speed"]
    wind_direction = reading["wind_direction"]

    weight = mass * GRAVITY
    potential_energy = mass * GRAVITY * altitude
    kinetic_energy = 0.5 * mass * velocity**2
    momentum = mass * velocity

    landing_time = altitude / abs(velocity) if altitude > 0 and velocity < 0 else None

    north_velocity, east_velocity = calculate_wind_components(wind_speed, wind_direction)

    if landing_time is not None:
        north_drift = north_velocity * landing_time
        east_drift = east_velocity * landing_time
        total_wind_drift = math.sqrt(north_drift**2 + east_drift**2)
    else:
        north_drift = None
        east_drift = None
        total_wind_drift = None

    measured_acceleration = calculate_measured_acceleration(previous_reading, reading)
    air_density = calculate_air_density(reading["pressure"], reading["temperature"])

    if reading["parachute_deployed"]:
        active_area = setup["parachute_area"]
        active_drag_coefficient = setup["parachute_drag_coefficient"]
        active_configuration = "Parachute"
    else:
        active_area = setup["cansat_area"]
        active_drag_coefficient = setup["cansat_drag_coefficient"]
        active_configuration = "CanSat body"

    drag_force = calculate_drag_force(
        air_density,
        velocity,
        active_drag_coefficient,
        active_area
    )

    net_vertical_force = calculate_net_vertical_force(weight, drag_force, velocity)
    force_based_acceleration = calculate_force_based_acceleration(net_vertical_force, mass)

    # Terminal velocity estimate (for active configuration)
    terminal_velocity = calculate_terminal_velocity(
        mass,
        GRAVITY,
        air_density if air_density is not None else 1.2,
        active_drag_coefficient,
        active_area
    )

    # Cumulative horizontal position
    if previous_physics is None:
        north_position = 0.0
        east_position = 0.0
    else:
        dt = reading["mission_time"] - previous_reading["mission_time"]
        if dt < 0:
            dt = 0
        north_position = previous_physics["north_position"] + north_velocity * dt
        east_position = previous_physics["east_position"] + east_velocity * dt

    horizontal_displacement = math.sqrt(north_position**2 + east_position**2)

    physics = {
        "weight": weight,
        "potential_energy": potential_energy,
        "kinetic_energy": kinetic_energy,
        "momentum": momentum,
        "landing_time": landing_time,
        "north_velocity": north_velocity,
        "east_velocity": east_velocity,
        "north_drift": north_drift,
        "east_drift": east_drift,
        "total_wind_drift": total_wind_drift,
        "measured_acceleration": measured_acceleration,
        "air_density": air_density,
        "active_configuration": active_configuration,
        "active_area": active_area,
        "active_drag_coefficient": active_drag_coefficient,
        "drag_force": drag_force,
        "net_vertical_force": net_vertical_force,
        "force_based_acceleration": force_based_acceleration,
        "estimated_terminal_velocity": terminal_velocity,
        "north_position": north_position,
        "east_position": east_position,
        "horizontal_displacement": horizontal_displacement,
    }

    return physics


# ---------------------------------------------------------
# WARNINGS (SAFETY + DATA + STATUS)
# ---------------------------------------------------------

def generate_warnings(setup, reading, previous_reading, physics, previous_physics):
    warnings = []

    battery = reading["battery_level"]
    velocity = reading["vertical_velocity"]
    altitude = reading["altitude"]
    wind_speed = reading["wind_speed"]
    temperature = reading["temperature"]
    pressure = reading["pressure"]
    parachute = reading["parachute_deployed"]

    # SAFETY WARNINGS
    if battery < 10:
        warnings.append("SAFETY WARNING: Battery below 10%")
    elif battery < 20:
        warnings.append("SAFETY WARNING: Battery below 20%")

    if wind_speed > setup["max_safe_wind"]:
        warnings.append("SAFETY WARNING: Wind exceeds safe limit")

    if not (setup["min_safe_temp"] <= temperature <= setup["max_safe_temp"]):
        warnings.append("SAFETY WARNING: Temperature outside safe range")

    if velocity < 0 and abs(velocity) > setup["safe_landing_speed"]:
        warnings.append("SAFETY WARNING: Unsafe descent speed")

    if physics["estimated_terminal_velocity"] is not None:
        if physics["estimated_terminal_velocity"] > setup["safe_landing_speed"] and parachute:
            warnings.append(
                "SAFETY WARNING: Estimated parachute terminal velocity exceeds safe landing speed"
            )

    # MISSION STATUS
    if altitude <= 0:
        warnings.append("MISSION STATUS: LANDING DETECTED")

        if velocity > 0:
            warnings.append("DATA WARNING: Positive velocity at landing")
        elif abs(velocity) <= setup["safe_landing_speed"]:
            warnings.append("MISSION STATUS: SAFE LANDING")
        else:
            warnings.append("MISSION STATUS: UNSAFE LANDING")

    # DATA-INTEGRITY WARNINGS
    if previous_reading is not None:
        if reading["mission_time"] <= previous_reading["mission_time"]:
            warnings.append("DATA WARNING: Mission time did not increase")

        if battery > previous_reading["battery_level"]:
            warnings.append("DATA WARNING: Battery increased from previous reading")

        # Contradictory altitude/velocity
        if altitude > previous_reading["altitude"] and velocity < -0.5:
            warnings.append(
                "DATA WARNING: Altitude rising while velocity strongly negative"
            )
        if altitude < previous_reading["altitude"] and velocity > 0.5:
            warnings.append(
                "DATA WARNING: Altitude falling while velocity strongly positive"
            )

        # Parachute during ascent
        if velocity > 0 and parachute:
            warnings.append("DATA WARNING: Parachute deployed during ascent")

        # Parachute not deployed below recommended altitude
        if altitude < setup["parachute_min_altitude"] and not parachute and velocity < 0:
            warnings.append(
                "SAFETY WARNING: Parachute not deployed below recommended altitude"
            )

        # Extreme acceleration
        if physics["measured_acceleration"] is not None:
            if abs(physics["measured_acceleration"]) > 50:
                warnings.append("DATA WARNING: Extreme measured acceleration")

        # Unrealistic change between readings (simple heuristic)
        if previous_physics is not None:
            dv = velocity - previous_reading["vertical_velocity"]
            dt = reading["mission_time"] - previous_reading["mission_time"]
            if dt > 0 and abs(dv / dt) > 100:
                warnings.append("DATA WARNING: Unrealistic change in velocity")

    # Pressure plausibility (very rough)
    if pressure < 50000 or pressure > 120000:
        warnings.append("DATA WARNING: Pressure outside typical range")

    # Temperature near absolute zero
    if temperature < -200:
        warnings.append("DATA WARNING: Temperature near unrealistic low value")

    # Wind speed negative (should be impossible due to input, but check anyway)
    if wind_speed < 0:
        warnings.append("DATA WARNING: Negative wind speed")

    return warnings


# ---------------------------------------------------------
# DISPLAY
# ---------------------------------------------------------

def display_analysis(reading, physics, warnings, mission_phase):
    print("\n=== Flight Analysis ===")
    print(f"Mission Phase: {mission_phase}")
    print(f"Weight: {physics['weight']:.2f} N")
    print(f"Potential Energy: {physics['potential_energy']:.2f} J")
    print(f"Kinetic Energy: {physics['kinetic_energy']:.2f} J")
    print(f"Momentum: {physics['momentum']:.2f} kg·m/s")

    if physics["landing_time"] is None:
        print("Estimated Landing Time: N/A")
        print("Estimated Total Wind Drift: N/A")
    else:
        print(f"Estimated Landing Time: {physics['landing_time']:.2f} s")
        if physics["total_wind_drift"] is not None:
            print(f"Estimated Total Wind Drift: {physics['total_wind_drift']:.2f} m")
            print(f"Estimated North Drift: {physics['north_drift']:.2f} m")
            print(f"Estimated East Drift: {physics['east_drift']:.2f} m")
        else:
            print("Estimated Wind Drift: N/A")

    if physics["measured_acceleration"] is None:
        print("Measured Acceleration: N/A")
    else:
        print(f"Measured Acceleration: {physics['measured_acceleration']:.2f} m/s²")

    print(f"Air Density: {physics['air_density']:.3f} kg/m³")
    print(f"Active Configuration: {physics['active_configuration']}")
    print(f"Active Area: {physics['active_area']:.4f} m²")
    print(f"Active Drag Coefficient: {physics['active_drag_coefficient']:.2f}")
    print(f"Drag Force: {physics['drag_force']:.2f} N")
    print(f"Net Vertical Force: {physics['net_vertical_force']:.2f} N")
    print(f"Force-Based Acceleration: {physics['force_based_acceleration']:.2f} m/s²")

    if physics["estimated_terminal_velocity"] is None:
        print("Estimated Terminal Velocity: N/A")
    else:
        print(f"Estimated Terminal Velocity: {physics['estimated_terminal_velocity']:.2f} m/s")

    print(f"North Position: {physics['north_position']:.2f} m")
    print(f"East Position: {physics['east_position']:.2f} m")
    print(f"Total Horizontal Displacement: {physics['horizontal_displacement']:.2f} m")

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
        physics = entry["physics"]
        mission_phase = entry["mission_phase"]
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
        print(f"Mission Phase: {mission_phase}")
        print(f"North Position: {physics['north_position']:.1f} m")
        print(f"East Position: {physics['east_position']:.1f} m")
        print(f"Horizontal Displacement: {physics['horizontal_displacement']:.1f} m")
        print(f"Status: {status}")


def display_mission_summary(setup, timesheet):
    readings = [entry["reading"] for entry in timesheet]
    physics_list = [entry["physics"] for entry in timesheet]
    final_reading = readings[-1]
    final_physics = physics_list[-1]

    maximum_altitude = max(r["altitude"] for r in readings)
    minimum_battery = min(r["battery_level"] for r in readings)
    maximum_wind = max(r["wind_speed"] for r in readings)
    average_wind = sum(r["wind_speed"] for r in readings) / len(readings)

    ascent_speeds = [r["vertical_velocity"] for r in readings if r["vertical_velocity"] > 0]
    descent_speeds = [abs(r["vertical_velocity"]) for r in readings if r["vertical_velocity"] < 0]

    maximum_ascent_speed = max(ascent_speeds) if ascent_speeds else 0
    maximum_descent_speed = max(descent_speeds) if descent_speeds else 0

    measured_accels = [
        p["measured_acceleration"]
        for p in physics_list
        if p["measured_acceleration"] is not None
    ]
    maximum_measured_acceleration = max(measured_accels) if measured_accels else 0

    maximum_drag_force = max(p["drag_force"] for p in physics_list)
    maximum_net_force = max(abs(p["net_vertical_force"]) for p in physics_list)

    terminal_velocities = [
        p["estimated_terminal_velocity"]
        for p in physics_list
        if p["estimated_terminal_velocity"] is not None
    ]
    estimated_terminal_velocity = terminal_velocities[-1] if terminal_velocities else None

    final_north = final_physics["north_position"]
    final_east = final_physics["east_position"]
    total_horizontal_displacement = final_physics["horizontal_displacement"]

    # Estimated landing direction (simple compass-style)
    def direction_from_components(north, east):
        if abs(north) < 1e-3 and abs(east) < 1e-3:
            return "At launch point"
        angle = math.degrees(math.atan2(east, north))
        if angle < 0:
            angle += 360
        if 45 <= angle < 135:
            return "East"
        if 135 <= angle < 225:
            return "South"
        if 225 <= angle < 315:
            return "West"
        return "North"

    estimated_landing_direction = direction_from_components(final_north, final_east)

    warning_count_safety = sum(
        1
        for entry in timesheet
        for msg in entry["warnings"]
        if msg.startswith("SAFETY WARNING")
    )
    warning_count_data = sum(
        1
        for entry in timesheet
        for msg in entry["warnings"]
        if msg.startswith("DATA WARNING")
    )

    final_statuses = timesheet[-1]["warnings"]

    if any("MISSION STATUS: SAFE LANDING" in msg for msg in final_statuses):
        landing_result = "Safe landing"
    elif any("MISSION STATUS: UNSAFE LANDING" in msg for msg in final_statuses):
        landing_result = "Unsafe landing"
    elif any("MISSION STATUS: LANDING DETECTED" in msg for msg in final_statuses):
        landing_result = "Landing detected (unclassified)"
    else:
        landing_result = "Mission ended before landing"

    battery_used = setup["starting_battery"] - final_reading["battery_level"]

    # Apogee time (highest altitude)
    apogee_index = max(range(len(readings)), key=lambda i: readings[i]["altitude"])
    apogee_time = readings[apogee_index]["mission_time"]

    print("\n=== ASTRA SAT Final Mission Summary ===")
    print(f"Mission Name: {setup['mission_name']}")
    print(f"Total Readings: {len(timesheet)}")
    print(f"Total Mission Time: {final_reading['mission_time']:.1f} s")
    print(f"Maximum Altitude: {maximum_altitude:.1f} m")
    print(f"Apogee Time: {apogee_time:.1f} s")
    print(f"Maximum Ascent Speed: {maximum_ascent_speed:.1f} m/s")
    print(f"Maximum Descent Speed: {maximum_descent_speed:.1f} m/s")
    print(f"Maximum Measured Acceleration: {maximum_measured_acceleration:.2f} m/s²")
    print(f"Average Wind Speed: {average_wind:.1f} m/s")
    print(f"Maximum Wind Speed: {maximum_wind:.1f} m/s")
    print(f"Minimum Battery: {minimum_battery:.1f}%")
    print(f"Battery Consumed: {battery_used:.1f}%")
    print(f"Maximum Drag Force: {maximum_drag_force:.2f} N")
    print(f"Maximum Net Force: {maximum_net_force:.2f} N")

    if estimated_terminal_velocity is None:
        print("Estimated Terminal Velocity: N/A")
    else:
        print(f"Estimated Terminal Velocity: {estimated_terminal_velocity:.2f} m/s")

    print(f"Final North Position: {final_north:.2f} m")
    print(f"Final East Position: {final_east:.2f} m")
    print(f"Total Horizontal Displacement: {total_horizontal_displacement:.2f} m")
    print(f"Estimated Landing Direction: {estimated_landing_direction}")
    print(f"Total Safety Warnings: {warning_count_safety}")
    print(f"Total Data Warnings: {warning_count_data}")
    print(f"Final Mission Result: {landing_result}")

    print("\nEstimated landing position:")
    print(f"{final_east:.1f} m East")
    print(f"{final_north:.1f} m North")
    print(f"{total_horizontal_displacement:.1f} m from launch")


# ---------------------------------------------------------
# EXPORT FUNCTIONS
# ---------------------------------------------------------

def export_mission_csv(setup, timesheet):
    os.makedirs("data", exist_ok=True)

    safe_name = setup["mission_name"].strip().lower().replace(" ", "_")
    filename = f"data/{safe_name}.csv"

    fieldnames = [
        "reading_number",
        "mission_time",
        "altitude",
        "vertical_velocity",
        "mission_phase",
        "measured_acceleration",
        "wind_speed",
        "wind_direction",
        "north_velocity",
        "east_velocity",
        "temperature",
        "pressure",
        "air_density",
        "battery_level",
        "parachute_deployed",
        "weight",
        "potential_energy",
        "kinetic_energy",
        "momentum",
        "landing_time",
        "north_drift",
        "east_drift",
        "total_wind_drift",
        "drag_force",
        "net_vertical_force",
        "force_based_acceleration",
        "estimated_terminal_velocity",
        "north_position",
        "east_position",
        "horizontal_displacement",
        "warnings",
        "notes",
    ]

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for entry in timesheet:
            reading = entry["reading"]
            physics = entry["physics"]

            writer.writerow({
                "reading_number": entry["reading_number"],
                "mission_time": reading["mission_time"],
                "altitude": reading["altitude"],
                "vertical_velocity": reading["vertical_velocity"],
                "mission_phase": entry["mission_phase"],
                "measured_acceleration": physics["measured_acceleration"],
                "wind_speed": reading["wind_speed"],
                "wind_direction": reading["wind_direction"],
                "north_velocity": physics["north_velocity"],
                "east_velocity": physics["east_velocity"],
                "temperature": reading["temperature"],
                "pressure": reading["pressure"],
                "air_density": physics["air_density"],
                "battery_level": reading["battery_level"],
                "parachute_deployed": reading["parachute_deployed"],
                "weight": physics["weight"],
                "potential_energy": physics["potential_energy"],
                "kinetic_energy": physics["kinetic_energy"],
                "momentum": physics["momentum"],
                "landing_time": physics["landing_time"],
                "north_drift": physics["north_drift"],
                "east_drift": physics["east_drift"],
                "total_wind_drift": physics["total_wind_drift"],
                "drag_force": physics["drag_force"],
                "net_vertical_force": physics["net_vertical_force"],
                "force_based_acceleration": physics["force_based_acceleration"],
                "estimated_terminal_velocity": physics["estimated_terminal_velocity"],
                "north_position": physics["north_position"],
                "east_position": physics["east_position"],
                "horizontal_displacement": physics["horizontal_displacement"],
                "warnings": "; ".join(entry["warnings"]),
                "notes": reading["notes"],
            })

    print(f"Mission data exported to {filename}")


def export_mission_setup(setup):
    os.makedirs("data", exist_ok=True)

    safe_name = setup["mission_name"].strip().lower().replace(" ", "_")
    filename = f"data/{safe_name}_setup.txt"

    with open(filename, "w", encoding="utf-8") as file:
        file.write("ASTRA SAT Mission Setup\n")
        file.write("------------------------\n")
        for key, value in setup.items():
            file.write(f"{key}: {value}\n")

    print(f"Mission setup exported to {filename}")


def export_mission_summary(setup, timesheet):
    os.makedirs("data", exist_ok=True)

    safe_name = setup["mission_name"].strip().lower().replace(" ", "_")
    filename = f"data/{safe_name}_summary.txt"

    readings = [entry["reading"] for entry in timesheet]
    physics_list = [entry["physics"] for entry in timesheet]
    final_reading = readings[-1]
    final_physics = physics_list[-1]

    maximum_altitude = max(r["altitude"] for r in readings)
    minimum_battery = min(r["battery_level"] for r in readings)
    maximum_wind = max(r["wind_speed"] for r in readings)
    average_wind = sum(r["wind_speed"] for r in readings) / len(readings)

    ascent_speeds = [r["vertical_velocity"] for r in readings if r["vertical_velocity"] > 0]
    descent_speeds = [abs(r["vertical_velocity"]) for r in readings if r["vertical_velocity"] < 0]

    maximum_ascent_speed = max(ascent_speeds) if ascent_speeds else 0
    maximum_descent_speed = max(descent_speeds) if descent_speeds else 0

    measured_accels = [
        p["measured_acceleration"]
        for p in physics_list
        if p["measured_acceleration"] is not None
    ]
    maximum_measured_acceleration = max(measured_accels) if measured_accels else 0

    maximum_drag_force = max(p["drag_force"] for p in physics_list)
    maximum_net_force = max(abs(p["net_vertical_force"]) for p in physics_list)

    terminal_velocities = [
        p["estimated_terminal_velocity"]
        for p in physics_list
        if p["estimated_terminal_velocity"] is not None
    ]
    estimated_terminal_velocity = terminal_velocities[-1] if terminal_velocities else None

    final_north = final_physics["north_position"]
    final_east = final_physics["east_position"]
    total_horizontal_displacement = final_physics["horizontal_displacement"]

    def direction_from_components(north, east):
        if abs(north) < 1e-3 and abs(east) < 1e-3:
            return "At launch point"
        angle = math.degrees(math.atan2(east, north))
        if angle < 0:
            angle += 360
        if 45 <= angle < 135:
            return "East"
        if 135 <= angle < 225:
            return "South"
        if 225 <= angle < 315:
            return "West"
        return "North"

    estimated_landing_direction = direction_from_components(final_north, final_east)

    warning_count_safety = sum(
        1
        for entry in timesheet
        for msg in entry["warnings"]
        if msg.startswith("SAFETY WARNING")
    )
    warning_count_data = sum(
        1
        for entry in timesheet
        for msg in entry["warnings"]
        if msg.startswith("DATA WARNING")
    )

    final_statuses = timesheet[-1]["warnings"]

    if any("MISSION STATUS: SAFE LANDING" in msg for msg in final_statuses):
        landing_result = "Safe landing"
    elif any("MISSION STATUS: UNSAFE LANDING" in msg for msg in final_statuses):
        landing_result = "Unsafe landing"
    elif any("MISSION STATUS: LANDING DETECTED" in msg for msg in final_statuses):
        landing_result = "Landing detected (unclassified)"
    else:
        landing_result = "Mission ended before landing"

    battery_used = setup["starting_battery"] - final_reading["battery_level"]

    apogee_index = max(range(len(readings)), key=lambda i: readings[i]["altitude"])
    apogee_time = readings[apogee_index]["mission_time"]

    with open(filename, "w", encoding="utf-8") as file:
        file.write("ASTRA SAT Final Mission Summary\n")
        file.write("--------------------------------\n")
        file.write(f"Mission Name: {setup['mission_name']}\n")
        file.write(f"Total Readings: {len(timesheet)}\n")
        file.write(f"Total Mission Time: {final_reading['mission_time']:.1f} s\n")
        file.write(f"Maximum Altitude: {maximum_altitude:.1f} m\n")
        file.write(f"Apogee Time: {apogee_time:.1f} s\n")
        file.write(f"Maximum Ascent Speed: {maximum_ascent_speed:.1f} m/s\n")
        file.write(f"Maximum Descent Speed: {maximum_descent_speed:.1f} m/s\n")
        file.write(f"Maximum Measured Acceleration: {maximum_measured_acceleration:.2f} m/s²\n")
        file.write(f"Average Wind Speed: {average_wind:.1f} m/s\n")
        file.write(f"Maximum Wind Speed: {maximum_wind:.1f} m/s\n")
        file.write(f"Minimum Battery: {minimum_battery:.1f}%\n")
        file.write(f"Battery Consumed: {battery_used:.1f}%\n")
        file.write(f"Maximum Drag Force: {maximum_drag_force:.2f} N\n")
        file.write(f"Maximum Net Force: {maximum_net_force:.2f} N\n")
        if estimated_terminal_velocity is None:
            file.write("Estimated Terminal Velocity: N/A\n")
        else:
            file.write(f"Estimated Terminal Velocity: {estimated_terminal_velocity:.2f} m/s\n")
        file.write(f"Final North Position: {final_north:.2f} m\n")
        file.write(f"Final East Position: {final_east:.2f} m\n")
        file.write(f"Total Horizontal Displacement: {total_horizontal_displacement:.2f} m\n")
        file.write(f"Estimated Landing Direction: {estimated_landing_direction}\n")
        file.write(f"Total Safety Warnings: {warning_count_safety}\n")
        file.write(f"Total Data Warnings: {warning_count_data}\n")
        file.write(f"Final Mission Result: {landing_result}\n")
        file.write("\nEstimated landing position:\n")
        file.write(f"{final_east:.1f} m East\n")
        file.write(f"{final_north:.1f} m North\n")
        file.write(f"{total_horizontal_displacement:.1f} m from launch\n")

    print(f"Mission summary exported to {filename}")


# ---------------------------------------------------------
# GRAPH FUNCTIONS
# ---------------------------------------------------------

def ensure_graph_folder():
    os.makedirs("data/graphs", exist_ok=True)


def plot_generic(times, values, xlabel, ylabel, title, filename):
    if len(times) < 2 or len(values) < 2:
        print(f"Graph skipped ({title}): Not enough data.")
        return

    ensure_graph_folder()
    plt.figure()
    plt.plot(times, values, marker="o")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    print(f"Graph saved: {filename}")


def plot_altitude(timesheet, mission_name):
    times = [entry["reading"]["mission_time"] for entry in timesheet]
    altitudes = [entry["reading"]["altitude"] for entry in timesheet]
    plot_generic(
        times,
        altitudes,
        "Mission Time (s)",
        "Altitude (m)",
        f"{mission_name} — Altitude vs Time",
        "data/graphs/altitude_vs_time.png",
    )


def plot_velocity(timesheet, mission_name):
    times = [entry["reading"]["mission_time"] for entry in timesheet]
    velocities = [entry["reading"]["vertical_velocity"] for entry in timesheet]
    plot_generic(
        times,
        velocities,
        "Mission Time (s)",
        "Vertical Velocity (m/s)",
        f"{mission_name} — Velocity vs Time",
        "data/graphs/velocity_vs_time.png",
    )


def plot_battery(timesheet, mission_name):
    times = [entry["reading"]["mission_time"] for entry in timesheet]
    battery = [entry["reading"]["battery_level"] for entry in timesheet]
    plot_generic(
        times,
        battery,
        "Mission Time (s)",
        "Battery Level (%)",
        f"{mission_name} — Battery vs Time",
        "data/graphs/battery_vs_time.png",
    )


def plot_acceleration(timesheet, mission_name):
    valid_entries = [
        entry for entry in timesheet
        if entry["physics"]["measured_acceleration"] is not None
    ]

    if len(valid_entries) < 2:
        print("Graph skipped (Acceleration): Not enough data.")
        return

    times = [entry["reading"]["mission_time"] for entry in valid_entries]
    accels = [entry["physics"]["measured_acceleration"] for entry in valid_entries]
    plot_generic(
        times,
        accels,
        "Mission Time (s)",
        "Measured Acceleration (m/s²)",
        f"{mission_name} — Acceleration vs Time",
        "data/graphs/acceleration_vs_time.png",
    )


def plot_temperature(timesheet, mission_name):
    times = [entry["reading"]["mission_time"] for entry in timesheet]
    temps = [entry["reading"]["temperature"] for entry in timesheet]
    plot_generic(
        times,
        temps,
        "Mission Time (s)",
        "Temperature (°C)",
        f"{mission_name} — Temperature vs Time",
        "data/graphs/temperature_vs_time.png",
    )


def plot_pressure(timesheet, mission_name):
    times = [entry["reading"]["mission_time"] for entry in timesheet]
    pressures = [entry["reading"]["pressure"] for entry in timesheet]
    plot_generic(
        times,
        pressures,
        "Mission Time (s)",
        "Pressure (Pa)",
        f"{mission_name} — Pressure vs Time",
        "data/graphs/pressure_vs_time.png",
    )


def plot_air_density(timesheet, mission_name):
    times = [entry["reading"]["mission_time"] for entry in timesheet]
    densities = [entry["physics"]["air_density"] for entry in timesheet]
    plot_generic(
        times,
        densities,
        "Mission Time (s)",
        "Air Density (kg/m³)",
        f"{mission_name} — Air Density vs Time",
        "data/graphs/air_density_vs_time.png",
    )


def plot_drag_force(timesheet, mission_name):
    times = [entry["reading"]["mission_time"] for entry in timesheet]
    drag_forces = [entry["physics"]["drag_force"] for entry in timesheet]
    plot_generic(
        times,
        drag_forces,
        "Mission Time (s)",
        "Drag Force (N)",
        f"{mission_name} — Drag Force vs Time",
        "data/graphs/drag_force_vs_time.png",
    )


def plot_net_vertical_force(timesheet, mission_name):
    times = [entry["reading"]["mission_time"] for entry in timesheet]
    net_forces = [entry["physics"]["net_vertical_force"] for entry in timesheet]
    plot_generic(
        times,
        net_forces,
        "Mission Time (s)",
        "Net Vertical Force (N)",
        f"{mission_name} — Net Vertical Force vs Time",
        "data/graphs/net_vertical_force_vs_time.png",
    )


def plot_horizontal_path(timesheet, mission_name):
    east_positions = [entry["physics"]["east_position"] for entry in timesheet]
    north_positions = [entry["physics"]["north_position"] for entry in timesheet]

    if len(east_positions) < 2 or len(north_positions) < 2:
        print("Graph skipped (Horizontal path): Not enough data.")
        return

    ensure_graph_folder()
    plt.figure()
    plt.plot(east_positions, north_positions, marker="o", label="Flight path")
    plt.scatter([0], [0], color="green", label="Launch point")
    plt.scatter([east_positions[-1]], [north_positions[-1]], color="red", label="Final position")
    plt.xlabel("East Position (m)")
    plt.ylabel("North Position (m)")
    plt.title(f"{mission_name} — Horizontal Flight Path")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("data/graphs/horizontal_path.png")
    plt.close()
    print("Graph saved: data/graphs/horizontal_path.png")


def generate_mission_graphs(setup, timesheet):
    mission_name = setup["mission_name"]
    plot_altitude(timesheet, mission_name)
    plot_velocity(timesheet, mission_name)
    plot_acceleration(timesheet, mission_name)
    plot_battery(timesheet, mission_name)
    plot_temperature(timesheet, mission_name)
    plot_pressure(timesheet, mission_name)
    plot_air_density(timesheet, mission_name)
    plot_drag_force(timesheet, mission_name)
    plot_net_vertical_force(timesheet, mission_name)
    plot_horizontal_path(timesheet, mission_name)
    print("Mission graphs generated.")


# ---------------------------------------------------------
# MAIN PROGRAM FLOW
# ---------------------------------------------------------

def main():
    setup = collect_mission_setup()
    mission_timesheet = []

    print("\nSetup confirmation complete. Beginning mission...\n")

    while True:
        previous_entry = mission_timesheet[-1] if mission_timesheet else None
        previous_reading = previous_entry["reading"] if previous_entry else None
        previous_physics = previous_entry["physics"] if previous_entry else None
        previous_time = previous_reading["mission_time"] if previous_reading else None

        reading = collect_flight_reading(previous_time)
        physics = calculate_physics(setup, reading, previous_reading, previous_physics)
        mission_phase = classify_mission_phase(reading, previous_reading)
        warnings = generate_warnings(setup, reading, previous_reading, physics, previous_physics)

        entry = {
            "reading_number": len(mission_timesheet) + 1,
            "reading": reading,
            "physics": physics,
            "warnings": warnings,
            "mission_phase": mission_phase,
        }

        mission_timesheet.append(entry)

        display_analysis(reading, physics, warnings, mission_phase)

        if reading["altitude"] <= 0:
            print("\nMission end: Landing detected.")
            break

        if not get_yes_no("Enter another flight reading? (yes/no): "):
            print("\nMission end: Manual termination.")
            break

    display_timesheet(mission_timesheet)
    display_mission_summary(setup, mission_timesheet)

    if get_yes_no("Export mission data? (yes/no): "):
        export_mission_csv(setup, mission_timesheet)
        export_mission_setup(setup)
        export_mission_summary(setup, mission_timesheet)

    if get_yes_no("Generate mission graphs? (yes/no): "):
        generate_mission_graphs(setup, mission_timesheet)

    print("\nASTRA SAT Manual Input Edition v1.0 — Mission complete.")


if __name__ == "__main__":
    main()
