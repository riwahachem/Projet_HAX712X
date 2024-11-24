import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px


# Charger le fichier de données 
df = pd.read_csv("C:\\Users\\Clara\\Desktop\\dossier Projet\\TAM_MMM_CoursesVelomagg.csv")
print(df)

# Convertir la colonne 'Departure' en type datetime (ajuste le nom de la colonne si nécessaire)
df['Departure'] = pd.to_datetime(df['Departure'], errors='coerce')

# Filtrer les lignes avec des dates valides
df = df.dropna(subset=['Departure'])

# Ajouter une colonne pour les jours
df['Day'] = df['Departure'].dt.date  # Extraire la date sans l'heure

# Calculer le nombre de trajets par jour
daily_rides = df.groupby('Day').size().reset_index(name='Number of Rides')

# Créer un graphique interactif
fig = px.bar(daily_rides, x='Day', y='Number of Rides', title='Nombre total de trajets par jour',
             labels={'Day': 'Jour', 'Number of Rides': 'Nombre de trajets'},
             text='Number of Rides')  # Affiche les valeurs sur les barres

fig.update_layout(xaxis_title='Jour', yaxis_title='Nombre de trajets', showlegend=False)
fig.show()

# Créer les variables d'entraînement pour le modèle
trajets_par_jour['Jour_precedent'] = trajets_par_jour['Nombre_de_trajets'].shift(1)
trajets_par_jour.dropna(inplace=True)"""

