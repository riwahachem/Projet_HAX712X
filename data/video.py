import os
import osmnx as ox
import folium
import networkx as nx
import pandas as pd
from unidecode import unidecode
from geopy.geocoders import Nominatim
import json
import time
import re
import imageio.v2 as iio  # Importer imageio.v2 explicitement
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image  # Pour redimensionner l'image

# Configuration de Selenium pour un usage sans interface graphique (headless)
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(options=options)

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
        station_name = re.sub(r'^\d+\s*', '', station_name).strip()
        return station_name
    return station_name

data['Departure station'] = data['Departure station'].apply(corriger_encodage)
data['Return station'] = data['Return station'].apply(corriger_encodage)

# Extraction des stations uniques corrigées
stations_uniques = pd.concat([data['Departure station'], data['Return station']]).unique()
stations_uniques = [station for station in stations_uniques if isinstance(station, str)]
stations_uniques = [station.replace("FacdesSciences", "Faculté des sciences") for station in stations_uniques]

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
    if station not in coordonnees_stations:
        coords = get_station_coordinates(station)
        if coords:
            coordonnees_stations[station] = coords
            print(f"Coordonnées trouvées pour {station}: {coords}")
        else:
            print(f"Coordonnées non trouvées pour {station}")
        
        # Sauvegarde en cours de traitement
        with open("station_coords.json", "w") as outfile:
            json.dump(coordonnees_stations, outfile)
        time.sleep(1)

# Génération de la carte
ville = "Montpellier, France"
G = ox.graph_from_place(ville, network_type="all")

# Extraction des trajets
trajets = data[['Departure', 'Departure station', 'Return station', 'Duration (sec.)', 'Covered distance (m)']]

# Interaction avec l'utilisateur pour choisir une date
date = input("Veuillez choisir une date (au format YYYY-MM-DD) : ")
trajets_du_jour = trajets[trajets['Departure'].str.startswith(date)]
nombre_trajets = len(trajets_du_jour)

print(f"Nous avons {nombre_trajets} trajets à cette date.")

# Définir une fonction pour choisir la couleur en fonction de la distance
def couleur_par_distance(distance):
    if distance < 1000:  # Moins de 1 km
        return 'green'
    elif distance < 5000:  # Moins de 5 km
        return 'blue'
    else:  # Plus de 5 km
        return 'red'

# Créer un writer pour la vidéo sans sauvegarder de fichiers PNG
with iio.get_writer('trajets_video.mp4', fps=10, format="mp4") as writer:
    for i in range(min(nombre_trajets, 50)):  # Limiter à 50 trajets pour la démonstration
        trajet = trajets_du_jour.iloc[i]
        depart_station = trajet['Departure station']
        retour_station = trajet['Return station']
        distance = trajet['Covered distance (m)']

        # Créez une nouvelle carte pour chaque trajet
        m = folium.Map(location=[43.6114, 3.8767], zoom_start=13)

        if depart_station in coordonnees_stations and retour_station in coordonnees_stations:
            coords_depart = coordonnees_stations[depart_station]
            coords_retour = coordonnees_stations[retour_station]
            
            depart_node = ox.distance.nearest_nodes(G, coords_depart['longitude'], coords_depart['latitude'])
            retour_node = ox.distance.nearest_nodes(G, coords_retour['longitude'], coords_retour['latitude'])

            route = nx.shortest_path(G, source=depart_node, target=retour_node, weight='length')
            route_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in route]
            folium.PolyLine(locations=route_coords, color=couleur_par_distance(distance), weight=5, opacity=0.7).add_to(m)

            folium.Marker(
                location=[coords_depart['latitude'], coords_depart['longitude']],
                popup=f"Départ: {depart_station}",
                icon=folium.Icon(color='blue')
            ).add_to(m)

            folium.Marker(
                location=[coords_retour['latitude'], coords_retour['longitude']],
                popup=f"Retour: {retour_station}",
                icon=folium.Icon(color='red')
            ).add_to(m)

        m.save("temp_map.html")
        driver.get("file://" + os.path.abspath("temp_map.html"))
        img_data = driver.get_screenshot_as_png()

        img = Image.open(BytesIO(img_data))
        img = img.resize((1360, 768))
        img_bytes = BytesIO()
        img.save(img_bytes, format="PNG")

        writer.append_data(iio.imread(img_bytes))

driver.quit()
print("La vidéo a été sauvegardée sous 'trajets_video.mp4'.")
