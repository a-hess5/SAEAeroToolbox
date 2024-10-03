# Initial Velocity (ft/s)
initVelocity = 0  # in feet per second (ft/s)

# Initial Position (ft)
initPosition = 0  # in feet (ft)

# Position Step (ft)
positionStep = 0.01  # step size in feet (ft)

# Distance until takeoff (ft)
takeoffDistance = 90 # in feet (ft)

# Thrust (lb)
thrustLbs = 10  # in pounds (lb)

# New Section
# Run over position, stepping by positionStep
# Run until the takeoff time

position = initPosition
velocity = initVelocity

while (position<=takeoffDistance):
    velocity = velocity