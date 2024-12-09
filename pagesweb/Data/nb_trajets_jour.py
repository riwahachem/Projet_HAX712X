import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import os
import requests
import zipfile

# Charger le fichier de données
url_2024="https://data.montpellier3m.fr/node/12468/download"
df_2024 = pd.read_csv(url_2024,low_memory=False)
# URL du fichier ZIP
url = "https://data.montpellier3m.fr/node/12668/download"

# Télécharger le fichier ZIP
response = requests.get(url)

# Vérifier si le téléchargement a réussi
if response.status_code == 200:
    # Sauvegarder le fichier ZIP localement
    zip_path = 'velomagg_data.zip'
    with open(zip_path, 'wb') as f:
        f.write(response.content)

    # Extraire le contenu du ZIP
    extract_path = 'velomagg_data'  # Dossier où extraire les fichiers
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

    #print(f"Fichier téléchargé et extrait dans {extract_path}")

    # Vérifier le contenu du dossier extrait
    files = os.listdir(extract_path)
    #print("Fichiers extraits:", files)

    # Charger les fichiers 2023 et 2022 (ajuste les noms de fichiers si nécessaire)
    df_2023_path = os.path.join(extract_path, 'TAM_MMM_CoursesVelomagg_2023.csv')
    df_2022_path = os.path.join(extract_path, 'TAM_MMM_CoursesVelomagg_2022.csv')
   

    # Vérifier si les fichiers existent avant de les charger
    if os.path.exists(df_2023_path) and os.path.exists(df_2022_path):
        # Charger les tables dans des DataFrames
        df_2023 = pd.read_csv(df_2023_path,low_memory=False)
        df_2022 = pd.read_csv(df_2022_path,low_memory=False)
        

        # Afficher les premières lignes pour vérifier
        #print("Table 2023:")
        #print(df_2023.head())
        #print("Table 2022:")
        #print(df_2022.head())
    else:
        print("Les fichiers CSV 2023 ou 2022 sont manquants.")
else:
    print("Erreur lors du téléchargement.")






def afficher_graphe(df):
# Convertir la colonne 'Departure' en type datetime 
   df['Departure'] = pd.to_datetime(df['Departure'], errors='coerce')

# Filtrer les lignes avec des dates valides
   df = df.dropna(subset=['Departure'])

# Ajouter une colonne pour les jours
   df['Day'] = df['Departure'].dt.date  # Extraire la date sans l'heure

# Calculer le nombre de trajets par jour
   daily_rides = df.groupby('Day').size().reset_index(name='Number of Rides')

# Statistiques descriptives
   print("\nStatistiques descriptives des trajets par jour:")
   print(daily_rides['Number of Rides'].describe())

# Créer un graphique interactif
   fig = px.bar(daily_rides, x='Day', y='Number of Rides', title='Nombre total de trajets par jour',
              labels={'Day': 'Jour', 'Number of Rides': 'Nombre de trajets'},
              text='Number of Rides')  # Affiche les valeurs sur les barres

   fig.update_layout(xaxis_title='Jour', yaxis_title='Nombre de trajets', showlegend=False)
   fig.show()
   fig.write_image("nombre_trajets_par_jour.png")

print("Année 2022")
print(afficher_graphe(df_2022))
print("Année 2023")
print(afficher_graphe(df_2023))
print("Année 2024")
print(afficher_graphe(df_2024))

