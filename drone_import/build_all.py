import csv
import os
from math import ceil

# Chemins d'entrée/sortie
INPUT_FILE = "./Data/waypoint.csv"
MISSIONS_FOLDER = "./missions"
MAX_POINTS = 200

# Créer le dossier missions/ s'il n'existe pas
os.makedirs(MISSIONS_FOLDER, exist_ok=True)

# Lire les waypoints
with open(INPUT_FILE, mode='r') as file:
    reader = csv.DictReader(file)
    waypoints = list(reader)

# Calcul du nombre de missions
total_missions = ceil(len(waypoints) / MAX_POINTS)
print(f" Total waypoints: {len(waypoints)} → {total_missions} mission(s)")

# Découper les points en mission_X.csv
for i in range(total_missions):
    start = i * MAX_POINTS
    end = start + MAX_POINTS
    chunk = waypoints[start:end]

    mission_file = os.path.join(MISSIONS_FOLDER, f"mission_{i+1}.csv")
    with open(mission_file, mode='w', newline='') as out_file:
        writer = csv.DictWriter(out_file, fieldnames=['Index', 'Latitude', 'Longitude', 'Altitude'])
        writer.writeheader()
        writer.writerows(chunk)

    print(f" Mission {i+1} enregistrée : {mission_file}")
