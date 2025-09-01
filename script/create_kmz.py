import zipfile
import os

# Paramètres
kml_file = '../mission/mission_1.kml'
kmz_file = '../mission/mission_1.kmz'

# Vérifier si le fichier .kml existe
if not os.path.exists(kml_file):
    print(f" Fichier KML introuvable : {kml_file}")
else:
    # create the kmz file (zip into .kmz)
    with zipfile.ZipFile(kmz_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(kml_file, arcname="doc.kml")  # DJI are waiting for a file named 'doc.kml'

    print(f" KMZ file generated: {kmz_file}")
