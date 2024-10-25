import osmnx as ox
import pandas as pd

file_path = 'C:/Users/welma/HAX712X_Wahel/Projet_HAX712X/data/TAM_MMM_CoursesVelomagg.csv'
data = pd.read_csv(file_path)
data.columns = data.columns.str.strip()
# Extraire les noms uniques des stations de départ et de retour
stations = pd.concat([data['Departure station'], data['Return station']]).unique()

# Fct pour obtenir les coordonnees d'une station avec OpenStreetMap
def get_station_coord(nom):
    try:
        # On utilise OpenStreetMap pour trouver l'emplacement de la station
        loc = ox.geocode(f"{nom}, Montpellier, France")
        return loc
    except:
        return None
# On recupere les coordonnees de chaque station
station_coord = {station: get_station_coord(station) for station in stations}
# On affiche les premieres coordonnees pour verif
print(station_coord)
print (get_station_coord("Faculte des Sciences"))
