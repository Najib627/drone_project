import csv
import os
from math import ceil

# Chemins
INPUT_FILE = '../data/waypoint.csv'
OUTPUT_FOLDER = '../mission'
MAX_POINTS = 200

# Créer le dossier missions/ s'il n'existe pas
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Lire tous les waypoints
with open(INPUT_FILE, mode='r') as file:
    reader = csv.DictReader(file)
    waypoints = list(reader)

# Calcul du nombre de missions nécessaires
total_missions = ceil(len(waypoints) / MAX_POINTS)
print(f" Total waypoints : {len(waypoints)} → {total_missions} mission(s)")

# Découper en sous-fichiers
for i in range(total_missions):
    start = i * MAX_POINTS
    end = start + MAX_POINTS
    chunk = waypoints[start:end]

    output_file = os.path.join(OUTPUT_FOLDER, f"mission_{i+1}.csv")
    with open(output_file, mode='w', newline='') as out_file:
        writer = csv.DictWriter(out_file, fieldnames=['Index', 'Latitude', 'Longitude', 'Altitude'])
        writer.writeheader()
        writer.writerows(chunk)

    print(f" Fichier généré : {output_file}")
