from tkinter import *
import tkintermapview
from geopy.geocoders import Nominatim

# --- GUI ---
root = Tk()
root.geometry("1200x900")
root.title("System Zarządzania Punktami Szczepień")

# Ramki aplikacji
ramka_lista = Frame(root)
ramka_formularz = Frame(root)
ramka_szczegoly = Frame(root)
ramka_mapa = Frame(root)

ramka_lista.grid(row=0, column=0)
ramka_formularz.grid(row=0, column=1)
ramka_szczegoly.grid(row=1, column=0, columnspan=2)
ramka_mapa.grid(row=2, column=0, columnspan=2)

# Podstawowe elementy interfejsu
Label(ramka_lista, text="LISTA PUNKTÓW SZCZEPIEŃ").grid(row=0, column=0, columnspan=3)
listbox_punkty_szczepien = Listbox(ramka_lista, width=60, height=15)
listbox_punkty_szczepien.grid(row=1, column=0, columnspan=3)

# Mapa
map_widget = tkintermapview.TkinterMapView(ramka_mapa, width=1200, height=600, corner_radius=5)
map_widget.set_position(52.23, 21.0)
map_widget.set_zoom(6)
map_widget.grid(row=0, column=0, columnspan=3)

root.mainloop()