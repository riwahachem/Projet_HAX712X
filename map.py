import folium
import osmnx as ox
import pandas as pd
from geopy.geocoders import Nominatim

# Charger le fichier CSV
file_path = 'C:/Users/welma/HAX712X_Wahel/Projet_HAX712X/data/TAM_MMM_CoursesVelomagg.csv'
data = pd.read_csv(file_path)

# Nettoyage des noms de colonnes
data.columns = data.columns.str.strip()

# Extraire les noms uniques des stations de départ et de retour
stations = pd.concat([data['Departure station'], data['Return station']]).unique()

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
def afficher_route(depart, arrivee):
    # Géocoder les stations de départ et d'arrivée
    depart_coords = get_station_coord(depart)
    arrivee_coords = get_station_coord(arrivee)

    if depart_coords and arrivee_coords:
        # Trouver les nœuds les plus proches dans le graphe pour chaque station
        origin_node = ox.nearest_nodes(G, depart_coords[1], depart_coords[0])
        destination_node = ox.nearest_nodes(G, arrivee_coords[1], arrivee_coords[0])

        # Calculer la route
        route = ox.shortest_path(G, origin_node, destination_node)

        # Convertir la route en GeoDataFrame
        route_edges = ox.utils_graph.route_to_gdf(G, route)

        # Ajouter la route à la carte Folium
        folium.PolyLine(locations=[(point.xy[1][0], point.xy[0][0]) for point in route_edges.geometry], color="red", weight=5).add_to(m)

        # Ajouter des marqueurs pour la station de départ et d'arrivée
        folium.Marker(depart_coords, popup=f"Départ: {depart}").add_to(m)
        folium.Marker(arrivee_coords, popup=f"Arrivée: {arrivee}").add_to(m)

# Demander à l'utilisateur d'entrer les stations de départ et d'arrivée
station_depart = input("Entrez le nom de la station de départ: ")
station_arrivee = input("Entrez le nom de la station d'arrivée: ")

# Afficher la route entre les deux stations saisies
afficher_route(station_depart, station_arrivee)
# Compter le nombre d'arrêts uniques
nombre_arrets = len(stations)
print(f"Nombre d'arrêts uniques : {nombre_arrets}")


# Enregistrer la carte dans un fichier HTML
m.save('carte_velomagg_route.html')

print("Carte enregistrée sous 'carte_velomagg_route.html'. Ouvrez ce fichier pour voir la carte.")