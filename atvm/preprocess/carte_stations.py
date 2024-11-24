#%%
import osmnx as ox
import folium
import os

output_path = os.path.join(os.path.dirname(__file__), "../../pagesweb/Video/map_stations.html")

montpellier = "Montpellier, France"

stations_velo = ox.geometries_from_place(montpellier, tags={'amenity': 'bicycle_rental'})

frontiere = ox.geocode_to_gdf(montpellier)

coord = ox.geocode(montpellier)

# Créer une carte Folium
m = folium.Map(location=coord, zoom_start=12)

# Marquer les stations de vélo
for _, station in stations_velo.iterrows():
    if station.geometry.geom_type == "Point": 
        coords = station.geometry.coords[0]
        station_name = station.get('name', 'Station de vélo sans nom')
        folium.CircleMarker(
            location=(coords[1], coords[0]), 
            radius=6,
            color='blue',
            fill=True,
            fill_color='cyan',
            fill_opacity=0.7,
            popup=f"Vélo : {station_name}" 
        ).add_to(m)

# Tracer les limites de Montpellier
coords = frontiere.geometry.values[0].exterior.coords[:]
folium.Polygon(
    locations=[(lat, lon) for lon, lat in coords],  
    color='black',
    fill=False,
    weight=2.5,
).add_to(m)

m.save(output_path)
# %%
