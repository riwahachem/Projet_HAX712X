import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import os
import requests
import zipfile

# URL des fichiers
url_2022_2023 = "https://data.montpellier3m.fr/node/12668/download"  # Fichier ZIP contenant 2022 et 2023
url_2024 = "https://data.montpellier3m.fr/node/12468/download"       # Fichier CSV pour 2024

# Fonction pour charger un fichier CSV directement depuis une URL
def load_csv_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return pd.read_csv(io.BytesIO(response.content), low_memory=False)
    else:
        print(f"Erreur lors de l'accès au fichier : {url}")
        return None

# Fonction pour charger un fichier CSV depuis un ZIP via URL
def load_csv_from_zip(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
            if filename in zip_ref.namelist():
                with zip_ref.open(filename) as file:
                    return pd.read_csv(file, low_memory=False)
            else:
                print(f"Le fichier {filename} est manquant dans le ZIP.")
                return None
    else:
        print("Erreur lors de l'accès au fichier ZIP.")
        return None

# Charger les fichiers directement sans téléchargement local
df_2022 = load_csv_from_zip(url_2022_2023, 'TAM_MMM_CoursesVelomagg_2022.csv')
df_2023 = load_csv_from_zip(url_2022_2023, 'TAM_MMM_CoursesVelomagg_2023.csv')
df_2024 = load_csv_from_url(url_2024)

# Vérification des données chargées
#if df_2022 is not None:
    #print("Table 2022 chargée avec succès.")
#if df_2023 is not None:
    #print("Table 2023 chargée avec succès.")
#if df_2024 is not None:
    #print("Table 2024 chargée avec succès.")

# Fonction trajets_analys

def trajets_analys(df):
    try:
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
        #fig.write_image("nombre_trajets_par_jour.png")

    except KeyError as e:
        print(f"Erreur dans les colonnes : {e}")

# Exemple d'utilisation de trajets_analys
if df_2022 is not None:
    print("Analyse pour 2022 :")
    trajets_analys(df_2022)

if df_2023 is not None:
    print("Analyse pour 2023 :")
    trajets_analys(df_2023)

if df_2024 is not None:
    print("Analyse pour 2024 :")
    trajets_analys(df_2024)



