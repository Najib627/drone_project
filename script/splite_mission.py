import csv
import os
from math import ceil, radians, sin, cos, sqrt, atan2

# Chemins
INPUT_FILE = '../data/waypoints_detailed.csv'
OUTPUT_FOLDER = '../mission'
DRONE_SPEED = 5  # m/s
FLIGHT_TIME_MAX = 25  # minutes

# Fonction de distance Haversine
def distance_haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # rayon de la Terre en mètres
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

# Créer le dossier missions/ s'il n'existe pas
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Lire tous les waypoints
with open(INPUT_FILE, mode='r') as file:
    reader = csv.DictReader(file)
    waypoints = list(reader)

# Calcul du nombre de missions équilibrées
MAX_POINTS = 50# waypoints est 450
total_missions = ceil(len(waypoints) / MAX_POINTS)#3
points_per_mission = ceil(len(waypoints) / total_missions)#150

print(f"Total waypoints : {len(waypoints)} → {total_missions} mission(s), {points_per_mission} points/mission")

# Découper en sous-fichiers équilibrés
for i in range(total_missions):
    start = i * points_per_mission
    end = min(start + points_per_mission, len(waypoints))
    chunk = waypoints[start:end]

    # Calcul de distance
    distance = 0
    for j in range(1, len(chunk)):
        lat1, lon1 = float(chunk[j-1]['latitude']), float(chunk[j-1]['longitude'])
        lat2, lon2 = float(chunk[j]['latitude']), float(chunk[j]['longitude'])
        distance += distance_haversine(lat1, lon1, lat2, lon2)

    duration_minutes = round(distance / DRONE_SPEED / 60, 1)
    battery_percent = round((duration_minutes / FLIGHT_TIME_MAX) * 100, 1)

    print(f"Mission {i+1} → Distance: {round(distance, 2)} m | Temps estimé: {duration_minutes} min | Batterie estimée: {battery_percent}%")

    # Sauvegarder mission CSV
    output_file = os.path.join(OUTPUT_FOLDER, f"mission_{i+1}.csv")
    with open(output_file, mode='w', newline='') as out_file:
        writer = csv.DictWriter(out_file, fieldnames=chunk[0].keys())
        writer.writeheader()
        writer.writerows(chunk)

    print(f"Fichier généré : {output_file}")
