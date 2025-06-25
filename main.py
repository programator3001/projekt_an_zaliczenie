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

class PunktSzczepien:
    def __init__(self, nazwa, ulica, miejscowosc, nr_budynku):
        self.nazwa = nazwa
        self.ulica = ulica
        self.miejscowosc = miejscowosc
        self.nr_budynku = nr_budynku
        self.coordinates = self.get_coordinates()
        self.marker = map_widget.set_marker(
            self.coordinates[0], self.coordinates[1],
            text=self.nazwa
        )

    def get_coordinates(self):
        geolocator = Nominatim(user_agent="mapbook_ak")
        address = f"{self.ulica} {self.nr_budynku}, {self.miejscowosc}, Polska"
        location = geolocator.geocode(address)
        if location:
            return [location.latitude, location.longitude]
        else:
            return [52.23, 21.01]  # Warszawa fallback

# Funkcje CRUD dla punktów szczepień
def dodaj_punkt_szczepien():
    nazwa = entry_nazwa.get()
    ulica = entry_ulica.get()
    miejscowosc = entry_miejscowosc.get()
    nr = entry_nr_budynku.get()

    punkt = PunktSzczepien(nazwa, ulica, miejscowosc, nr)
    punkty_szczepien_list.append(punkt)
    pokaz_liste_punktow_szczepien()

def pokaz_liste_punktow_szczepien():
    listbox_punkty_szczepien.delete(0, END)
    for i, punkt in enumerate(punkty_szczepien_list):
        listbox_punkty_szczepien.insert(i, f"{i + 1}. {punkt.nazwa}, {punkt.ulica}")

# Dodaj te funkcje do GUI
Button(ramka_lista, text="Dodaj punkt", command=dodaj_punkt_szczepien).grid(row=2, column=0)

class Pracownik:
    def __init__(self, imie, nazwisko, ulica, miejscowosc, nr_budynku):
        self.imie = imie
        self.nazwisko = nazwisko
        self.ulica = ulica
        self.miejscowosc = miejscowosc
        self.nr_budynku = nr_budynku
        self.coordinates = self.get_coordinates()

    def get_coordinates(self):
        geolocator = Nominatim(user_agent="mapbook_ak")
        address = f"{self.ulica} {self.nr_budynku}, {self.miejscowosc}, Polska"
        location = geolocator.geocode(address)
        if location:
            return [location.latitude, location.longitude]
        else:
            return [52.23, 21.01]

class Pacjent:
    def __init__(self, imie, nazwisko, ulica, miejscowosc, nr_budynku):
        self.imie = imie
        self.nazwisko = nazwisko
        self.ulica = ulica
        self.miejscowosc = miejscowosc
        self.nr_budynku = nr_budynku
        self.coordinates = self.get_coordinates()

    def get_coordinates(self):
        geolocator = Nominatim(user_agent="mapbook_ak")
        address = f"{self.ulica} {self.nr_budynku}, {self.miejscowosc}, Polska"
        location = geolocator.geocode(address)
        if location:
            return [location.latitude, location.longitude]
        else:
            return [52.23, 21.01]

        def open_pracownicy_window(punkt_szczepien):
            # Okno do zarządzania pracownikami
            pass

        def open_pacjenci_window(punkt_szczepien):
            # Okno do zarządzania pacjentami
            pass

        # Dodaj przyciski do GUI
        Button(ramka_lista, text="Pracownicy", command=lambda: open_pracownicy_window(active_punkt_szczepien)).grid(
            row=3, column=0)
        Button(ramka_lista, text="Pacjenci", command=lambda: open_pacjenci_window(active_punkt_szczepien)).grid(row=3,
                                                                                                                column=1)
def show_worker_locations(self):
    # Wyświetlanie markerów pracowników na mapie
    pass

def show_patient_locations(self):
    # Wyświetlanie markerów pacjentów na mapie
    pass

# Rozszerzenie klasy PunktSzczepien o nowe metody
root.mainloop()