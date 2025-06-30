from tkinter import Tk, Button
from display_map import afficher_carte

def lancer_affichage():
    afficher_carte('../mission/mission_1.csv')

root = Tk()
root.title("Drone Mission Planner")

Button(root, text="Afficher Waypoints sur la carte", command=lancer_affichage).pack(pady=20)

root.mainloop()
