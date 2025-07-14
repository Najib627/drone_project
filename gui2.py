import tkinter as tk
from tkinter import filedialog, messagebox
import os
import platform
import webbrowser

# Création de la fenêtre principale
root = tk.Tk()
root.title("Map-Creator Settings")
root.geometry("400x600")
root.resizable(False, False)

# Variables
alt_inception = tk.DoubleVar(value=3.0)
alt_wp1 = tk.DoubleVar(value=5.0)
alt_wp2 = tk.DoubleVar(value=5.0)
pitch = tk.IntVar(value=-90)
focal_length = tk.StringVar(value="35mm")
kmz_format = tk.StringVar(value="Google KML")
triangulate = tk.BooleanVar()
security = tk.BooleanVar(value=True)
drag_2d = tk.BooleanVar()
api_key = tk.StringVar()

# Fonctions
def generate_mission():
    msg = f"Mission Parameters:\n"
    msg += f"Start Altitude: {alt_inception.get()} m\n"
    msg += f"Waypoint 1 Altitude: {alt_wp1.get()} m\n"
    msg += f"Waypoint 2 Altitude: {alt_wp2.get()} m\n"
    msg += f"Pitch: {pitch.get()}\u00b0\n"
    msg += f"Format: {kmz_format.get()}\n"
    msg += f"Focal Length: {focal_length.get()}\n"
    msg += f"Triangulate: {'Yes' if triangulate.get() else 'No'}\n"
    msg += f"Security: {'Enabled' if security.get() else 'Disabled'}\n"
    msg += f"2D Drag All: {'Enabled' if drag_2d.get() else 'Disabled'}\n"
    msg += f"API Key: {api_key.get()}"
    messagebox.showinfo("Mission Settings", msg)

# Widgets
tk.Label(root, text="Inception start altitude [m]").pack(pady=5)
tk.Scale(root, from_=0, to=100, resolution=0.1, orient="horizontal", variable=alt_inception).pack()

tk.Label(root, text="Vertical mission waypoint 1 altitude [m]").pack(pady=5)
tk.Scale(root, from_=0, to=100, resolution=0.1, orient="horizontal", variable=alt_wp1).pack()

tk.Label(root, text="Vertical mission waypoint 2 altitude [m]").pack(pady=5)
tk.Scale(root, from_=0, to=100, resolution=0.1, orient="horizontal", variable=alt_wp2).pack()

# Format boutons
frame_format = tk.Frame(root)
frame_format.pack(pady=10)
tk.Label(frame_format, text="KML / KMZ").pack()
tk.Radiobutton(frame_format, text="Google KML", variable=kmz_format, value="Google KML").pack()
tk.Radiobutton(frame_format, text="Pilot 2 KMZ", variable=kmz_format, value="Pilot 2 KMZ").pack()
tk.Radiobutton(frame_format, text="DJI Fly KMZ", variable=kmz_format, value="DJI Fly KMZ").pack()

# Pitch
frame_pitch = tk.Frame(root)
frame_pitch.pack(pady=10)
tk.Label(frame_pitch, text="Camera pitch grid [°]").pack()
tk.Scale(frame_pitch, from_=-90, to=0, orient="horizontal", variable=pitch).pack()

# Focal length
frame_focal = tk.Frame(root)
frame_focal.pack(pady=10)
tk.Label(frame_focal, text="35mm equivalent focal length").pack()
tk.Radiobutton(frame_focal, text="20mm", variable=focal_length, value="20mm").pack()
tk.Radiobutton(frame_focal, text="24mm", variable=focal_length, value="24mm").pack()
tk.Radiobutton(frame_focal, text="28mm", variable=focal_length, value="28mm").pack()
tk.Radiobutton(frame_focal, text="35mm", variable=focal_length, value="35mm").pack()

# Options
tk.Checkbutton(root, text="Triangulate", variable=triangulate).pack(pady=2)
tk.Checkbutton(root, text="Security", variable=security).pack(pady=2)
tk.Checkbutton(root, text="2D drag all", variable=drag_2d).pack(pady=2)

# API key
tk.Label(root, text="GPXZ high-resolution API key:").pack(pady=5)
tk.Entry(root, textvariable=api_key).pack()

# Bouton Generate
tk.Button(root, text="Generate Mission File", command=generate_mission, bg="green", fg="white").pack(pady=20)

root.mainloop()
