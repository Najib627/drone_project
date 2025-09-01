import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
from matplotlib.patches import Polygon
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
#second method 
# --- FUNCTIONS ---

def load_mission_csv(file_path):
    df = pd.read_csv(file_path, skip_blank_lines=True)
    df.columns = df.columns.str.strip().str.lower()
    print("Detected columns:", df.columns.tolist())

    if "longitude" in df.columns and "latitude" in df.columns:
        waypoints = list(zip(df["longitude"], df["latitude"]))
    elif "x" in df.columns and "y" in df.columns:
        waypoints = list(zip(df["x"], df["y"]))
    else:
        raise ValueError(f"Columns not recognized in the CSV file: {df.columns.tolist()}")

    return waypoints

def calculate_total_distance(start, waypoints):
    total_distance = 0
    current_position = start
    for waypoint in waypoints:
        distance = np.linalg.norm(np.array(waypoint) - np.array(current_position))
        total_distance += distance
        current_position = waypoint
    total_distance += np.linalg.norm(np.array(current_position) - np.array(start))
    return total_distance

def find_nearest_waypoint(waypoints, drone_position=(0, 0)):
    distances = [np.linalg.norm(np.array(wp) - np.array(drone_position)) for wp in waypoints]
    min_index = np.argmin(distances)
    return min_index

def point_in_danger_zone(point, danger_zones):
    for zone in danger_zones:
        path = Path(zone)
        if path.contains_point(point):
            return True
    return False

# --- USER INPUT ---

# Request CSV filename from user
csv_filename = input("Enter the name of the mission CSV file (e.g., mission.csv): ")
csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Data", csv_filename))

# Request drone starting position
x0 = float(input("Enter the drone's starting X (or longitude): "))
y0 = float(input("Enter the drone's starting Y (or latitude): "))
drone_position = (x0, y0)

# Request danger zones
danger_zones = []
n_zones = int(input("How many danger zones do you want to enter? "))

for i in range(n_zones):
    print(f"Enter the coordinates for danger zone {i+1} as a list of tuples (e.g. [(x1,y1), (x2,y2), ...]):")
    zone_input = input()
    try:
        zone = eval(zone_input)
        danger_zones.append(zone)
    except:
        print("Invalid format. Skipping this zone.")

# --- MAIN EXECUTION ---

# Load waypoints
waypoints = load_mission_csv(csv_path)

# Estimate battery
battery_per_100m = 1.0
battery_estimate = calculate_total_distance(waypoints[0], waypoints) / 100 * battery_per_100m

# Find closest waypoint to drone
optimal_index = find_nearest_waypoint(waypoints, drone_position=drone_position)
waypoints = waypoints[optimal_index:] + waypoints[:optimal_index]

# Identify waypoints inside danger zones
dangerous_points = [pt for pt in waypoints if point_in_danger_zone(pt, danger_zones)]

# Plot
x, y = zip(*waypoints)
fig, ax = plt.subplots(figsize=(7, 7))
ax.plot(x, y, marker='o', linestyle='-', color='blue', label="Trajet CSV")
ax.scatter(x[0], y[0], color='purple', s=100, marker='s', label="Optimal Start")

# Draw danger zones
for zone in danger_zones:
    polygon = Polygon(zone, closed=True, color='red', alpha=0.3, label="Danger Zone")
    ax.add_patch(polygon)

# Highlight dangerous waypoints
for (xp, yp) in dangerous_points:
    ax.plot(xp, yp, 'rx', markersize=8, label="Waypoint in Danger Zone")

ax.set_title("Optimized Drone Mission with User-Defined Danger Zones")
ax.set_xlabel("Longitude" if abs(x[0]) > 100 else "X")
ax.set_ylabel("Latitude" if abs(y[0]) > 100 else "Y")
ax.grid(True)
ax.legend(loc="upper right")
plt.tight_layout()
plt.show()

# Logs
print(f"Total distance (including return): {calculate_total_distance(waypoints[0], waypoints):.2f} units")
print(f"Estimated battery needed: {battery_estimate:.2f}%")
print("Dangerous waypoints:")

import ace_tools as tools
tools.display_dataframe_to_user(name="Waypoints in Danger Zones", dataframe=pd.DataFrame(dangerous_points, columns=["X", "Y"]))
