import numpy as np
import matplotlib.pyplot as plt

F = 1000 # Newton'ów
m = 1000 # kg
airResistance = 0.25
A = 2 # m^2
airDensity = 1.225 # kg/m^-3
g = 9.81 # m/s^2
totalTime = 100 # s
dt = 0.001 # s

road = [
    (0, 100, 0),
    (100, 200, 2),
    (200, 300, -1),
    (300, 400, 1),
    (400, 500, 3),
    (500, 600, -2),
    (600, 700, 1),
    (700, 800, 2),
    (800, 900, 1),
    (900, 1000, -1),
]

def getAlpha(position):
    for start, end, incline in road:
        if start <= position < end:
            alpha = np.arctan(incline / 100)
            return alpha
    return 0
        
def accelaration(position, velocity, engineOn):
    alpha = getAlpha(position)

    if engineOn:
        Force = F
    else:
        Force = 0

    a = (Force - airResistance*airDensity*A*velocity**2 - m*g* np.sin(alpha) ) / m

    return a

def drive(engineTime):
    times = np.arange(0, totalTime, dt)
    positions = []
    velocities = []

    position = 0
    velocity = 0

    for i in times:
        if i <= engineTime:
            engineOn = True
        else:
            engineOn = False
    
        a = accelaration(position, velocity, engineOn)
        velocity += a * dt
        position += velocity * dt

        velocities.append(velocity)
        positions.append(position)
    
    return times, positions, velocities

def findOptimalEngineTime():
    low = 0
    high = totalTime
    targetDistance = 1000
    marginError = 0.1

    while high - low > 0.001:
        mid = (low + high) / 2
        _, positions, _ = drive(mid)
        finalPos = positions[-1]

        if finalPos < targetDistance - marginError:
            low = mid
        elif finalPos > targetDistance + marginError:
            high = mid
        else:
            return mid
    
    return (low + high) / 2

optimalEngineTime = findOptimalEngineTime()

print(optimalEngineTime)

times, positions, velocities = drive(optimalEngineTime)

plt.figure(figsize=(12,5))

plt.subplot(1,2,1)
plt.plot(times, positions)
plt.title("Położenie [m]")
plt.xlabel("Czas [s]")
plt.ylabel("Położenie [m]")

plt.subplot(1,2,2)
plt.plot(times, velocities)
plt.title("Prędkość [m/s]")
plt.xlabel("Czas [s]")
plt.ylabel("Prędkość [m/s]")

plt.tight_layout()
plt.show()