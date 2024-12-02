import os
import osmnx as ox
import pandas as pd
import networkx as nx
from unidecode import unidecode
import json
import re
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
import random

# Charger les données
file_path = 'C:/Users/welma/HAX712X_Wahel/Projet_HAX712X/data/TAM_MMM_CoursesVelomagg.csv'
data = pd.read_csv(file_path)

# Convertir la colonne "Departure" en format datetime
data['Departure'] = pd.to_datetime(data['Departure'], errors='coerce')

# Demander à l'utilisateur de saisir une date au format 'YYYY-MM-DD'
date_str = input("Veuillez entrer une date (format YYYY-MM-DD) : ")

try:
    date_saisie = pd.to_datetime(date_str).date()  # Extraire uniquement la date
except ValueError:
    print("Format de date invalide.")
    exit()

# Filtrer les trajets en fonction de la date saisie (sans l'heure)
data_filtered = data[data['Departure'].dt.date == date_saisie].copy()

# Si aucun trajet n'a été trouvé pour cette date
if data_filtered.empty:
    print(f"Aucun trajet trouvé pour la date {date_saisie}.")
    exit()

# Fonction pour corriger les noms des stations
def corriger_nom_station(nom_station):
    if isinstance(nom_station, str):
        try:
            nom_station = nom_station.encode('latin1').decode('utf-8')
        except (UnicodeEncodeError, UnicodeDecodeError):
            print(f"Attention : encodage corrigé pour la station '{nom_station}'.")
            nom_station = unidecode(nom_station)
        nom_station = re.sub(r'^\d+\s*', '', nom_station).strip()
        nom_station = nom_station.replace("FacdesSciences", "Faculté des sciences")
        return nom_station
    return nom_station

# Appliquer la fonction de correction aux colonnes pertinentes
data_filtered['Departure station'] = data_filtered['Departure station'].apply(corriger_nom_station)
data_filtered['Return station'] = data_filtered['Return station'].apply(corriger_nom_station)

# Charger les coordonnées des stations depuis un fichier JSON
try:
    with open("station_coords.json", "r") as infile:
        coordonnees_stations = json.load(infile)
except FileNotFoundError:
    coordonnees_stations = {}

# Ajouter les coordonnées aux trajets
data_filtered['latitude_depart'] = data_filtered['Departure station'].map(lambda x: coordonnees_stations.get(x, {}).get('latitude'))
data_filtered['longitude_depart'] = data_filtered['Departure station'].map(lambda x: coordonnees_stations.get(x, {}).get('longitude'))
data_filtered['latitude_retour'] = data_filtered['Return station'].map(lambda x: coordonnees_stations.get(x, {}).get('latitude'))
data_filtered['longitude_retour'] = data_filtered['Return station'].map(lambda x: coordonnees_stations.get(x, {}).get('longitude'))

# Demander combien de trajets afficher
try:
    min_trajets = int(input("Combien de trajets voulez-vous afficher sur votre journée ? "))
    if min_trajets <= 0:
        raise ValueError("Le nombre de trajets doit être positif.")
except ValueError as ve:
    print(f"Erreur : {ve}")
    exit()

# Limiter à la taille du DataFrame filtré
min_trajets = min(min_trajets, len(data_filtered))
df = data_filtered.iloc[:min_trajets].dropna(subset=['latitude_depart', 'longitude_depart', 'latitude_retour', 'longitude_retour'])
df.reset_index(drop=True, inplace=True)

trajets_valides = len(df)
print(f"Nombre de trajets valides après filtrage : {trajets_valides}")

# Charger le réseau de Montpellier
G = ox.graph_from_place("Montpellier, France", network_type="all")

# Initialiser la figure pour l'animation avec un fond noir
fig, ax = plt.subplots(figsize=(12, 8))
fig.patch.set_facecolor('black')  # Fond noir pour la figure
ax.set_facecolor('black')         # Fond noir pour l'axe
ax.set_title("Trajets à Montpellier", color='white')
ax.set_xlabel("Longitude", color='white')
ax.set_ylabel("Latitude", color='white')

# Plot de la carte avec des couleurs adaptées au fond noir
ox.plot_graph(G, ax=ax, show=False, close=False, node_size=0, edge_color="white", edge_linewidth=0.5)

# Fonction pour calculer le chemin le plus court
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

# Calculer les chemins
chemins = [calcul_chemin_vélo(row) for _, row in df.iterrows()]
trajets_valides_calcules = [chemin for chemin in chemins if chemin is not None]
print(f"Nombre de trajets valides calculés : {len(trajets_valides_calcules)}")

# Créer des objets graphiques pour les points et les lignes
points = [ax.plot([], [], 'o', color='cyan')[0] for _ in trajets_valides_calcules]  # Points visibles sur fond noir
lignes = [ax.plot([], [], '-', color='white', linewidth=1)[0] for _ in trajets_valides_calcules]  # Lignes visibles

# Fonction d'initialisation de l'animation
def init():
    for point, ligne in zip(points, lignes):
        point.set_data([], [])
        ligne.set_data([], [])
    return points + lignes

# Fonction de mise à jour de l'animation
def mettre_a_jour_trajets(frame):
    for i, chemin in enumerate(trajets_valides_calcules):
        if frame < len(chemin):
            x_vals = [G.nodes[node]['x'] for node in chemin[:frame + 1]]
            y_vals = [G.nodes[node]['y'] for node in chemin[:frame + 1]]
            lignes[i].set_data(x_vals, y_vals)
            points[i].set_data([G.nodes[chemin[frame]]['x']], [G.nodes[chemin[frame]]['y']])
    return points + lignes

# Calculer le nombre total de frames basé sur le plus long trajet
max_frames = max(len(chemin) for chemin in trajets_valides_calcules)

# Créer l'animation
ani = FuncAnimation(fig, mettre_a_jour_trajets, frames=max_frames, init_func=init, blit=True, repeat=False)

# Sauvegarder l'animation sous forme de fichier MP4
mp4_path = "simulation_trajets_dynamique.mp4"
ani.save(mp4_path, writer=FFMpegWriter(fps=10))
print(f"La simulation a été sauvegardée sous forme de fichier MP4 : {mp4_path}")