import pandas as pd
import math
import csv
import os

# --- Define the name of the input file ---
file_name = '../AirfoilScraperAndData/foil_data_symmetric.csv'

# --- Safety Check: Ensure the file exists before running ---
if not os.path.exists(file_name):
    print(f"FATAL ERROR: The input file '{file_name}' was not found.")
    print("Please ensure the CSV file is uploaded and accessible.")
else:
    # --- If file exists, proceed with the full program ---
    print(f"Successfully located '{file_name}'. Starting analysis...")

    df = pd.read_csv(file_name)

    # --- User-defined constants and parameters ---
    weight = 3  # pounds
    AirDensity = 0.002378  # slugs/ft^3
    g = 32.17  # ft/s^2
    coefRollFrict = 0.05
    wing_area_min = 0.75  # ft^2
    wing_area_max = 4.5  # ft^2
    wing_area_step = 0.1
    max_thrust = 2  # pounds
    takeoff_distance = 10  # feet


    # --- Physics Calculation Functions (from your original code) ---
    def NeededTakeoffVelocity(W, density, CLMax, WingArea):
        if density * WingArea * CLMax <= 0:
            return float('inf')
        Vstall = math.sqrt((2 * W) / (density * WingArea * CLMax))
        VLo = 1.2 * Vstall
        return VLo


    def TakeoffLift(density, CL, WingArea, VLo):
        L = 0.5 * density * ((0.7 * VLo) ** 2) * WingArea * CL
        return L


    def TakeoffDrag(density, CD, WingArea, VLo):
        D = 0.5 * density * ((0.7 * VLo) ** 2) * WingArea * CD
        return D


    def TakeoffResistiveForce(Drag, CoefFrictRoll, W, Lift):
        Rav = Drag + CoefFrictRoll * (W - Lift)
        return Rav


    def ThrustForDistance(W, g, density, WingArea, CLMax, Distance, Rav):
        denominator = Distance * g * density * WingArea * CLMax
        if denominator == 0:
            return float('inf')
        T = (1.44 * (W ** 2)) / denominator + Rav
        return T


    # --- Data Processing ---
    output_file_path = "takeoff_performance_results.csv"
    header = [
        "Airfoil", "Reynolds_Number", "Alpha", "CL", "CD", "CLMax",
        "Wing_Area_sq_ft", "Takeoff_Velocity_ft_s", "Thrust_Needed_lbs"
    ]
    with open(output_file_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(header)

    # Clean the 'Name' column to get a simple airfoil identifier
    df['Airfoil'] = df['Name'].apply(lambda x: x.split(',')[1].strip())

    # Group data by each unique airfoil and Reynold's number combination
    grouped = df.groupby(['Airfoil', "Reynold's Number"])

    # Main processing loop
    for (airfoil_name, reynolds_num), subset_df in grouped:

        # Determine CLMax for this specific configuration
        CLMax = subset_df['CL'].max()

        if CLMax <= 0:
            continue  # Cannot generate lift, skip this entire airfoil/Re combo

        # Iterate through each angle of attack for this configuration
        for index, row in subset_df.iterrows():
            CL = row['CL']
            CD = row['CD']
            alpha = row['Alpha']

            if CL <= 0 or CD <= 0 or alpha != 0:
                continue

            # Iterate through the specified range of wing areas
            current_wing_area = wing_area_min
            while current_wing_area <= wing_area_max:
                Vlo = NeededTakeoffVelocity(weight, AirDensity, CLMax, current_wing_area)
                if math.isinf(Vlo):
                    current_wing_area += wing_area_step
                    continue

                Lift = TakeoffLift(AirDensity, CL, current_wing_area, Vlo)
                Drag = TakeoffDrag(AirDensity, CD, current_wing_area, Vlo)
                Rav = TakeoffResistiveForce(Drag, coefRollFrict, weight, Lift)
                ThrustNeeded = ThrustForDistance(weight, g, AirDensity, current_wing_area, CLMax, takeoff_distance, Rav)

                if ThrustNeeded < max_thrust:
                    # If required thrust is within limits, save the results
                    data_to_write = [
                        airfoil_name, reynolds_num, alpha, CL, CD, CLMax,
                        round(current_wing_area, 3), round(Vlo, 2), round(ThrustNeeded, 2)
                    ]
                    with open(output_file_path, mode="a", newline="") as file:
                        writer = csv.writer(file)
                        writer.writerow(data_to_write)

                current_wing_area += wing_area_step

    print(f"\nProcessing complete. Results are saved in '{output_file_path}'")

    # Display the head of the results file
    results_df = pd.read_csv(output_file_path)
    print(f"Found {len(results_df)} possible design combinations.")
    print("\nHere are the first 10 results:")
    print(results_df.head(10))