#Define target airplane Weight (in pounds)
import math

W = 6600
density = 0.002378
WingArea = 160.0
CL = 0.4
CD = 0.0388
CoefFrictRoll = 0.02
Thrust = 1200
g=32.17
CLMax = 1.6 #The maximum CL for an airfoil based on data on airfoil tools (Stall CL)

Vstall = math.sqrt((2*W)/(density*WingArea*CLMax))
Vstall = 140.4
print("Vstall (ft/s)- ",Vstall)

VLo = 1.2*Vstall
print("Vliftoff (ft/s)- ",VLo)

L = 0.5*density*((.7*VLo)**2)*WingArea*CL

D = 0.5*density*((.7*VLo)**2)*WingArea*CD

#Average Resistive Force on Airplane (measured at .7*VLo)
Rav = (D+CoefFrictRoll*(W-L))

sLo = (1.44*(W**2))/(g*density*WingArea*CLMax*(Thrust-Rav))
print("Liftoff Distance (ft)- ",sLo)

