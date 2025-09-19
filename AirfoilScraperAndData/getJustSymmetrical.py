## We can assume that in the case of a symmetric airfoil, the Cl will be very low at 0 degree AoA
## We will filter those with a very small AoA and use that to find symmetrics

import csv

all_airfoils = []
symmetrical_airfoil_names = []
symmetrical_airfoil_data = []

#Define file path of CSV with airfoil data
csv_file_path = '../AirfoilScraperAndData/foil_data_new_pg1-80.csv'

#Open CSV File with Scraped Airfoil data. Save data to list named Data
try:
    with open(csv_file_path, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            all_airfoils.append(row)
except FileNotFoundError:
    print("File not found.")
except Exception as e:
    print(f"An error occurred: {e}")

for i in range(1,len(all_airfoils),1):
    if float(all_airfoils[i][3]) == 0:
        if 0.005 > float(all_airfoils[i][4]) > -0.005:
            symmetrical_airfoil_names.append(all_airfoils[i][0])

filtered_list = [
    row for row in all_airfoils
    if row[0] in symmetrical_airfoil_names
]

file_path = "foil_data_symmetric.csv"
with open(file_path, mode="w", newline="") as file:
    writer = csv.writer(file)
    # Write header row (optional)
    header = ["Name", "Data Url", "Reynold's Number", "Alpha", "CL", "CD"]
    writer.writerow(header)

    writer.writerows(filtered_list)