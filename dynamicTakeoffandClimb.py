import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import interp1d

# Constants
g = 32.174  # Acceleration due to gravity, ft/s^2


# Function to read Cl and Cd data from CSV files
def load_airfoil_data(filename, airfoil_name):
    df = pd.read_csv(filename)
    df = df[df["Name"].str.contains(airfoil_name, case=False, na=False)]  # Filter by airfoil name
    reynolds_numbers = df["Reynold's Number"].unique()
    airfoil_data = {Re: df[df["Reynold's Number"] == Re] for Re in reynolds_numbers}
    return airfoil_data



# Function to interpolate Cl and Cd
def get_aero_coeffs(airfoil_data, reynolds, alpha):
    reynolds_numbers = sorted(airfoil_data.keys())
    lower_re = max([Re for Re in reynolds_numbers if Re <= reynolds], default=reynolds_numbers[0])
    upper_re = min([Re for Re in reynolds_numbers if Re >= reynolds], default=reynolds_numbers[-1])

    lower_data = airfoil_data[lower_re]
    upper_data = airfoil_data[upper_re]

    cl_lower = interp1d(lower_data['Alpha'], lower_data['CL'], fill_value='extrapolate')(alpha)
    cd_lower = interp1d(lower_data['Alpha'], lower_data['CD'], fill_value='extrapolate')(alpha)
    cl_upper = interp1d(upper_data['Alpha'], upper_data['CL'], fill_value='extrapolate')(alpha)
    cd_upper = interp1d(upper_data['Alpha'], upper_data['CD'], fill_value='extrapolate')(alpha)

    if lower_re == upper_re:
        return cl_lower, cd_lower

    re_ratio = (reynolds - lower_re) / (upper_re - lower_re)
    cl = cl_lower + re_ratio * (cl_upper - cl_lower)
    cd = cd_lower + re_ratio * (cd_upper - cd_lower)

    return cl, cd


# Function to simulate takeoff and climb
def takeoff_and_climb_simulation(wing_area, mass, rho, runway_length, simulation_length, step_size, chord_length, kinematic_viscosity,
                                 thrust_curve, airfoil_data):
    weight = mass * g
    position, velocity, altitude, time = 0, 0, 0, 0.0
    alpha = 0

    position_list, velocity_list, altitude_list, thrust_list, lift_list, drag_list, alpha_list = [], [], [], [], [], [], []

    while position < simulation_length:
        reynolds = (velocity * chord_length) / kinematic_viscosity
        cl, cd = get_aero_coeffs(airfoil_data, reynolds, alpha)

        lift = 0.5 * rho * cl * wing_area * velocity ** 2
        drag = 0.5 * rho * cd * wing_area * velocity ** 2
        thrust = velocity * thrust_curve[0] ** 2 + velocity * thrust_curve[1] + thrust_curve[2]
        net_force = thrust - drag
        acceleration = net_force / mass

        velocity += acceleration * step_size
        position += velocity * step_size

        if lift >= weight:
            altitude += velocity * math.sin(math.radians(alpha)) * step_size
            alpha = min(alpha + 0.1, 10)  # Slowly increase AoA during climb

        position_list.append(position)
        velocity_list.append(velocity)
        altitude_list.append(altitude)
        thrust_list.append(thrust)
        lift_list.append(lift)
        drag_list.append(drag)
        alpha_list.append(alpha)
        time += step_size

    plt.figure(figsize=(12, 6))
    plt.subplot(3, 2, 1)
    plt.plot(position_list, thrust_list, label='Thrust')
    plt.xlabel('Position (ft)')
    plt.ylabel('Thrust (lbf)')
    plt.title('Thrust vs Position')
    plt.grid(True)

    plt.subplot(3, 2, 2)
    plt.plot(position_list, lift_list, label='Lift')
    plt.xlabel('Position (ft)')
    plt.ylabel('Lift (lbf)')
    plt.title('Lift vs Position')
    plt.grid(True)

    plt.subplot(3, 2, 3)
    plt.plot(position_list, altitude_list, label='Altitude', color='orange')
    plt.xlabel('Position (ft)')
    plt.ylabel('Altitude (ft)')
    plt.title('Altitude vs Position')
    plt.grid(True)

    plt.subplot(3, 2, 4)
    plt.plot(position_list, velocity_list, label='Velocity', color='green')
    plt.xlabel('Position (ft)')
    plt.ylabel('Velocity (ft/s)')
    plt.title('Velocity vs Position')
    plt.grid(True)

    plt.subplot(3, 2, 5)
    plt.plot(position_list, drag_list, label='Drag', color='red')
    plt.xlabel('Position (ft)')
    plt.ylabel('Drag (lbf)')
    plt.title('Drag vs Position')
    plt.grid(True)

    plt.subplot(3, 2, 6)
    plt.plot(position_list, alpha_list, label='AOA', color='orange')
    plt.xlabel('Position (ft)')
    plt.ylabel('Angle of Attack (degrees)')
    plt.title('Angle of Attack vs Position')
    plt.grid(True)

    plt.tight_layout()
    plt.show()


# Specify the airfoil you want to use
selected_airfoil = "goe244-il"  # Change this to the airfoil of interest

# Load data only for that airfoil
airfoil_data = load_airfoil_data('foil_data_new_pg1-80.csv', selected_airfoil)

# Example parameters
wing_area = 31.467
mass = 45 / 32.2
rho = 0.0023769
runway_length = 90
simulation_length = 300
step_size = 0.001
chord_length = 29 / 12
kinematic_viscosity = 0.00015723
thrust_curve = [-3.47418e-03, -7.88148e-02, 1.327000e+01]

# Run simulation
takeoff_and_climb_simulation(wing_area, mass, rho, runway_length, simulation_length, step_size, chord_length, kinematic_viscosity,
                             thrust_curve, airfoil_data)
