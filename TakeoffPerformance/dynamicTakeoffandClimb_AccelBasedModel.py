import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import interp1d

# Constants
g = 32.174  # ft/s^2


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


# Function to simulate takeoff and climb (acceleration-based)
def takeoff_and_climb_simulation(wing_area, mass, rho, runway_length, simulation_length, step_size,
                                 chord_length, kinematic_viscosity, thrust_curve, airfoil_data):
    weight = mass * g                       # lbf downward
    x_pos, u_vel, z_alt, w_vel, time = 0.0, 0.0, 0.0, 0.0, 0.0
    alpha = 0.0                             # degrees

    position_list, velocity_list, altitude_list = [], [], []
    thrust_list, lift_list, drag_list, alpha_list = [], [], [], []

    while x_pos < simulation_length:
        # Reynolds (avoid divide-by-zero)
        reynolds = (u_vel * chord_length) / kinematic_viscosity if u_vel > 1e-6 else 1e3
        cl, cd = get_aero_coeffs(airfoil_data, reynolds, alpha)

        # Aerodynamic forces (assume lift acts perpendicular to free-stream, drag along stream)
        q = 0.5 * rho * u_vel ** 2                 # dynamic pressure (use horizontal speed)
        lift = q * cl * wing_area                  # lbf upward
        drag = q * cd * wing_area                  # lbf, opposes forward motion

        # Thrust as quadratic in (forward) velocity: T(V) = A*V^2 + B*V + C
        A, B, C = thrust_curve
        thrust_total = A * u_vel ** 2 + B * u_vel + C

        # Assume thrust direction aligned with aircraft body (alpha). If you want thrust always horizontal,
        # set thrust_x = thrust_total; thrust_z = 0.0
        alpha_rad = math.radians(alpha)
        thrust_x = thrust_total * math.cos(alpha_rad)
        thrust_z = thrust_total * math.sin(alpha_rad)

        # Horizontal dynamics
        # Drag direction: opposite u_vel. If u_vel ~ 0, assume small drag direction = 0
        # For simplicity keep drag acting purely opposite to u_vel (horizontal)
        net_x = thrust_x - drag
        a_x = net_x / mass               # ft/s^2

        # Vertical dynamics
        # Upward forces: lift + vertical component of thrust. Downward: weight.
        net_z = lift + thrust_z - weight
        a_z = net_z / mass               # ft/s^2

        # Integrate (explicit Euler)
        u_vel += a_x * step_size
        x_pos += u_vel * step_size

        w_vel += a_z * step_size
        z_alt += w_vel * step_size

        # Ground contact: prevent penetrating ground, simple contact model
        if z_alt < 0.0:
            z_alt = 0.0
            if w_vel < 0.0:
                w_vel = 0.0  # zero vertical speed on impact (inelastic)

        # Angle of attack control (preserve your previous behavior)
        # Only ramp AoA once in ground roll end-of-runway or when lift >= weight (airborne)
        if lift >= weight or x_pos >= runway_length * 0.9:
            alpha = min(alpha + 0.1, 5.0)  # deg

        # Save data
        position_list.append(x_pos)
        velocity_list.append(u_vel)
        altitude_list.append(z_alt)
        thrust_list.append(thrust_total)
        lift_list.append(lift)
        drag_list.append(drag)
        alpha_list.append(alpha)

        time += step_size

        # small safety break to avoid infinite loop if something goes wrong
        if time > 60.0:   # 60 s limit
            break

    # plotting (same as before)
    plt.figure(figsize=(12, 6))
    plt.subplot(3, 2, 1)
    plt.plot(position_list, thrust_list, label='Thrust')
    plt.xlabel('Position (ft)'); plt.ylabel('Thrust (lbf)'); plt.title('Thrust vs Position'); plt.grid(True)

    plt.subplot(3, 2, 2)
    plt.plot(position_list, lift_list, label='Lift')
    plt.xlabel('Position (ft)'); plt.ylabel('Lift (lbf)'); plt.title('Lift vs Position'); plt.grid(True)

    plt.subplot(3, 2, 3)
    plt.plot(position_list, altitude_list, label='Altitude', color='orange')
    plt.xlabel('Position (ft)'); plt.ylabel('Altitude (ft)'); plt.title('Altitude vs Position'); plt.grid(True)

    plt.subplot(3, 2, 4)
    plt.plot(position_list, velocity_list, label='Velocity', color='green')
    plt.xlabel('Position (ft)'); plt.ylabel('Velocity (ft/s)'); plt.title('Velocity vs Position'); plt.grid(True)

    plt.subplot(3, 2, 5)
    plt.plot(position_list, drag_list, label='Drag', color='red')
    plt.xlabel('Position (ft)'); plt.ylabel('Drag (lbf)'); plt.title('Drag vs Position'); plt.grid(True)

    plt.subplot(3, 2, 6)
    plt.plot(position_list, alpha_list, label='AOA', color='orange')
    plt.xlabel('Position (ft)'); plt.ylabel('Angle of Attack (deg)'); plt.title('Angle of Attack vs Position'); plt.grid(True)

    plt.tight_layout()
    plt.show()


# Example usage
selected_airfoil = "Airfoil,clarkysm-il"  # Change this to your airfoil
airfoil_data = load_airfoil_data('../AirfoilScraperAndData/foil_data_new_pg1-80.csv', selected_airfoil)

wing_area = 5
mass = 2.5 / 32.2  # slugs
rho = 0.0023769
runway_length = 10
simulation_length = 100
step_size = 0.001
chord_length = 12 / 12
kinematic_viscosity = 0.00015723
thrust_curve = [-1.34264307e-04, -2.03613928e-03, 2.23465198e+00]

takeoff_and_climb_simulation(wing_area, mass, rho, runway_length, simulation_length,
                             step_size, chord_length, kinematic_viscosity,
                             thrust_curve, airfoil_data)


