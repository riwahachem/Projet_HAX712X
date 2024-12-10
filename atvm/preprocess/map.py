"""
Module pour la génération d'une carte interactive basée sur des trajets de vélos.

Ce module utilise des données CSV contenant les trajets de vélos partagés, corrige les noms des stations, calcule les trajets les plus courts en utilisant un graphe routier d'OSMNX, et affiche les trajets sur une carte interactive à l'aide de Folium.

Fonctionnalités :
- Chargement et filtrage des données de trajets de vélos
- Calcul du chemin le plus court entre stations en fonction du graphe routier
- Affichage des trajets sur une carte interactive avec des marqueurs pour les stations
- Code couleur des trajets en fonction de leur distance
- Interaction avec l'utilisateur (choix de la date, du nombre de trajets à afficher)

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
sys.path.append(os.path.abspath("../data_atvm"))

from .utils import corriger_encodage
# Chemin vers le fichier CSV
file_path =  os.path.abspath(os.path.join(os.path.dirname(__file__),'../data_atvm/TAM_MMM_CoursesVelomagg.csv'))
data = pd.read_csv(file_path)

data['Departure station'] = data['Departure station'].apply(corriger_encodage)
data['Return station'] = data['Return station'].apply(corriger_encodage)

# Exclure les stations spécifiques non pertinentes
stations_exclues = ["AtelierTAM", "Station SAV", "Smoove_Test"]
data = data[~data['Departure station'].isin(stations_exclues)]
data = data[~data['Return station'].isin(stations_exclues)]

# Charger le fichier JSON existant
try:
    with open("station_coords.json", "r") as infile:
        coordonnees_stations = json.load(infile)
except FileNotFoundError:
    coordonnees_stations = {}

# Génération de la carte
ville = "Montpellier, France"
G = ox.graph_from_place(ville, network_type="all")
m = folium.Map(location=[43.6114, 3.8767], zoom_start=13)

# Interaction avec l'utilisateur pour choisir la date et le nombre de trajets
#date = input("Veuillez choisir une date (format YYYY-MM-DD) : ")
date = os.getenv("USER_DATE", input("Veuillez choisir une date (format YYYY-MM-DD) : "))
trajets_du_jour = data[data['Departure'].str.startswith(date)]
nombre_trajets = len(trajets_du_jour)

print(f"Nous avons trouvé {nombre_trajets} trajets à cette date.")

# Demander à l'utilisateur combien de trajets afficher
nb_trajets_max = min(nombre_trajets, nombre_trajets)  # Pas de limite imposée
try:
    #nb_trajets_a_afficher = int(input(f"Combien de trajets voulez-vous afficher (entre 1 et {nb_trajets_max}) ? "))
    nb_trajets_a_afficher = int(os.getenv("USER_TRAJETS", input(f"Combien de trajets voulez-vous afficher (entre 1 et {nb_trajets_max}) ? ")))
    if nb_trajets_a_afficher > nb_trajets_max or nb_trajets_a_afficher < 1:
        raise ValueError("Nombre hors limites.")
except (ValueError, TypeError):
    print("Entrée invalide, affichage de 10 trajets par défaut.")
    nb_trajets_a_afficher = 10

print(f"{nb_trajets_a_afficher} trajets seront affichés et calculés.")

# Définir une fonction pour choisir la couleur en fonction de la distance
def couleur_par_distance(distance):
    """
    Associe une couleur à un trajet en fonction de sa distance.

    Args:
        param: distance (float): Distance du trajet en mètres.

    Returns:
        str: Couleur associée au trajet ('green', 'blue', 'orange', 'red').
    """
    if distance < 1000:  # Moins de 1 km
        return 'green'
    elif distance < 2000:  # Moins de 5 km
        return 'blue'
    elif distance < 3000:  # Moins de 5 km
        return 'orange'
    else:  # Plus de 5 km
        return 'red'

# Afficher les trajets de la journée sur la carte
for i in range(nb_trajets_a_afficher):
    trajet = trajets_du_jour.iloc[i]
    depart_station = trajet['Departure station']
    retour_station = trajet['Return station']
    distance = trajet['Covered distance (m)']  # Récupérer la distance du trajet

    if depart_station in coordonnees_stations and retour_station in coordonnees_stations:
        # Récupérer les coordonnées des stations
        coords_depart = coordonnees_stations[depart_station]
        coords_retour = coordonnees_stations[retour_station]
        
        # Trouver les nœuds les plus proches dans le graphe
        depart_node = ox.distance.nearest_nodes(G, coords_depart['longitude'], coords_depart['latitude'])
        retour_node = ox.distance.nearest_nodes(G, coords_retour['longitude'], coords_retour['latitude'])

        # Calculer le chemin le plus court
        route = nx.shortest_path(G, source=depart_node, target=retour_node, weight='length')

        # Tracer la route sur la carte avec la couleur dynamique
        route_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in route]
        folium.PolyLine(locations=route_coords, color=couleur_par_distance(distance), weight=5, opacity=0.7).add_to(m)

        # Ajouter les marqueurs pour les stations
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

# Ajouter une légende
legend_html = """
<div style="position: fixed; 
            bottom: 50px; left: 50px; width: 200px; height: auto; 
            background-color: white; opacity: 0.8; z-index: 1000; border:2px solid grey; 
            padding: 10px; font-size: 14px;">
    <h4 style="margin: 0;">Légende des Couleurs</h4>
    <p><span style="color: green;">&#9679;</span> Moins de 1 km</p>
    <p><span style="color: blue;">&#9679;</span> Entre 1 km et 2 km</p>
    <p><span style="color: orange;">&#9679;</span> Entre 2 km et 3 km</p>
    <p><span style="color: red;">&#9679;</span> Plus de 5 km</p>
</div>
"""

m.get_root().html.add_child(folium.Element(legend_html))

# Sauvegarder la carte dans un fichier HTML
m.save("carte_montpellier_ameliore.html")

# Afficher un message pour indiquer que la carte est prête
print("La carte a été sauvegardée sous 'carte_montpellier_ameliore.html'. Ouvrez ce fichier dans votre navigateur pour afficher la carte.")
