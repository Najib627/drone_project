import pandas as pd
from fastkml import kml
from shapely.geometry import Polygon
from shapely.geometry import Point
import matplotlib.pyplot as plt
import os

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


def load_danger_zones_from_kml(kml_file):
    with open(kml_file, 'rt', encoding='utf-8') as f:
        doc = f.read()

    k = kml.KML()
    k.from_string(doc.encode('utf-8'))

    danger_zones = []

    for feature in k.features:
        for placemark in feature.features():
            geom = placemark.geometry
            if isinstance(geom, Polygon):
                coords = list(geom.exterior.coords)
                danger_zones.append(Polygon(coords))  # Store as shapely Polygon

    print(f"{len(danger_zones)} danger zone(s) loaded from {kml_file}")
    return danger_zones




def detect_waypoints_in_danger(waypoints, danger_zones):
    in_danger = []
    safe = []

    for wp in waypoints:
        point = Point(wp)
        if any(zone.contains(point) for zone in danger_zones):
            in_danger.append(wp)
        else:
            safe.append(wp)

    print(f"{len(in_danger)} waypoint(s) in danger zones detected.")
    return safe, in_danger





def plot_mission(waypoints_safe, waypoints_danger, danger_zones, start_point=None):
    plt.figure(figsize=(8, 8))
    
    # --- Trajet sûr ---
    if waypoints_safe:
        x_safe, y_safe = zip(*waypoints_safe)
        plt.plot(x_safe, y_safe, 'o-', color='blue', label="Safe Waypoints")
    
    # --- Points dangereux ---
    if waypoints_danger:
        x_danger, y_danger = zip(*waypoints_danger)
        plt.scatter(x_danger, y_danger, c='red', marker='x', label="Danger Points")

    # --- Zones interdites ---
    for poly in danger_zones:
        x, y = poly.exterior.xy
        plt.fill(x, y, color='red', alpha=0.3, label="Danger Zone")

    # --- Point de départ ---
    if start_point:
        plt.scatter(start_point[0], start_point[1], c='purple', s=100, marker='s', label="Start Point")

    plt.title("Drone Mission with Danger Zones")
    plt.xlabel("X" if abs(x_safe[0]) < 100 else "Longitude")
    plt.ylabel("Y" if abs(y_safe[0]) < 100 else "Latitude")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # === Chemins d'accès ===
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Data", "waypoints_detailed.csv"))
    kml_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Data", "danger_zone.kml"))

    # === Chargement des données ===
    waypoints = load_mission_csv(csv_path)
    danger_zones = load_danger_zones_from_kml(kml_path)

    # === Détection des points dangereux ===
    safe_points, danger_points = detect_waypoints_in_danger(waypoints, danger_zones)

    # === Affichage graphique ===
    start = safe_points[0] if safe_points else None
    plot_mission(safe_points, danger_points, danger_zones, start_point=start)
