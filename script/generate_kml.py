import csv
from xml.dom.minidom import Document

INPUT_CSV = '../mission/mission_1.csv'
OUTPUT_KML = '../mission/mission_1.kml'

# read the data of CSV
with open(INPUT_CSV, mode='r') as file:
    reader = csv.DictReader(file)
    waypoints = list(reader)

# Check if there are points
if not waypoints:
    print(" Aucune donnée dans le CSV.")
    exit()

# Création du document KML
doc = Document()
kml = doc.createElement("kml")
kml.setAttribute("xmlns", "http://www.opengis.net/kml/2.2")
doc.appendChild(kml)

document = doc.createElement("Document")
kml.appendChild(document)

# Ajouter les waypoints
for wp in waypoints:
    placemark = doc.createElement("Placemark")
    point = doc.createElement("Point")
    coordinates = doc.createElement("coordinates")
    coord_text = f"{wp['longitude']},{wp['latitude']},{wp['altitude(m)']}"
    coordinates.appendChild(doc.createTextNode(coord_text))
    point.appendChild(coordinates)
    placemark.appendChild(point)
    document.appendChild(placemark)

# Sauvegarde du fichier KML
with open(OUTPUT_KML, "w", encoding="utf-8") as f:
    f.write(doc.toprettyxml(indent="  "))

print(f" Fichier KML généré avec {len(waypoints)} points : {OUTPUT_KML}")
