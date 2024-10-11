import math

import numpy as np
import matplotlib.pyplot as plt

# Constants
g = 32.174  # Acceleration due to gravity, ft/s^2


# Function to calculate the thrust based on motor characteristics
def calculate_thrust(kv, horsepower, prop_diameter, prop_pitch, velocity):
    # Simplified model for thrust: thrust = motor power / velocity (approximate)
    # Assuming horsepower converted to ft-lb/s
    power = horsepower * 550  # 1 HP = 550 ft-lb/s
    max_rpm = kv * (power ** 0.5)
    thrust = (max_rpm / (velocity + 1)) * (prop_diameter * prop_pitch)
    thrust /= 32.174  # Convert from lb to lbf (pound-force)
    return thrust


def calculate_rolling_resistance(Cr, weight):
    return Cr * weight

# Function to calculate lift in imperial units
def calculate_lift(rho, Cl, wing_area, velocity):
    return 0.5 * rho * Cl * wing_area * velocity ** 2

# Function to calculate lift in imperial units
def calculate_veloNeeded(rho, Cl, wing_area, weight):
    velocity = math.sqrt((2 * weight) / (rho * wing_area * Cl))
    return velocity

# Function to calculate drag in imperial units
def calculate_drag(rho, Cd, wing_area, velocity):
    return 0.5 * rho * Cd * wing_area * velocity ** 2


# Main function to model takeoff
def takeoff_simulation(wing_area, mass, rho, Cl, Cd, Cr, kv, horsepower, prop_diameter, prop_pitch, runway_length,
                       step_size, chord_length, kinematic_viscosity):

    # Other calculations and definitions
    reynoldsOptions = [50000, 100000, 200000, 500000] # Options for reynold's number (based on airfoiltools data)
    time_step = step_size  # Time step for simulation (passed in from outside function)
    weight = mass * g  # Convert mass to weight in pounds-force (lbf)

    # Initial Values
    position = 0  # x0
    velocity = 0  # v0
    time = 0.0  # t0
    lift = 0.0
    drag = 0.0
    rolling_resistance = 0.0
    thrust = 7.952 #Thrust in lbs
    net_force = thrust - drag - rolling_resistance

    takeoffVeloFactor = 1.2 # Defines what safety factor the velocity must be at to trigger takeoff
    reynoldsIndex = 0  # The selected index in reynoldsOptions, changes position in list to change the Cl and Cd values used

    # Lists to store data over iterations
    timeList = []
    positionList = []
    velocityList = []
    thrustList = []
    liftList = []
    reynoldsList = []

    #Main loop to iterate time and calculate results
    while position < runway_length:
        #Inner loop to determine if it can transition from 0 degree alpha to a higher AoA to take off
        # Update kinematics (F = ma -> a = F/m)
        acceleration = net_force / mass
        velocity += acceleration * time_step
        position += velocity * time_step
        reynolds = (velocity * chord_length) / kinematic_viscosity  # Dynamic Reynolds Number (changes with velocity)

        if reynoldsOptions[reynoldsIndex] < 500000 and reynolds > reynoldsOptions[
            reynoldsIndex]:  # Checks if the approximate reynold's number being used for Cl and Cd needs changed
            reynoldsIndex += 1


        lift = calculate_lift(rho, Cl, wing_area, velocity)
        drag = calculate_drag(rho, Cd, wing_area, velocity)
        rolling_resistance = calculate_rolling_resistance(Cr, weight)
        net_force = thrust - drag - rolling_resistance
        time += time_step


        # Store data for plotting
        positionList.append(position)
        velocityList.append(velocity)
        thrustList.append(thrust)
        liftList.append(lift)
        reynoldsList.append(reynolds)


    # Plot the results
    plt.figure(figsize=(10, 10))

    # Plot thrust vs position
    plt.subplot(2, 2, 1)
    plt.plot(positionList, thrustList, label='Thrust')
    plt.xlabel('Position (ft)')
    plt.ylabel('Thrust (lbf)')
    plt.title('Thrust vs Position')
    plt.grid(True)

    # Plot Lift vs position
    plt.subplot(2, 2, 2)
    plt.plot(positionList, liftList, label='Lift')
    plt.xlabel('Position (ft)')
    plt.ylabel('Lift (lbf)')
    plt.title('Lift vs Position')
    plt.grid(True)

    # Plot velocity vs position
    plt.subplot(2, 2, 3)
    plt.plot(positionList, velocityList, label='Velocity', color='orange')
    plt.xlabel('Position (ft)')
    plt.ylabel('Velocity (ft/s)')
    plt.title('Velocity vs Position')
    plt.grid(True)

    # Plot Reynolds Number vs position
    plt.subplot(2, 2, 4)
    plt.plot(positionList, reynoldsList, label='Reynold\'s Number', color='orange')
    plt.xlabel('Position (ft)')
    plt.ylabel('Reynold\'s Number')
    plt.title('Reynold\'s Number vs Position')
    plt.grid(True)

    plt.tight_layout()
    plt.show()


# Example usage
wing_area = 31.467  # ft^2
mass = 45/32.2  # slugs (5 lb, use lb/g to convert)
rho = 0.0023769  # slugs/ft^3, air density at sea level
Cl = 1.2045  # Coefficient of lift
Cd = 0.01643  # Coefficient of drag
Cr = .02 # Coefficient of Rolling Resistance
kv = 370  # Motor kv rating
horsepower = 1.01  # Motor power in HP
prop_diameter = 17/12.0  # Propeller diameter in feet
prop_pitch = 7/12.0  # Propeller pitch in feet
runway_length = 100  # Runway length in feet
step_size = 0.001  # Step size for simulation (in s)
chord_length = 29/12 # Chord Length in feet
kinematic_viscosity = .00015723 # Kinematic Viscosity at Sea Level (ft2/s)

# Run the simulation
takeoff_simulation(wing_area, mass, rho, Cl, Cd, Cr, kv, horsepower, prop_diameter, prop_pitch, runway_length, step_size, chord_length, kinematic_viscosity)