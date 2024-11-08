import osmnx as ox
import folium
import networkx as nx
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
        time.sleep(1)  # Pause pour éviter les limites de requêtes

# Génération de la carte
ville = "Montpellier, France"
G = ox.graph_from_place(ville, network_type="all")
m = folium.Map(location=[43.6114, 3.8767], zoom_start=13)

# Extraction des trajets
data_traité = pd.read_csv("C:/Users/welma/HAX712X_Wahel/Projet_HAX712X/data/TAM_MMM_CoursesVelomagg.csv").dropna()
trajets = data_traité[['Departure', 'Departure station', 'Return station', 'Duration (sec.)', 'Covered distance (m)']]
liste_trajet = trajets

# Nettoyage des colonnes
liste_trajet.loc[:, 'Departure station'] = liste_trajet['Departure station'].apply(corriger_encodage)
liste_trajet.loc[:, 'Return station'] = liste_trajet['Return station'].apply(corriger_encodage)

# Interaction avec l'utilisateur
date = input("Veuillez choisir une date : ")
trajets_du_jour = liste_trajet[liste_trajet['Departure'].str.startswith(date)]
nombre_trajets = len(trajets_du_jour)

print("Nous avons ", nombre_trajets, "trajets à cette date.")

# Définir une fonction pour choisir la couleur en fonction de la distance
def couleur_par_distance(distance):
    if distance < 1000:  # Moins de 1 km
        return 'green'
    elif distance < 5000:  # Moins de 5 km
        return 'blue'
    else:  # Plus de 5 km
        return 'red'

# J'affiche les trajets de la journée sur la carte
for i in range(min(nombre_trajets, 50)):  # Limiter à 20 trajets maximum
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
    <p><span style="color: blue;">&#9679;</span> Entre 1 km et 5 km</p>
    <p><span style="color: red;">&#9679;</span> Plus de 5 km</p>
</div>
"""

m.get_root().html.add_child(folium.Element(legend_html))

# Sauvegarder la carte dans un fichier HTML
m.save("carte_montpellier_ameliore.html")

# Afficher un message pour indiquer que la carte est prête
print("La carte a été sauvegardée sous 'carte_montpellier_ameliore.html'. Ouvrez ce fichier dans votre navigateur pour afficher la carte.")
