from tkinter import *
import tkintermapview
from geopy.geocoders import Nominatim

punkty_szczepien_list = []
active_punkt_szczepien = None


class Pracownik:
    def __init__(self, imie, nazwisko, ulica, miejscowosc, nr_budynku):
        self.imie = imie
        self.nazwisko = nazwisko
        self.ulica = ulica
        self.miejscowosc = miejscowosc
        self.nr_budynku = nr_budynku
        self.coordinates = self.get_coordinates()
        self.marker = None

    def get_coordinates(self):
        geolocator = Nominatim(user_agent="mapbook_ak")
        address = f"{self.ulica} {self.nr_budynku}, {self.miejscowosc}, Polska"
        location = geolocator.geocode(address)
        if location:
            return [location.latitude, location.longitude]
        else:
            return [52.23, 21.01]  # Warszawa fallback


class Pacjent:
    def __init__(self, imie, nazwisko, ulica, miejscowosc, nr_budynku):
        self.imie = imie
        self.nazwisko = nazwisko
        self.ulica = ulica
        self.miejscowosc = miejscowosc
        self.nr_budynku = nr_budynku
        self.coordinates = self.get_coordinates()
        self.marker = None

    def get_coordinates(self):
        geolocator = Nominatim(user_agent="mapbook_ak")
        address = f"{self.ulica} {self.nr_budynku}, {self.miejscowosc}, Polska"
        location = geolocator.geocode(address)
        if location:
            return [location.latitude, location.longitude]
        else:
            return [52.23, 21.01]  # Warszawa fallback


class PunktSzczepien:
    def __init__(self, nazwa, ulica, miejscowosc, nr_budynku):
        self.nazwa = nazwa
        self.ulica = ulica
        self.miejscowosc = miejscowosc
        self.nr_budynku = nr_budynku
        self.coordinates = self.get_coordinates()
        self.pracownicy = []
        self.pacjenci = []
        self.patient_markers = []  # To store patient markers
        self.worker_markers = []  # To store worker markers
        self.marker = map_widget.set_marker(
            self.coordinates[0], self.coordinates[1],
            text=self.nazwa,
            command=lambda m=None,: self.on_marker_click()
        )

    def get_coordinates(self):
        geolocator = Nominatim(user_agent="mapbook_ak")
        address = f"{self.ulica} {self.nr_budynku}, {self.miejscowosc}, Polska"
        location = geolocator.geocode(address)
        if location:
            return [location.latitude, location.longitude]
        else:
            return [52.23, 21.01]  # Warszawa fallback

    def on_marker_click(self):
        win = Toplevel(root)
        win.title(f"{self.nazwa} - Wybierz listę")
        win.geometry("300x250")

        Label(win, text=f"Punkt szczepień: {self.nazwa}", font=("Arial", 14, "bold")).pack(pady=10)

        Button(win, text="Pokaż pracowników", width=25,
               command=lambda: [win.destroy(), pokaz_liste_pracownikow(self, z_mapy=True)]).pack(pady=10)
        Button(win, text="Pokaż pacjentów", width=25,
               command=lambda: [win.destroy(), pokaz_liste_pacjentow(self, z_mapy=True)]).pack(pady=10)
        Button(win, text="Zamknij", width=25, command=win.destroy).pack(pady=20)

    def show_patient_locations(self):
        self.clear_patient_markers()

        for pacjent in self.pacjenci:
            marker = map_widget.set_marker(
                pacjent.coordinates[0], pacjent.coordinates[1],
                text=f"{pacjent.imie} {pacjent.nazwisko}",
                marker_color_circle="blue",
                marker_color_outside="blue",
                font=("Helvetica Bold", 10)
            )
            self.patient_markers.append(marker)
            pacjent.marker = marker

        map_widget.set_position(self.coordinates[0], self.coordinates[1])
        map_widget.set_zoom(12)

    def show_worker_locations(self):
        self.clear_worker_markers()

        for pracownik in self.pracownicy:
            marker = map_widget.set_marker(
                pracownik.coordinates[0], pracownik.coordinates[1],
                text=f"{pracownik.imie} {pracownik.nazwisko}",
                marker_color_circle="green",
                marker_color_outside="green",
                font=("Helvetica Bold", 10)
            )
            self.worker_markers.append(marker)
            pracownik.marker = marker

        map_widget.set_position(self.coordinates[0], self.coordinates[1])
        map_widget.set_zoom(12)

    def clear_patient_markers(self):
        for marker in self.patient_markers:
            marker.delete()
        self.patient_markers = []
        for pacjent in self.pacjenci:
            pacjent.marker = None

    def clear_worker_markers(self):
        for marker in self.worker_markers:
            marker.delete()
        self.worker_markers = []
        for pracownik in self.pracownicy:
            pracownik.marker = None


def pokaz_liste_pracownikow(punkt_szczepien, z_mapy=False):
    win = Toplevel(root)
    win.title(f"Pracownicy - {punkt_szczepien.nazwa}")
    win.geometry("300x400")

    Label(win, text=f"Pracownicy punktu: {punkt_szczepien.nazwa}", font=("Arial", 14, "bold")).pack(pady=10)

    listbox = Listbox(win, width=40)
    listbox.pack(pady=10, padx=10, fill=BOTH, expand=True)

    for pracownik in punkt_szczepien.pracownicy:
        listbox.insert(END, f"{pracownik.imie} {pracownik.nazwisko}")

    Button(win, text="Pokaż lokalizacje pracowników",
           command=lambda: punkt_szczepien.show_worker_locations()).pack(pady=5)

    Button(win, text="Zamknij", command=lambda: [punkt_szczepien.clear_worker_markers(), win.destroy()]).pack(pady=5)

    if z_mapy:
        Button(win, text="Cofnij",
               command=lambda: [punkt_szczepien.clear_worker_markers(), win.destroy(), punkt_szczepien.on_marker_click()]).pack(pady=5)


def pokaz_liste_pacjentow(punkt_szczepien, z_mapy=False):
    win = Toplevel(root)
    win.title(f"Pacjenci - {punkt_szczepien.nazwa}")
    win.geometry("300x400")

    Label(win, text=f"Pacjenci punktu: {punkt_szczepien.nazwa}", font=("Arial", 14, "bold")).pack(pady=10)

    listbox = Listbox(win, width=40)
    listbox.pack(pady=10, padx=10, fill=BOTH, expand=True)

    for pacjent in punkt_szczepien.pacjenci:
        listbox.insert(END, f"{pacjent.imie} {pacjent.nazwisko}")

    Button(win, text="Pokaż lokalizacje pacjentów",
           command=lambda: punkt_szczepien.show_patient_locations()).pack(pady=5)

    Button(win, text="Zamknij", command=lambda: [punkt_szczepien.clear_patient_markers(), win.destroy()]).pack(pady=5)

    if z_mapy:
        Button(win, text="Cofnij",
               command=lambda: [punkt_szczepien.clear_patient_markers(), win.destroy(), punkt_szczepien.on_marker_click()]).pack(pady=5)


def open_pacjenci_window(punkt_szczepien):
    pacj_window = Toplevel(root)
    pacj_window.title(f"Pacjenci - {punkt_szczepien.nazwa}")
    pacj_window.geometry("400x500")

    listbox = Listbox(pacj_window, width=40, height=10)
    listbox.pack(pady=10)

    Label(pacj_window, text="Imię:").pack()
    entry_imie = Entry(pacj_window)
    entry_imie.pack()

    Label(pacj_window, text="Nazwisko:").pack()
    entry_nazwisko = Entry(pacj_window)
    entry_nazwisko.pack()

    Label(pacj_window, text="Ulica:").pack()
    entry_ulica = Entry(pacj_window)
    entry_ulica.pack()

    Label(pacj_window, text="Miejscowość:").pack()
    entry_miejscowosc = Entry(pacj_window)
    entry_miejscowosc.pack()

    Label(pacj_window, text="Nr budynku:").pack()
    entry_nr_budynku = Entry(pacj_window)
    entry_nr_budynku.pack()

    selected_index = None

    def refresh_list():
        listbox.delete(0, END)
        for p in punkt_szczepien.pacjenci:
            listbox.insert(END, f"{p.imie} {p.nazwisko}")

    def add_pacjent():
        imie = entry_imie.get()
        nazwisko = entry_nazwisko.get()
        ulica = entry_ulica.get()
        miejscowosc = entry_miejscowosc.get()
        nr_budynku = entry_nr_budynku.get()
        if imie and nazwisko and ulica and miejscowosc and nr_budynku:
            punkt_szczepien.pacjenci.append(Pacjent(imie, nazwisko, ulica, miejscowosc, nr_budynku))
            refresh_list()
            clear_entries()

    def start_edit_pacjent():
        nonlocal selected_index
        sel = listbox.curselection()
        if not sel:
            return
        selected_index = sel[0]
        p = punkt_szczepien.pacjenci[selected_index]
        entry_imie.delete(0, END)
        entry_imie.insert(0, p.imie)
        entry_nazwisko.delete(0, END)
        entry_nazwisko.insert(0, p.nazwisko)
        entry_ulica.delete(0, END)
        entry_ulica.insert(0, p.ulica)
        entry_miejscowosc.delete(0, END)
        entry_miejscowosc.insert(0, p.miejscowosc)
        entry_nr_budynku.delete(0, END)
        entry_nr_budynku.insert(0, p.nr_budynku)

        button_save_edit.config(state=NORMAL)
        button_add.config(state=DISABLED)
        listbox.config(state=DISABLED)
        button_edit.config(state=DISABLED)
        button_delete.config(state=DISABLED)

    def save_edit():
        nonlocal selected_index
        if selected_index is not None:
            p = punkt_szczepien.pacjenci[selected_index]
            p.imie = entry_imie.get()
            p.nazwisko = entry_nazwisko.get()
            p.ulica = entry_ulica.get()
            p.miejscowosc = entry_miejscowosc.get()
            p.nr_budynku = entry_nr_budynku.get()
            p.coordinates = p.get_coordinates()
            if p.marker:
                p.marker.delete()
                p.marker = map_widget.set_marker(
                    p.coordinates[0], p.coordinates[1],
                    text=f"{p.imie} {p.nazwisko}",
                    marker_color_circle="blue",
                    marker_color_outside="blue",
                    font=("Helvetica Bold", 10)
                )
            refresh_list()
            clear_entries()
            reset_buttons()

    def delete_pacjent():
        sel = listbox.curselection()
        if sel:
            idx = sel[0]
            if punkt_szczepien.pacjenci[idx].marker:
                punkt_szczepien.pacjenci[idx].marker.delete()
            del punkt_szczepien.pacjenci[idx]
            refresh_list()

    def clear_entries():
        entry_imie.delete(0, END)
        entry_nazwisko.delete(0, END)
        entry_ulica.delete(0, END)
        entry_miejscowosc.delete(0, END)
        entry_nr_budynku.delete(0, END)

    def reset_buttons():
        button_save_edit.config(state=DISABLED)
        button_add.config(state=NORMAL)
        listbox.config(state=NORMAL)
        button_edit.config(state=NORMAL)
        button_delete.config(state=NORMAL)

    button_add = Button(pacj_window, text="Dodaj", command=add_pacjent)
    button_add.pack(pady=5)

    button_save_edit = Button(pacj_window, text="Zapisz", state=DISABLED, command=save_edit)
    button_save_edit.pack(pady=5)

    button_edit = Button(pacj_window, text="Edytuj pacjenta", command=start_edit_pacjent)
    button_edit.pack(pady=5)

    button_delete = Button(pacj_window, text="Usuń", command=delete_pacjent)
    button_delete.pack(pady=5)

    Button(pacj_window, text="Pokaż na mapie",
           command=lambda: punkt_szczepien.show_patient_locations()).pack(pady=5)

    Button(pacj_window, text="Zamknij",
           command=lambda: [punkt_szczepien.clear_patient_markers(), pacj_window.destroy()]).pack(pady=10)

    refresh_list()


def open_pracownicy_window(punkt_szczepien):
    prac_window = Toplevel(root)
    prac_window.title(f"Pracownicy - {punkt_szczepien.nazwa}")
    prac_window.geometry("400x500")

    listbox = Listbox(prac_window, width=40, height=10)
    listbox.pack(pady=10)

    Label(prac_window, text="Imię:").pack()
    entry_imie = Entry(prac_window)
    entry_imie.pack()

    Label(prac_window, text="Nazwisko:").pack()
    entry_nazwisko = Entry(prac_window)
    entry_nazwisko.pack()

    Label(prac_window, text="Ulica:").pack()
    entry_ulica = Entry(prac_window)
    entry_ulica.pack()

    Label(prac_window, text="Miejscowość:").pack()
    entry_miejscowosc = Entry(prac_window)
    entry_miejscowosc.pack()

    Label(prac_window, text="Nr budynku:").pack()
    entry_nr_budynku = Entry(prac_window)
    entry_nr_budynku.pack()

    selected_index = None

    def refresh_list():
        listbox.delete(0, END)
        for p in punkt_szczepien.pracownicy:
            listbox.insert(END, f"{p.imie} {p.nazwisko}")

    def add_pracownik():
        imie = entry_imie.get()
        nazwisko = entry_nazwisko.get()
        ulica = entry_ulica.get()
        miejscowosc = entry_miejscowosc.get()
        nr_budynku = entry_nr_budynku.get()
        if imie and nazwisko and ulica and miejscowosc and nr_budynku:
            punkt_szczepien.pracownicy.append(Pracownik(imie, nazwisko, ulica, miejscowosc, nr_budynku))
            refresh_list()
            clear_entries()

    def start_edit_pracownik():
        nonlocal selected_index
        sel = listbox.curselection()
        if not sel:
            return
        selected_index = sel[0]
        p = punkt_szczepien.pracownicy[selected_index]
        entry_imie.delete(0, END)
        entry_imie.insert(0, p.imie)
        entry_nazwisko.delete(0, END)
        entry_nazwisko.insert(0, p.nazwisko)
        entry_ulica.delete(0, END)
        entry_ulica.insert(0, p.ulica)
        entry_miejscowosc.delete(0, END)
        entry_miejscowosc.insert(0, p.miejscowosc)
        entry_nr_budynku.delete(0, END)
        entry_nr_budynku.insert(0, p.nr_budynku)

        button_save_edit.config(state=NORMAL)
        button_add.config(state=DISABLED)
        listbox.config(state=DISABLED)
        button_edit.config(state=DISABLED)
        button_delete.config(state=DISABLED)

    def save_edit():
        nonlocal selected_index
        if selected_index is not None:
            p = punkt_szczepien.pracownicy[selected_index]
            p.imie = entry_imie.get()
            p.nazwisko = entry_nazwisko.get()
            p.ulica = entry_ulica.get()
            p.miejscowosc = entry_miejscowosc.get()
            p.nr_budynku = entry_nr_budynku.get()
            p.coordinates = p.get_coordinates()
            if p.marker:
                p.marker.delete()
                p.marker = map_widget.set_marker(
                    p.coordinates[0], p.coordinates[1],
                    text=f"{p.imie} {p.nazwisko}",
                    marker_color_circle="green",
                    marker_color_outside="green",
                    font=("Helvetica Bold", 10)
                )
            refresh_list()
            clear_entries()
            reset_buttons()

    def delete_pracownik():
        sel = listbox.curselection()
        if sel:
            idx = sel[0]
            if punkt_szczepien.pracownicy[idx].marker:
                punkt_szczepien.pracownicy[idx].marker.delete()
            del punkt_szczepien.pracownicy[idx]
            refresh_list()

    def clear_entries():
        entry_imie.delete(0, END)
        entry_nazwisko.delete(0, END)
        entry_ulica.delete(0, END)
        entry_miejscowosc.delete(0, END)
        entry_nr_budynku.delete(0, END)

    def reset_buttons():
        button_save_edit.config(state=DISABLED)
        button_add.config(state=NORMAL)
        listbox.config(state=NORMAL)
        button_edit.config(state=NORMAL)
        button_delete.config(state=NORMAL)

    button_add = Button(prac_window, text="Dodaj", command=add_pracownik)
    button_add.pack(pady=5)

    button_save_edit = Button(prac_window, text="Zapisz", state=DISABLED, command=save_edit)
    button_save_edit.pack(pady=5)

    button_edit = Button(prac_window, text="Edytuj pracownika", command=start_edit_pracownik)
    button_edit.pack(pady=5)

    button_delete = Button(prac_window, text="Usuń", command=delete_pracownik)
    button_delete.pack(pady=5)

    Button(prac_window, text="Pokaż na mapie",
           command=lambda: punkt_szczepien.show_worker_locations()).pack(pady=5)

    Button(prac_window, text="Zamknij",
           command=lambda: [punkt_szczepien.clear_worker_markers(), prac_window.destroy()]).pack(pady=10)

    refresh_list()


def show_pacjenci_window():
    global active_punkt_szczepien
    if listbox_punkty_szczepien.curselection():
        i = listbox_punkty_szczepien.curselection()[0]
        active_punkt_szczepien = punkty_szczepien_list[i]
        open_pacjenci_window(active_punkt_szczepien)


def show_pracownicy_window():
    global active_punkt_szczepien
    if listbox_punkty_szczepien.curselection():
        i = listbox_punkty_szczepien.curselection()[0]
        active_punkt_szczepien = punkty_szczepien_list[i]
        open_pracownicy_window(active_punkt_szczepien)


def dodaj_punkt_szczepien():
    nazwa = entry_nazwa.get()
    ulica = entry_ulica.get()
    miejscowosc = entry_miejscowosc.get()
    nr = entry_nr_budynku.get()

    punkt = PunktSzczepien(nazwa, ulica, miejscowosc, nr)
    punkty_szczepien_list.append(punkt)
    czysc_formularz()
    pokaz_liste_punktow_szczepien()


def czysc_formularz():
    entry_nazwa.delete(0, END)
    entry_ulica.delete(0, END)
    entry_miejscowosc.delete(0, END)
    entry_nr_budynku.delete(0, END)


def pokaz_liste_punktow_szczepien():
    listbox_punkty_szczepien.delete(0, END)
    for i, punkt in enumerate(punkty_szczepien_list):
        listbox_punkty_szczepien.insert(i, f"{i + 1}. {punkt.nazwa}, {punkt.ulica}")


def usun_punkt_szczepien():
    i = listbox_punkty_szczepien.index(ACTIVE)
    punkty_szczepien_list[i].marker.delete()
    for pacjent in punkty_szczepien_list[i].pacjenci:
        if pacjent.marker:
            pacjent.marker.delete()
    for pracownik in punkty_szczepien_list[i].pracownicy:
        if pracownik.marker:
            pracownik.marker.delete()
    punkty_szczepien_list.pop(i)
    pokaz_liste_punktow_szczepien()


def pokaz_szczegoly_punktu_szczepien():
    i = listbox_punkty_szczepien.index(ACTIVE)
    p = punkty_szczepien_list[i]
    label_nazwa_wartosc.config(text=p.nazwa)
    label_ulica_wartosc.config(text=p.ulica)
    label_miejscowosc_wartosc.config(text=p.miejscowosc)
    label_nr_budynku_wartosc.config(text=p.nr_budynku)
    map_widget.set_position(p.coordinates[0], p.coordinates[1])
    map_widget.set_zoom(12)


def edytuj_punkt_szczepien():
    i = listbox_punkty_szczepien.index(ACTIVE)
    p = punkty_szczepien_list[i]
    entry_nazwa.delete(0, END)
    entry_nazwa.insert(0, p.nazwa)
    entry_ulica.delete(0, END)
    entry_ulica.insert(0, p.ulica)
    entry_miejscowosc.delete(0, END)
    entry_miejscowosc.insert(0, p.miejscowosc)
    entry_nr_budynku.delete(0, END)
    entry_nr_budynku.insert(0, p.nr_budynku)
    button_dodaj.config(text="Zapisz", command=lambda: zapisz_edycje_punktu(i))


def zapisz_edycje_punktu(i):
    p = punkty_szczepien_list[i]
    p.nazwa = entry_nazwa.get()
    p.ulica = entry_ulica.get()
    p.miejscowosc = entry_miejscowosc.get()
    p.nr_budynku = entry_nr_budynku.get()

    p.marker.delete()
    p.coordinates = p.get_coordinates()
    p.marker = map_widget.set_marker(
        p.coordinates[0], p.coordinates[1], text=p.nazwa,
        command=lambda m=None, self=p: self.on_marker_click()
    )

    button_dodaj.config(text="Dodaj punkt szczepień", command=dodaj_punkt_szczepien)
    czysc_formularz()
    pokaz_liste_punktow_szczepien()


# --- GUI ---
root = Tk()
root.geometry("1200x900")
root.title("System Zarządzania Punktami Szczepień")

ramka_lista = Frame(root)
ramka_formularz = Frame(root)
ramka_szczegoly = Frame(root)
ramka_mapa = Frame(root)

ramka_lista.grid(row=0, column=0)
ramka_formularz.grid(row=0, column=1)
ramka_szczegoly.grid(row=1, column=0, columnspan=2)
ramka_mapa.grid(row=2, column=0, columnspan=2)

Label(ramka_lista, text="LISTA PUNKTÓW SZCZEPIEŃ").grid(row=0, column=0, columnspan=3)
listbox_punkty_szczepien = Listbox(ramka_lista, width=60, height=15)
listbox_punkty_szczepien.grid(row=1, column=0, columnspan=3)
Button(ramka_lista, text="Pokaż szczegóły", command=pokaz_szczegoly_punktu_szczepien).grid(row=2, column=0)
Button(ramka_lista, text="Usuń punkt", command=usun_punkt_szczepien).grid(row=2, column=1)
Button(ramka_lista, text="Edytuj punkt", command=edytuj_punkt_szczepien).grid(row=2, column=2)
Button(ramka_lista, text="Pracownicy", command=show_pracownicy_window).grid(row=3, column=0)
Button(ramka_lista, text="Pacjenci", command=show_pacjenci_window).grid(row=3, column=1)

Label(ramka_formularz, text="Nazwa Punktu Szczepień").grid(row=1, column=0, sticky=W)
Label(ramka_formularz, text="Ulica").grid(row=2, column=0, sticky=W)
Label(ramka_formularz, text="Miejscowość").grid(row=3, column=0, sticky=W)
Label(ramka_formularz, text="Numer Budynku").grid(row=4, column=0, sticky=W)

entry_nazwa = Entry(ramka_formularz)
entry_nazwa.grid(row=1, column=1)
entry_ulica = Entry(ramka_formularz)
entry_ulica.grid(row=2, column=1)
entry_miejscowosc = Entry(ramka_formularz)
entry_miejscowosc.grid(row=3, column=1)
entry_nr_budynku = Entry(ramka_formularz)
entry_nr_budynku.grid(row=4, column=1)

button_dodaj = Button(ramka_formularz, text="Dodaj punkt szczepień", command=dodaj_punkt_szczepien)
button_dodaj.grid(row=5, column=0, columnspan=2)

Label(ramka_szczegoly, text="Szczegóły punktu szczepień:").grid(row=0, column=0)
Label(ramka_szczegoly, text="Nazwa:").grid(row=1, column=0)
label_nazwa_wartosc = Label(ramka_szczegoly, text="...")
label_nazwa_wartosc.grid(row=1, column=1)
Label(ramka_szczegoly, text="Ulica:").grid(row=1, column=2)
label_ulica_wartosc = Label(ramka_szczegoly, text="...")
label_ulica_wartosc.grid(row=1, column=3)
Label(ramka_szczegoly, text="Miejscowość:").grid(row=1, column=4)
label_miejscowosc_wartosc = Label(ramka_szczegoly, text="...")
label_miejscowosc_wartosc.grid(row=1, column=5)
Label(ramka_szczegoly, text="Nr Budynku:").grid(row=1, column=6)
label_nr_budynku_wartosc = Label(ramka_szczegoly, text="...")
label_nr_budynku_wartosc.grid(row=1, column=7)

map_widget = tkintermapview.TkinterMapView(ramka_mapa, width=1200, height=600, corner_radius=5)
map_widget.set_position(52.23, 21.0)
map_widget.set_zoom(6)
map_widget.grid(row=0, column=0, columnspan=3)

root.mainloop()