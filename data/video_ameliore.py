import os
import osmnx as ox
import pandas as pd
import networkx as nx
from unidecode import unidecode
import json
import re
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from concurrent.futures import ThreadPoolExecutor

# Charger les données
file_path = 'C:/Users/welma/HAX712X_Wahel/Projet_HAX712X/data/TAM_MMM_CoursesVelomagg.csv'
data = pd.read_csv(file_path)

# Convertir la colonne "Departure" en format datetime (si tu l'as dans ton CSV)
data['Departure'] = pd.to_datetime(data['Departure'], errors='coerce')

# Demander à l'utilisateur de saisir une date au format 'YYYY-MM-DD'
date_str = input("Veuillez entrer une date (format YYYY-MM-DD) : ")

try:
    date_saisie = pd.to_datetime(date_str).date()  # Extraire uniquement la date
except ValueError:
    print("Format de date invalide.")
    exit()

# Filtrer les trajets en fonction de la date saisie (sans l'heure)
data_filtered = data[data['Departure'].dt.date == date_saisie].copy()  # Ajout de .copy() pour éviter les vues

# Si aucun trajet n'a été trouvé pour cette date
if data_filtered.empty:
    print(f"Aucun trajet trouvé pour la date {date_saisie}.")
    exit()

# Fonction personnalisée pour corriger les noms des stations
def corriger_nom_station(nom_station):
    if isinstance(nom_station, str):
        try:
            # Correction de l'encodage si nécessaire
            nom_station = nom_station.encode('latin1').decode('utf-8')
        except (UnicodeEncodeError, UnicodeDecodeError):
            nom_station = unidecode(nom_station)
        
        # Supprimer les numéros en début de nom
        nom_station = re.sub(r'^\d+\s*', '', nom_station).strip()

        # Remplacer "FacdesSciences" par "Faculté des Sciences"
        nom_station = nom_station.replace("FacdesSciences", "Faculté des Sciences")
        
        return nom_station
    return nom_station


# Appliquer la fonction à toutes les stations avec .loc[] pour éviter SettingWithCopyWarning
data_filtered.loc[:, 'Departure station'] = data_filtered['Departure station'].apply(corriger_nom_station)
data_filtered.loc[:, 'Return station'] = data_filtered['Return station'].apply(corriger_nom_station)

# Charger les coordonnées des stations depuis un fichier JSON
try:
    with open("station_coords.json", "r") as infile:
        coordonnees_stations = json.load(infile)
except FileNotFoundError:
    coordonnees_stations = {}

# Ajouter les coordonnées à chaque trajet avec .loc[]
data_filtered.loc[:, 'latitude_depart'] = data_filtered['Departure station'].map(lambda x: coordonnees_stations.get(x, {}).get('latitude'))
data_filtered.loc[:, 'longitude_depart'] = data_filtered['Departure station'].map(lambda x: coordonnees_stations.get(x, {}).get('longitude'))
data_filtered.loc[:, 'latitude_retour'] = data_filtered['Return station'].map(lambda x: coordonnees_stations.get(x, {}).get('latitude'))
data_filtered.loc[:, 'longitude_retour'] = data_filtered['Return station'].map(lambda x: coordonnees_stations.get(x, {}).get('longitude'))

# Demander combien de trajets afficher
min_trajets = int(input("Combien de trajets voulez-vous afficher sur votre journée ? "))
df = data_filtered.iloc[:min_trajets].dropna(subset=['latitude_depart', 'longitude_depart', 'latitude_retour', 'longitude_retour'])
df.reset_index(drop=True, inplace=True)

# Vérifier combien de trajets restent après filtrage (supprimant les NaN)
trajets_valides = len(df)
print(f"Nombre de trajets valides après filtrage : {trajets_valides}")

# Charger le réseau de Montpellier depuis OpenStreetMap
G = ox.graph_from_place("Montpellier, France", network_type="all")

# Initialiser la figure pour l'animation
fig, ax = plt.subplots(figsize=(12, 8))
ax.set_title("Trajets à Montpellier")
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ox.plot_graph(G, ax=ax, show=False, close=False, node_size=0, edge_color="grey", edge_linewidth=0.5)

# Fonction personnalisée pour calculer le chemin le plus court entre deux points
def calcul_chemin_vélo(row):
    try:
        depart_lat, depart_lon = row['latitude_depart'], row['longitude_depart']
        arrivee_lat, arrivee_lon = row['latitude_retour'], row['longitude_retour']
        
        noeud_deb = ox.distance.nearest_nodes(G, depart_lon, depart_lat)
        noeud_fin = ox.distance.nearest_nodes(G, arrivee_lon, arrivee_lat)
        
        chemin = nx.shortest_path(G, noeud_deb, noeud_fin, weight="length")
        return chemin
    except Exception as e:
        print(f"Erreur pour le trajet entre {row['Departure station']} et {row['Return station']}: {e}")
        return None

# Calculer les chemins en parallèle pour améliorer la vitesse d'exécution
with ThreadPoolExecutor() as executor:
    chemins = list(executor.map(calcul_chemin_vélo, [row for _, row in df.iterrows()]))

# Filtrer les trajets valides (ceux qui ont pu calculer un chemin)
trajets_valides_calcules = [chemin for chemin in chemins if chemin is not None]
print(f"Nombre de trajets valides calculés : {len(trajets_valides_calcules)}")

# Préparer les lignes pour l'animation
lignes = [ax.plot([], [], color="red", alpha=0.7, linewidth=1)[0] for _ in trajets_valides_calcules]

# Fonction d'initialisation de l'animation
def init():
    for ligne in lignes:
        ligne.set_data([], [])
    return lignes

# Fonction de mise à jour de l'animation
def mettre_a_jour_trajets(frame):
    for i, chemin in enumerate(trajets_valides_calcules):
        num_nodes = min(frame, len(chemin))
        if num_nodes > 1:
            x, y = zip(*[(G.nodes[node]['x'], G.nodes[node]['y']) for node in chemin[:num_nodes]])
            lignes[i].set_data(x, y)
    return lignes

# Créer l'animation
max_duration = 150  # Durée d'animation par défaut
ani = FuncAnimation(fig, mettre_a_jour_trajets, frames=range(max_duration), init_func=init, blit=False, repeat=False)

# Sauvegarder l'animation sous forme de GIF
gif_path = "simulation_trajets.gif"
ani.save(gif_path, writer=PillowWriter(fps=15))  # Utiliser PillowWriter pour générer un GIF
print(f"La simulation a été sauvegardée sous forme de GIF : {gif_path}")
