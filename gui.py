import tkinter as tk
from tkinter import filedialog, messagebox
from kml_generator import generate_kml_from_csv  # fonction qu’on écrira ensuite
from display_map import afficher_carte
import webbrowser
import os
import platform

# ouverture compatible Windows & WSL
if platform.system() == "Linux" and "microsoft" in platform.release().lower():
    os.system("explorer.exe map.html")
else:
    webbrowser.open("map.html")

root = tk.Tk()
root.title("Drone Mission Generator")
root.geometry("500x400")
root.resizable(False, False)

csv_path = tk.StringVar()
altitude = tk.IntVar(value=50)
pitch = tk.IntVar(value=-90)
file_format = tk.StringVar(value="kml")

def select_csv():
    path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if path:
        csv_path.set(path)

def generate():
    if not csv_path.get():
        messagebox.showerror("Error", "Please select a CSV file.")
        return
    generate_kml_from_csv(csv_path.get(), altitude.get(), pitch.get(), file_format.get())
    messagebox.showinfo("Success", "Mission file generated successfully.")


def lancer_affichage():
    afficher_carte('mission/mission_1.csv')
    path=os.path.abspath('mission/mission_1.csv') # Bouton de sélection de fichier
    print(path)

tk.Label(root, text="1. Select CSV File").pack(pady=10)
tk.Button(root, text="Browse CSV", command=select_csv).pack()
tk.Label(root, textvariable=csv_path, wraplength=400).pack(pady=5)

# Altitude
tk.Label(root, text="2. Altitude (m)").pack(pady=10)
tk.Scale(root, from_=10, to=150, orient="horizontal", variable=altitude).pack()

# Pitch
tk.Label(root, text="3. Camera Pitch (°)").pack(pady=10)
tk.Scale(root, from_=-90, to=0, orient="horizontal", variable=pitch).pack()

# Format
tk.Label(root, text="4. Output Format").pack(pady=10)
tk.Radiobutton(root, text="KML", variable=file_format, value="kml").pack()
tk.Radiobutton(root, text="KMZ", variable=file_format, value="kmz").pack()

# Bouton Générer
tk.Button(root, text="Generate Mission File", command=generate, bg="green", fg="white").pack(pady=20)
tk.Button(root, text="Afficher Waypoints sur la carte", command=lancer_affichage).pack(pady=20)

root.mainloop()
