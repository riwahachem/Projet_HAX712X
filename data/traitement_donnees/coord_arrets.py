import pandas as pd
from unidecode import unidecode
from geopy.geocoders import Nominatim
import json
import time
import re

# Chemin vers le fichier CSV
file_path = 'C:/Users/welma/HAX712X_Wahel/Projet_HAX712X/data/TAM_MMM_CoursesVelomagg.csv'
data = pd.read_csv(file_path)

# Correction des noms de stations
def corriger_encodage(station_name):
    if isinstance(station_name, str):
        try:
            station_name = station_name.encode('latin1').decode('utf-8')
        except (UnicodeEncodeError, UnicodeDecodeError):
            station_name = unidecode(station_name)
        station_name = re.sub(r'^\d+\s*', '', station_name).strip()  # Supprime les numéros en début
        return station_name
    return station_name

data['Departure station'] = data['Departure station'].apply(corriger_encodage)
data['Return station'] = data['Return station'].apply(corriger_encodage)

# Extraction des stations uniques corrigées
stations_uniques = pd.concat([data['Departure station'], data['Return station']]).unique()
stations_uniques = [station for station in stations_uniques if isinstance(station, str)]

# Renommer "FacdesSciences" en "Faculté des sciences"
stations_uniques = [station.replace("FacdesSciences", "Faculté des sciences") for station in stations_uniques]

# Exclure explicitement certaines stations
stations_a_exclure = ['Smoove_Test', 'AtelierTAM', 'Station SAV', 'Pérols Etang de l\'Or']
stations_uniques = [station for station in stations_uniques if station not in stations_a_exclure]

# Initialiser le géocodeur et charger le JSON existant
geolocator = Nominatim(user_agent="velomagg_locator")
try:
    with open("station_coords.json", "r") as infile:
        coordonnees_stations = json.load(infile)
except FileNotFoundError:
    coordonnees_stations = {}

def get_station_coordinates(station_name):
    if not isinstance(station_name, str):
        return None
    options = [
        f"{station_name}, Montpellier, France",
        f"{station_name.replace('-', ' ')}, Montpellier, France",
        f"{station_name.split('-')[0]}, Montpellier, France",
        f"{station_name.split('-')[-1]}, Montpellier, France",
        f"{station_name}, France"
    ]
    if "Fac" in station_name:
        options.append(station_name.replace("Fac", "Faculté") + ", Montpellier, France")
    for query in options:
        try:
            location = geolocator.geocode(query)
            if location:
                return {"latitude": location.latitude, "longitude": location.longitude}
        except Exception as e:
            print(f"Erreur pour {query}: {e}")
        time.sleep(1)
    return None

# Boucle pour obtenir et sauvegarder les coordonnées
for station in stations_uniques:
    if station not in coordonnees_stations and station not in stations_a_exclure:
        coords = get_station_coordinates(station)
        if coords:
            coordonnees_stations[station] = coords
            print(f"Coordonnées trouvées pour {station}: {coords}")
        else:
            print(f"Coordonnées non trouvées pour {station}")
        with open("station_coords.json", "w") as outfile:
            json.dump(coordonnees_stations, outfile, indent=4)
        time.sleep(1)

# Filtrer les stations avec coordonnées non nulles
coordonnees_stations_filtrees = {
    k: v for k, v in coordonnees_stations.items() 
    if k not in stations_a_exclure and v is not None
}

# Sauvegarder le dictionnaire filtré dans le fichier JSON
with open("station_coords.json", "w") as outfile:
    json.dump(coordonnees_stations_filtrees, outfile, indent=4)

# Affichage du nombre de stations avec des coordonnées trouvées
nombre_stations_avec_coords = len(coordonnees_stations_filtrees)
print(f"Nombre de stations avec coordonnées : {nombre_stations_avec_coords}")
print("Coordonnées des stations sauvegardées dans station_coords.json")
print(f"Les stations exclues : {stations_a_exclure}")
