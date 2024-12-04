"""
Module pour la génération d'une carte interactive entre deux stations.

Ce script permet à l'utilisateur de visualiser le chemin le plus court entre deux stations de vélos à Montpellier. 
Il utilise des données CSV contenant les trajets de vélos partagés, les coordonnées des stations stockées dans un fichier JSON, 
et un graphe routier OSMNX pour calculer le chemin optimal.

Dépendances :
- osmnx
- folium
- networkx
- json
- pandas
- geopy
- time
- sys
- os

Auteur :
    El Mazzouji Wahel
"""
import osmnx as ox
import folium
import networkx as nx
import pandas as pd
from geopy.geocoders import Nominatim
import json
import time
import sys
import os

# Ajouter le dossier parent (data) au chemin
sys.path.append(os.path.abspath("C:/Users/welma/HAX712X_WAHEL/Projet_HAX712X/data"))

from traitement_donnees.utils import corriger_encodage

# Chemin vers le fichier CSV
file_path = 'C:/Users/welma/HAX712X_Wahel/Projet_HAX712X/data/TAM_MMM_CoursesVelomagg.csv'
data = pd.read_csv(file_path)

data['Departure station'] = data['Departure station'].apply(corriger_encodage)
data['Return station'] = data['Return station'].apply(corriger_encodage)

# Exclure les stations spécifiques non pertinentes
stations_exclues = ["AtelierTAM", "Station SAV", "Smoove_Test"]
data = data[~data['Departure station'].isin(stations_exclues)]
data = data[~data['Return station'].isin(stations_exclues)]

# Charger le fichier JSON existant pour récupérer les coordonnées des stations
try:
    with open("station_coords.json", "r") as infile:
        coordonnees_stations = json.load(infile)
except FileNotFoundError:
    coordonnees_stations = {}

# Génération de la carte
ville = "Montpellier, France"
G = ox.graph_from_place(ville, network_type="all")
m = folium.Map(location=[43.6114, 3.8767], zoom_start=13)

# Interaction avec l'utilisateur pour choisir la station de départ et d'arrivée
depart_station = input("Veuillez entrer la station de départ : ")
arrivee_station = input("Veuillez entrer la station d'arrivée : ")

# Vérifier si les stations saisies existent dans le dataset
if depart_station not in coordonnees_stations:
    print(f"Station de départ {depart_station} non trouvée.")
    exit()

if arrivee_station not in coordonnees_stations:
    print(f"Station d'arrivée {arrivee_station} non trouvée.")
    exit()

# Récupérer les coordonnées des stations
coords_depart = coordonnees_stations[depart_station]
coords_retour = coordonnees_stations[arrivee_station]

# Trouver les nœuds les plus proches dans le graphe OSM
depart_node = ox.distance.nearest_nodes(G, coords_depart['longitude'], coords_depart['latitude'])
retour_node = ox.distance.nearest_nodes(G, coords_retour['longitude'], coords_retour['latitude'])

# Calculer le chemin le plus court
route = nx.shortest_path(G, source=depart_node, target=retour_node, weight='length')

# Tracer la route sur la carte
route_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in route]
folium.PolyLine(locations=route_coords, color='blue', weight=5, opacity=0.7).add_to(m)

# Ajouter les marqueurs pour les stations
folium.Marker(
    location=[coords_depart['latitude'], coords_depart['longitude']],
    popup=f"Départ: {depart_station}",
    icon=folium.Icon(color='blue')
).add_to(m)

folium.Marker(
    location=[coords_retour['latitude'], coords_retour['longitude']],
    popup=f"Arrivée: {arrivee_station}",
    icon=folium.Icon(color='red')
).add_to(m)

# Sauvegarder la carte dans un fichier HTML
m.save("carte_trajet_entre_stations.html")

# Afficher un message pour indiquer que la carte est prête
print("La carte a été sauvegardée sous 'carte_trajet_entre_stations.html'. Ouvrez ce fichier dans votre navigateur pour afficher la carte.")
