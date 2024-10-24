import folium
import osmnx as ox
import pandas as pd
from geopy.geocoders import Nominatim

# Charger le fichier CSV
file_path = 'C:/Users/welma/HAX712X_Wahel/Projet_HAX712X/data/TAM_MMM_CoursesVelomagg.csv'
data = pd.read_csv(file_path)

# Nettoyage des noms de colonnes
data.columns = data.columns.str.strip()

# Vérifier les colonnes du fichier
print("Colonnes du fichier :", data.columns)

# Afficher les dates uniques disponibles dans la colonne 'Departure' (extraction de la date sans l'heure)
if 'Departure' in data.columns:
    dates_disponibles = pd.to_datetime(data['Departure']).dt.date.unique()  # Extraire juste les dates (sans l'heure)
    print("Dates disponibles :")
    for date in dates_disponibles:
        print(date)
else:
    print("La colonne 'Departure' n'existe pas dans le fichier CSV.")
    exit()

# Demander à l'utilisateur de choisir une date parmi les disponibles
date_choisie = input("Entrez une date parmi les dates disponibles (format YYYY-MM-DD) : ")

# Vérifier que la date choisie est bien dans les dates disponibles
try:
    date_choisie = pd.to_datetime(date_choisie).date()  # Convertir la date saisie en format date
except ValueError:
    print("Format de date incorrect. Veuillez entrer une date au format YYYY-MM-DD.")
    exit()

if date_choisie not in dates_disponibles:
    print(f"La date {date_choisie} n'est pas dans les dates disponibles.")
    exit()

# Initialiser le géocodeur
geolocator = Nominatim(user_agent="velomagg")

# Créer une carte Folium centrée sur Montpellier
m = folium.Map(location=[43.6119, 3.8772], zoom_start=13)

# Créer un graphe des rues de Montpellier
G = ox.graph_from_place('Montpellier, France', network_type='bike')

# Fonction pour obtenir les coordonnées d'une station
def get_station_coord(station_name):
    try:
        loc = geolocator.geocode(f"{station_name}, Montpellier, France")
        if loc:
            return (loc.latitude, loc.longitude)
        else:
            return None
    except Exception as e:
        print(f"Erreur lors du géocodage de {station_name}: {e}")
        return None

# Calculer et afficher la route entre deux stations
def afficher_route(depart_coords, arrivee_coords, depart, arrivee):
    if depart_coords and arrivee_coords:
        try:
            # Trouver les nœuds les plus proches dans le graphe pour chaque station
            origin_node = ox.nearest_nodes(G, depart_coords[1], depart_coords[0])
            destination_node = ox.nearest_nodes(G, arrivee_coords[1], arrivee_coords[0])

            # Calculer la route
            route = ox.shortest_path(G, origin_node, destination_node)

            if not route:
                print(f"Aucune route trouvée entre {depart} et {arrivee}.")
                return

            # Convertir la route en GeoDataFrame
            route_edges = ox.utils_graph.routing.route_to_gdf(G, route)

            # Ajouter la route à la carte Folium
            folium.PolyLine(locations=[(point.xy[1][0], point.xy[0][0]) for point in route_edges.geometry], color="red", weight=5).add_to(m)

            # Ajouter des marqueurs pour la station de départ et d'arrivée
            folium.Marker(depart_coords, popup=f"Départ: {depart}").add_to(m)
            folium.Marker(arrivee_coords, popup=f"Arrivée: {arrivee}").add_to(m)
        
        except ValueError as e:
            print(f"Erreur lors du calcul de la route entre {depart} et {arrivee}: {e}")

# Filtrer les trajets pour la date choisie
trajets = data[pd.to_datetime(data['Departure']).dt.date == date_choisie]

if trajets.empty:
    print(f"Aucun trajet trouvé pour la date {date_choisie}.")
else:
    print(f"{len(trajets)} trajets trouvés pour la date {date_choisie}.")

    # Boucler sur les trajets trouvés
    for index, trajet in trajets.iterrows():
        station_depart = trajet['Departure station']
        station_arrivee = trajet['Return station']

        depart_coords = get_station_coord(station_depart)
        arrivee_coords = get_station_coord(station_arrivee)

        if depart_coords and arrivee_coords:
            afficher_route(depart_coords, arrivee_coords, station_depart, station_arrivee)

# Enregistrer la carte dans un fichier HTML
m.save('carte_velomagg_route.html')

print("Carte enregistrée sous 'carte_velomagg_route.html'. Ouvrez ce fichier pour voir la carte.")
