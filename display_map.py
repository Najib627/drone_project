import pandas as pd
import folium
import webbrowser
import os
import platform

def afficher_carte(csv_path):
    try:
        df = pd.read_csv(csv_path)

        # Création d'une carte centrée sur le 1er point
        map_center = [df.iloc[0]["Latitude"], df.iloc[0]["Longitude"]]
        m = folium.Map(location=map_center, zoom_start=17)

        # Ajouter les points
        for _, row in df.iterrows():
            folium.Marker(
                location=[row["Latitude"], row["Longitude"]],
                popup=f"Alt: {row['Altitude']}m",
                icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(m)

        m.save("map.html")

        # Ouverture compatible WSL
        if platform.system() == "Linux" and "microsoft" in platform.release().lower():
            os.system("explorer.exe map.html")
        else:
            webbrowser.open("map.html")

    except Exception as e:
        print(f"Erreur lors de l'affichage de la carte : {e}")
