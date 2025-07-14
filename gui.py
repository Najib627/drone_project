import tkinter as tk 
from tkinter import filedialog, messagebox
from kml_generator import generate_kml_from_csv
import os
import platform
import subprocess

root = tk.Tk()
root.title("Drone Mission Generator")
root.geometry("500x500")
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





def ouvrir_kml(path):
    # Obtenir le chemin absolu et convertir pour Windows si besoin
    abs_path = os.path.abspath(path)

    if platform.system() == "Linux" and "microsoft" in platform.release().lower():
        # On est sous WSL, on convertit le chemin pour Windows
        try:
            result = subprocess.run(['wslpath', '-w', abs_path], capture_output=True, text=True)
            windows_path = result.stdout.strip()
            subprocess.run(['powershell.exe', f'Start-Process "{windows_path}"'])
        except Exception as e:
            print("Erreur lors de l'ouverture du fichier KML :", e)
    else:
        # Sur Windows natif ou Linux standard
        try:
            import webbrowser
            webbrowser.open(f'file://{abs_path}')
        except Exception as e:
            print("Erreur d'ouverture avec webbrowser :", e)



# GUI layout
tk.Label(root, text="1. Select CSV File").pack(pady=10)
tk.Button(root, text="Browse CSV", command=select_csv).pack()
tk.Label(root, textvariable=csv_path, wraplength=400).pack(pady=5)

tk.Label(root, text="2. Altitude (m)").pack(pady=10)
tk.Scale(root, from_=10, to=150, orient="horizontal", variable=altitude).pack()

tk.Label(root, text="3. Camera Pitch (°)").pack(pady=10)
tk.Scale(root, from_=-90, to=0, orient="horizontal", variable=pitch).pack()

tk.Label(root, text="4. Output Format").pack(pady=10)
tk.Radiobutton(root, text="KML", variable=file_format, value="kml").pack()
tk.Radiobutton(root, text="KMZ", variable=file_format, value="kmz").pack()

tk.Button(root, text="Generate Mission File", command=generate, bg="green", fg="white").pack(pady=10)
#tk.Button(root, text="Afficher Waypoints sur la carte", command=lancer_affichage).pack(pady=10)
tk.Button(root, text="Open KML in Google Earth", command=ouvrir_kml).pack(pady=10)

root.mainloop()
