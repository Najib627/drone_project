import csv
import simplekml
import os

def generate_kml_from_csv(csv_file, altitude, pitch, file_format):
    # Crée le KML
    kml = simplekml.Kml()

    with open(csv_file, 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            lat = float(row['latitude'])
            lon = float(row['longitude'])
            alt = float(row.get('altitude', altitude))  # Priorité à l'altitude du fichier, sinon valeur par défaut

            pnt = kml.newpoint(coords=[(lon, lat, alt)])
            pnt.altitudemode = simplekml.AltitudeMode.absolute
            pnt.cameraaltitude = alt
            pnt.style.iconstyle.heading = 0
            pnt.style.iconstyle.color = 'ff0000ff'  # rouge
            pnt.style.iconstyle.scale = 1
            pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png'
            pnt.extendeddata.newdata(name='Pitch', value=str(pitch))

    # Crée le dossier de sortie s’il n'existe pas
    os.makedirs("output", exist_ok=True)

    # Détermine le nom de sortie
    base_name = os.path.splitext(os.path.basename(csv_file))[0]
    out_file = f"output/{base_name}.{file_format}"

    if file_format == "kml":
        kml.save(out_file)
    elif file_format == "kmz":
        kml.savekmz(out_file)
    else:
        raise ValueError("Unsupported format: choose 'kml' or 'kmz'")

    print(f" Fichier généré : {out_file}")
