# Takes in an airfoil data sheet made by AirfoilScrape.py
# Calculates the needed takeoff velocity and wing area at a provided takeoff distance and weight
# Outputs all possible combos within range

import csv
import math


#Define file path of CSV with airfoil data
csv_file_path = 'foil_data_new.csv'

#Open CSV File with Scraped Airfoil data. Save data to list named Data
try:
    with open(csv_file_path, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        data = []  # List to store the CSV data
        for row in csv_reader:
            data.append(row)
except FileNotFoundError:
    print("File not found.")
except Exception as e:
    print(f"An error occurred: {e}")

#Function to calculate the velocity given wing area and airplane/airfoil details
#Based on equations from https://eaglepubs.erau.edu/introductiontoaerospaceflightvehicles/chapter/takeoff-landing-performance/
#Params- W (Total Takeoff Weight), density (Density of air), CLMax (Maximum CL of the airfoil overall), WingArea
def NeededTakeoffVelocity(W, density, CLMax, WingArea):
    Vstall = math.sqrt((2 * W) / (density * WingArea * CLMax))
    #Convert the stall velocity to the needed V for takeoff
    VLo = 1.2 * Vstall
    return  VLo

#Function to calculate the lift given wing area and airplane/airfoil details
#Based on equations from https://eaglepubs.erau.edu/introductiontoaerospaceflightvehicles/chapter/takeoff-landing-performance/
#Params- density (Density of air), CL (CL at selected alpha), WingArea, VLo (Liftoff Velocity)
def TakeoffLift(density, CL, WingArea, VLo):
    L = 0.5 * density * ((.7 * VLo) ** 2) * WingArea * CL
    return L

#Function to calculate the drag given wing area and airplane/airfoil details
#Based on equations from https://eaglepubs.erau.edu/introductiontoaerospaceflightvehicles/chapter/takeoff-landing-performance/
#Params- density (Density of air), CD (CD at selected alpha), WingArea, VLo (Liftoff Velocity)
def TakeoffDrag(density, CD, WingArea, VLo):
    D = 0.5 * density * ((.7 * VLo) ** 2) * WingArea * CD
    return D

#Function to calculate the Average Resistive Force on the airplane given wing area and airplane/airfoil details
#Based on equations from https://eaglepubs.erau.edu/introductiontoaerospaceflightvehicles/chapter/takeoff-landing-performance/
#Params- Drag, CoefFrictRoll (The rolling coef. of friction), Weight of airplane, Lift Produced by Airplane
def TakeoffResistiveForce(Drag, CoefFrictRoll, W, Lift):
    Rav = (Drag + CoefFrictRoll * (W - Lift))
    return Rav

def TakeoffDistance(W, g, density, WingArea, CLMax, Thrust, Rav):
    sLo = (1.44 * (W ** 2)) / (g * density * WingArea * CLMax * (Thrust - Rav))
    return sLo

def ThrustForDistance(W, g, density, WingArea, CLMax, Distance, Rav):
    T = (1.44 * (W ** 2))/(Distance * g * density * WingArea * CLMax)+Rav
    return T



file_path = "foil_takeoff_calc55lb80.csv"
with open(file_path, mode="w", newline="") as file:
    writer = csv.writer(file)
    # Write header row (optional)
    header = ["Airfoil", "CL", "CD", "CLMax", "Vlo", "Lift", "Drag", "Average Resistance", "WingArea", "ThrustNeeded"]
    writer.writerow(header)



#Define target airplane Weight (in pounds)
weight = 45
#Define Air Density (slugs*ft^-3)
AirDensity = 0.002378
g = 32.17
coefRollFrict = 0.02



#Pulls out an airfoil from the sheet data
for foil in range(1,len(data)):
    #CLMax is constant for an airfoil so it can be pulled before alphas are changed
    CLMax = float(data[foil][17])
    #Iterate through the alpha values and pull CL and CD for them
    for alpha in range(2, 3, 3):
        name = data[foil][0].split(',')[1]+"-"+data[0][alpha].split('-')[1]
        CL = float(data[foil][alpha])
        CD = float(data[foil][alpha+1])
        if CL>0 and CD>0:
            for WingArea in range(150, 435, 5):
                WingArea = WingArea / 10.0
                Vlo = NeededTakeoffVelocity(weight, AirDensity, CLMax, WingArea)
                Lift = TakeoffLift(AirDensity, CL, WingArea, Vlo)
                Drag = TakeoffDrag(AirDensity, CD, WingArea, Vlo)
                Rav = TakeoffResistiveForce(Drag, coefRollFrict, weight, Lift)
                ThrustNeeded = ThrustForDistance(weight, g, AirDensity, WingArea, CLMax, 80, Rav)
                if ThrustNeeded < 20.0:
                    # Write data to the CSV file
                    data_to_write = [name, CL, CD, CLMax, Vlo, Lift, Drag, Rav, WingArea, ThrustNeeded]
                    with open(file_path, mode="a", newline="") as file:
                        writer = csv.writer(file)
                        writer.writerow(data_to_write)
