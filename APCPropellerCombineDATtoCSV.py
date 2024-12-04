#This program accepts a folder of APC .dat files and processes them into a .csv format for further manipulation
#Created by Aaron Hess


import os
import csv
from ast import parse

import pandas as pd

import re

def remove_non_numeric(string):
  return re.sub(r'[^0-9.]', '', string)


def parse_dat_file(file_path):
    rpm_data = {}
    current_rpm = None
    data_block = []

    with open(file_path, 'r') as file:
        for line in file:
            if '.dat' in line:
                diameter = line.split()[0].split('x')[0]
                pitch = remove_non_numeric(line.split()[0].split('x')[1])
            if "PROP RPM" in line:
                if current_rpm is not None and data_block:
                    rpm_data[current_rpm] = data_block  # Store raw data block without headers
                current_rpm = int(line.split('=')[-1].strip())
                data_block = []
            elif line.strip() and current_rpm is not None:
                values = line.split()
                if len(values) >= 8:
                    try:
                        velocity = float(values[0])
                        thrust = float(values[7])
                        torque = float(values[9])
                        advRatio = float(values[1])
                        Reynolds = float(values[13])
                        data_block.append([diameter, pitch, current_rpm, velocity, thrust, torque, advRatio, Reynolds])
                    except ValueError:
                        continue

    if current_rpm is not None and data_block:
        rpm_data[current_rpm] = data_block  # Store raw data block without headers

    return rpm_data


def process_folder(input_folder, output_csv):
    """Processes all data files in the input folder and writes to an output CSV."""
    all_data = []
    for filename in os.listdir(input_folder):
        if filename.endswith('.dat'):  # Only process .dat files
            filepath = os.path.join(input_folder, filename)
            file_data = parse_dat_file(filepath)

            # Flatten data: Extract rows from each RPM's data block
            for rpm, data_block in file_data.items():
                all_data.extend(data_block)

    # Write the collected data to a CSV file
    with open(output_csv, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        # Write header
        csv_writer.writerow(['Diameter', 'Pitch', 'RPM', 'Velocity (mph)', 'Thrust (lbf)', 'Torque (in-lbf)', 'Advance Ratio', 'Reynolds Number'])
        # Write all rows
        csv_writer.writerows(all_data)

    print(f"Data has been written to {output_csv}")


# Specify the folder containing data files and the output CSV file
input_folder = 'C:\\Users\\aug30\\Downloads\\PERFILES_WEB-202410\\PERFILES_WEB\\PERFILES2'  # Replace with the actual folder path
output_csv = 'all_props_data.csv'

# Run the processing function
process_folder(input_folder, output_csv)
