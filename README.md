#  Drone Project – Mission Generator & Optimizer

This project is a Python-based toolkit for generating, optimizing, and visualizing drone missions using coordinate data. It supports the generation of KML/KMZ files compatible with DJI drones, with additional features like mission splitting, time estimation, and trajectory optimization.

---

##  Project Goals

- ✅ Convert CSV waypoints to KML/KMZ for DJI Fly
- ✅ Optimize mission start point to minimize distance and flight time
- ✅ Visualize mission paths (original vs optimized)
- ✅ Estimate drone flight duration
- ✅ (Optional) Parse and display danger zones (KML)
- ✅ Handle multiple missions
- ✅ GUI (in development)

---

python tache2/zone.py
This will:
  Load waypoints_detailed.csv
  Optimize the start point
  Compare distance & estimated time
  Show trajectory plots
  Display side-by-side waypoint orders

python script/generate_kml.py
python script/create_kmz.py
     You’ll find results in the output/ folder.

python script/splite_mission.py
     This will generate multiple missions (e.g. mission_1.csv) in the mission/ folder if your mission exceeds 200 waypoints
     
  
## Parameters
Drone speed assumed = 5 m/s
Distance = Euclidean (good for small/flat areas)
CSV format: required columns are:
longitude, latitude OR
x, y

##Author

Najib Mounsif
