Drone Flight Plan Generator – README
------------------------------------

 Project Goal:
Automatically generate DJI-compatible flight plans (.kmz files) from a list of waypoints.

 Solves the DJI Fly limitation of 200 waypoints per mission.

 Requirements:
- Python 3.x
- Libraries: pandas, xml.dom.minidom, zipfile

Folder Structure:
- /data/            → Contains the initial waypoints.csv file
- /missions/        → Stores mission_1.csv, mission_1.kml, mission_1.kmz, etc.
- /scripts/         → Python scripts to generate each step
- build_all.py      → One-click script that performs all steps

Usage Steps:

1. Place your input file as: /data/waypoints.csv
   Format: Index, Latitude, Longitude, Altitude

2. Run the main script:
   python3 build_all.py

3. The script will:
   - Split the CSV into sub-missions of 200 points max
   - Generate .kml files for each mission
   - Convert .kml files into .kmz format for DJI Fly

4. Import into DJI Fly:
   - Create a dummy mission on your device
   - Replace the generated .kmz file in the DJI Fly mission folder
   - Reopen DJI Fly to load the mission

 Notes:
- Max 200 waypoints per .kmz due to DJI Fly limitations
- Make sure to name the internal .kml file as doc.kml
- Use third-party file managers if Android blocks access to DJI folders

