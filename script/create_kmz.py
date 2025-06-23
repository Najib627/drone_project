import zipfile
import os

# Paramètres
kml_file = "./mission/mission_1.kml"
kmz_file = "./mission/mission_1.kmz"

# Vérifier si le fichier .kml existe
if not os.path.exists(kml_file):
    print(f" Fichier KML introuvable : {kml_file}")
else:
    # Créer le fichier .kmz (zip renvoyé .kmz)
    with zipfile.ZipFile(kmz_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(kml_file, arcname="doc.kml")  # DJI attend un fichier nommé doc.kml

    print(f" Fichier KMZ généré : {kmz_file}")
