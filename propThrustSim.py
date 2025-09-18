# This program imports an APC DAT file of thrust data and models the dynamic thrust as a function of velocity.
# It can also interpolate a point given a specific RPM and Velocity

# Created by Aaron Hess


import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Function to parse the .dat file and extract data blocks for each RPM
def parse_dat_file(file_path):
    rpm_data = {}
    current_rpm = None
    data_block = []

    with open(file_path, 'r') as file:
        for line in file:
            if "PROP RPM" in line:
                if current_rpm is not None and data_block:
                    rpm_data[current_rpm] = pd.DataFrame(data_block, columns=['V', 'Thrust'])
                current_rpm = int(line.split('=')[-1].strip())
                data_block = []
            elif line.strip() and current_rpm is not None:
                values = line.split()
                if len(values) >= 8:
                    try:
                        velocity = float(values[0])
                        thrust = float(values[7])
                        data_block.append([velocity, thrust])
                    except ValueError:
                        continue

    if current_rpm is not None and data_block:
        rpm_data[current_rpm] = pd.DataFrame(data_block, columns=['V', 'Thrust'])

    return rpm_data

# Interpolation function for a given RPM and velocity, including interpolation between RPMs
def interpolate_thrust(rpm_data, target_rpm, target_velocity):
    available_rpms = sorted(rpm_data.keys())
    if target_rpm in available_rpms:
        # Direct interpolation for the target RPM
        data = rpm_data[target_rpm]
        thrust_interp = interp1d(data['V'], data['Thrust'], kind='linear', fill_value="extrapolate")
        return thrust_interp(target_velocity), None
    else:
        # Interpolate between the two nearest RPMs
        lower_rpm = max(r for r in available_rpms if r < target_rpm) if any(r < target_rpm for r in available_rpms) else None
        upper_rpm = min(r for r in available_rpms if r > target_rpm) if any(r > target_rpm for r in available_rpms) else None

        if lower_rpm is None or upper_rpm is None:
            return None, "Target RPM is out of the range of available data."

        # Interpolate thrust at target_velocity for both the lower and upper RPMs
        lower_data = rpm_data[lower_rpm]
        upper_data = rpm_data[upper_rpm]
        lower_interp = interp1d(lower_data['V'], lower_data['Thrust'], kind='linear', fill_value="extrapolate")
        upper_interp = interp1d(upper_data['V'], upper_data['Thrust'], kind='linear', fill_value="extrapolate")
        thrust_lower = lower_interp(target_velocity)
        thrust_upper = upper_interp(target_velocity)

        # Interpolate between the thrust values of the two RPMs
        thrust_interpolated = np.interp(target_rpm, [lower_rpm, upper_rpm], [thrust_lower, thrust_upper])
        return thrust_interpolated, None

# Curve fitting function for thrust as a function of velocity
def fit_thrust_curve(rpm_data, target_rpm):
    if target_rpm not in rpm_data:
        return None, f"RPM {target_rpm} not found in data."

    def thrust_curve(velocity, a, b, c):
        return a * velocity ** 2 + b * velocity + c

    data = rpm_data[target_rpm]
    popt, _ = curve_fit(thrust_curve, data['V'], data['Thrust'])
    return popt, None

# Load and parse the .dat file
file_path = 'PER3_27x13E.dat'  # Replace with your actual file path
rpm_data = parse_dat_file(file_path)

# Interpolate thrust at a specific RPM and velocity
target_rpm = 3000# Target RPM for interpolation, not directly in available RPM data
target_velocity = 0  # Target velocity for interpolation in mph
thrust, error = interpolate_thrust(rpm_data, target_rpm, target_velocity)
if error:
    print(error)
else:
    print(f"Interpolated thrust at {target_rpm} RPM and {target_velocity} mph: {thrust:.2f} lbs")
    print()

# Fit a curve to thrust as a function of velocity for the nearest available RPM
nearest_rpm = min(rpm_data.keys(), key=lambda r: abs(r - target_rpm))
fit_params, error = fit_thrust_curve(rpm_data, nearest_rpm)
if error:
    print(error)
else:
    print(f"Fitted curve parameters (a, b, c) for thrust at {nearest_rpm} RPM: {fit_params}")
    a, b, c = fit_params

    # Generate x values for plotting
    x = np.linspace(0, 30, 400)  # Velocity range for plotting (0 to 30 mph)
    # Calculate thrust values based on the fitted quadratic function
    y = a * x ** 2 + b * x + c

    # Plot the fitted thrust curve
    plt.figure(figsize=(8, 6))
    plt.plot(x, y, label=f"$y = {a:.3f}x^2 + {b:.3f}x + {c:.3f}$")  # Display equation on plot
    plt.xlabel("Velocity (mph)")
    plt.ylabel("Thrust (lbs)")
    plt.title(f"Thrust Curve Fit at Nearest RPM ({nearest_rpm} RPM)")
    plt.axhline(0, color='black', linewidth=0.5)  # X-axis
    plt.axvline(0, color='black', linewidth=0.5)  # Y-axis
    plt.legend()
    plt.grid(True)
    plt.show()
