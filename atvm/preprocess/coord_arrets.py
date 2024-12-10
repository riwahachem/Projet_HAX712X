"""
Module pour récupérer les coordonnées géographiques des stations de vélos à Montpellier.

Ce script prend un fichier CSV contenant des données de stations de vélos, corrige les encodages des noms de stations, 
puis obtient les coordonnées géographiques de chaque station unique à l'aide de l'API Nominatim de Geopy.

Les étapes du processus sont les suivantes :
- Lecture des données depuis un fichier CSV contenant des stations de vélos.
- Correction des encodages des noms de stations avec la fonction `corriger_encodage`.
- Extraction des stations uniques et suppression des doublons.
- Renommage des stations spécifiques (par exemple, "FacdesSciences" devient "Faculté des sciences").
- Exclusion de certaines stations de la liste des stations à traiter.
- Recherche des coordonnées géographiques des stations uniques en utilisant le service de géocodage de Nominatim.
- Sauvegarde des coordonnées obtenues dans un fichier JSON.
- Affichage du nombre de stations avec coordonnées et de celles qui ont été exclues.

Entrées :
- Un fichier CSV (`TAM_MMM_CoursesVelomagg.csv`) contenant des informations sur les stations de vélos.
- La fonction `corriger_encodage` pour corriger les noms de stations.

Sorties :
- Un fichier JSON (`station_coords.json`) contenant les coordonnées géographiques des stations de vélos qui ont été géocodées avec succès.

Exclusions :
- Certaines stations comme "Smoove_Test", "AtelierTAM", "Station SAV", et "Pérols Etang de l'Or" sont explicitement exclues.

Dépendances :
- pandas
- geopy
- json
- time
- sys
- os

Auteur : Wahel El Mazzouji
"""
import pandas as pd
from geopy.geocoders import Nominatim
import json
import time
import sys
import os

# Ajouter le dossier parent (data) au chemin
sys.path.append(os.path.abspath("../data_atvm"))

from utils import corriger_encodage
# Chemin vers le fichier CSV
file_path =  os.path.abspath(os.path.join(os.path.dirname(__file__),'../data_atvm/TAM_MMM_CoursesVelomagg.csv'))
data = pd.read_csv(file_path)

data['Departure station'] = data['Departure station'].apply(corriger_encodage)
data['Return station'] = data['Return station'].apply(corriger_encodage)

# Extraction des stations uniques corrigées
stations_uniques = pd.concat([data['Departure station'], data['Return station']]).unique()
stations_uniques = [station for station in stations_uniques if isinstance(station, str)]

# Renommer "FacdesSciences" en "Faculté des sciences"
stations_uniques = [station.replace("FacdesSciences", "Faculté des sciences") for station in stations_uniques]

# Exclure explicitement certaines stations
stations_a_exclure = ['Smoove_Test', 'AtelierTAM', 'Station SAV', 'Pérols Etang de l\'Or', 'Plan Cabanes']
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
