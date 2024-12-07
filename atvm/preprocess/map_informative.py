"""
Module pour la génération d'une carte interactive des stations de vélos à Montpellier.

Ce script crée une carte interactive de la ville de Montpellier en utilisant la bibliothèque Folium.
Il récupère les informations géographiques de la ville via OpenStreetMap (OSM) et les stations de vélos
via l'API de la ville de Montpellier. Les stations de vélos sont affichées avec des marqueurs contenant
des informations sur la disponibilité des vélos et des places de stationnement.

Le processus comprend les étapes suivantes :
- Récupération des coordonnées géographiques de Montpellier et du polygone des limites de la ville.
- Création d'une carte centrée sur Montpellier avec les limites de la ville tracées sous forme de polygone.
- Récupération des données JSON des stations de vélos via une API externe et sauvegarde dans un fichier.
- Ajout de marqueurs sur la carte pour chaque station de vélos, incluant des informations détaillées dans un popup.
- Sauvegarde de la carte résultante sous forme de fichier HTML pour affichage dans un navigateur.

Dépendances :
- osmnx
- folium
- requests
- json

Auteur : Wahel El Mazzouji
"""
import osmnx as ox
import folium
import requests
import json

# Définir l'endroit
ville = "Montpellier, France"

# Récupérer le polygone des limites de Montpellier
frontiere = ox.geocode_to_gdf(ville)

# Obtenir les coordonnées du centre de Montpellier
location = ox.geocode(ville)

# Créer une carte Folium centrée sur Montpellier
m = folium.Map(location=location, zoom_start=14)

# Extraire les coordonnées des limites de la ville pour tracer un polygone
coords = frontiere.geometry.values[0].exterior.coords[:]
folium.Polygon(
    locations=[(lat, lon) for lon, lat in coords],  # (lat, lon)
    color='black',
    fill=False,
    weight=2.5,  # Épaisseur de la bordure
).add_to(m)

# URL de l'API pour récupérer les données des stations de vélos à Montpellier
url = "https://portail-api-data.montpellier3m.fr/bikestation?limit=1000"
response = requests.get(url, headers={"accept": "application/json"})

# Vérifier si la requête a réussi
if response.status_code == 200:
    data = response.json()  # Extraire les données JSON
    
    # Sauvegarder les données dans un fichier JSON pour une utilisation future
    with open("stations_velo.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    
    # Charger les données depuis le fichier JSON pour afficher les informations
    with open("stations_velo.json", "r", encoding="utf-8") as file:
        data = json.load(file)

# Ajouter des marqueurs pour les stations de vélos
for station in data:
    # Extraire l'adresse, les vélos disponibles et les places libres
    address = station['address']['value']['streetAddress']
    velo_present = station['availableBikeNumber']['value']
    places_libres = station['freeSlotNumber']['value']
    
    # Créer le texte pour le popup
    popup_text = f"""
    <div style="font-size: 14px; font-weight: bold;">
        <p><b>Station:</b> {address}</p>
        <p><b>Vélos disponibles:</b> {velo_present}</p>
        <p><b>Places libres:</b> {places_libres}</p>
    </div>
    """
    
    # Extraire les coordonnées de chaque station
    coords = station['location']['value']['coordinates']
    
    # Ajouter un marqueur avec ces informations dans le popup
    folium.Marker(
        location=(coords[1], coords[0]),  # (lat, lon)
        popup=folium.Popup(popup_text, max_width=300),
        icon=folium.Icon(color='blue', icon='info-sign')  # Tous les marqueurs en bleu
    ).add_to(m)

# Sauvegarder la carte dans un fichier HTML
m.save('montpellier_bike_stations_same_color.html')

# Message pour confirmer que la carte est prête
print("La carte a été sauvegardée sous 'montpellier_bike_stations_same_color.html'. Ouvrez ce fichier dans votre navigateur.")
