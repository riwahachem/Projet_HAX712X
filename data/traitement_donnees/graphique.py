"""
Module pour analyser les trajets de vélos à Montpellier à partir d'un fichier CSV.

Ce script permet de charger un fichier CSV contenant des données de trajets, de les analyser, et de créer des visualisations graphiques des trajets par jour et par heure, en tenant compte de la pondération des trajets effectués entre 0h et 3h.

Etapes du traitement :
- Lecture du fichier CSV contenant les données des trajets.
- Conversion de la colonne 'Departure' en format datetime et extraction des informations sur la date, l'heure et le jour de la semaine.
- Pondération des trajets effectués entre 0h et 3h pour ajuster l'impact de ces trajets sur les analyses globales.
- Création d'un histogramme représentant le nombre total de trajets effectués chaque jour.
- Création d'un graphique en courbes représentant la répartition des trajets par jour de la semaine et par heure, avec une pondération.
- Sauvegarde des graphiques générés dans le dossier './images/'.

Entrée :
- Le chemin vers un fichier CSV contenant les données des trajets avec la colonne 'Departure' pour la date et l'heure du départ du trajet.

Sortie :
- Des graphiques sauvegardés dans le dossier './images/' :
- Un histogramme représentant le nombre de trajets par jour.
- Un graphique en courbes représentant la répartition des trajets par heure.
  
Le script crée automatiquement un dossier './images/' pour sauvegarder les graphiques si ce dossier n'existe pas déjà.

Dépendances :
- pandas
- matplotlib
- numpy
- os

Auteur : Wahel El Mazzouji
"""



import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

# Chemin du fichier de données unique
file_path = 'C:/Users/welma/HAX712X_Wahel/Projet_HAX712X/data/TAM_MMM_CoursesVelomagg.csv'

# Dossier de sortie pour les images
output_dir = './images/'
os.makedirs(output_dir, exist_ok=True)

# Fonction pour traiter et analyser les données
def analyse_trajets(file_path):
    # Charger les données
    df = pd.read_csv(file_path)
    
    # Convertir la colonne 'Departure' en datetime
    df['Departure'] = pd.to_datetime(df['Departure'])

    # Extraire la date, l'heure et le jour de la semaine
    df['Date'] = df['Departure'].dt.date
    df['Hour'] = df['Departure'].dt.hour
    df['DayOfWeek'] = df['Departure'].dt.dayofweek  # 0: Lundi, 6: Dimanche

    # Ajouter une colonne pondération pour ajuster les heures entre 0h-3h
    df['Weight'] = 1.0  # Initialiser en tant que float
    df.loc[df['Hour'].isin([0, 1, 2, 3]), 'Weight'] = 0.3  # Pondération réduite pour les trajets entre 0h et 3h

    # 1. Histogramme des trajets par jour
    trajets_par_jour = df.groupby('Date').size().reset_index(name='Nombre de trajets')
    plt.figure(figsize=(12, 6))
    plt.bar(trajets_par_jour['Date'], trajets_par_jour['Nombre de trajets'], 
            color='dodgerblue', alpha=0.8, edgecolor='navy')
    plt.title("Nombre total de trajets par jour", fontsize=16, fontweight='bold')
    plt.xlabel('Date', fontsize=14)
    plt.ylabel('Nombre de trajets', fontsize=14)
    plt.xticks(rotation=45, fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    histogram_path = os.path.join(output_dir, "Nb_trajets_par_jour.png")
    plt.savefig(histogram_path, dpi=300)
    plt.close()
    print(f"Histogramme sauvegardé sous : {histogram_path}")

    # 2. Graphique en courbes par jour et heure (avec pondération)
    df["weekday"] = df['DayOfWeek'].apply(lambda x: ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"][x])
    df_line = df.groupby(["weekday", "Hour"])["Weight"].sum().reset_index(name='Trajets pondérés')
    weekday_order = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]
    df_line['weekday'] = pd.Categorical(df_line['weekday'], categories=weekday_order, ordered=True)
    df_line = df_line.sort_values(['weekday', 'Hour'])
    
    # Création du graphique en courbes
    plt.figure(figsize=(12, 6))
    for jour in weekday_order:
        jour_data = df_line[df_line['weekday'] == jour]
        plt.plot(jour_data['Hour'], jour_data['Trajets pondérés'], label=jour, linewidth=2)
    plt.title("Répartition des trajets par jour et heure (pondéré)", fontsize=16, fontweight='bold')
    plt.xlabel('Heure de la journée', fontsize=14)
    plt.ylabel('Nombre de trajets pondérés', fontsize=14)
    plt.xticks(ticks=np.arange(0, 24, 1), labels=[f"{i}h" for i in range(24)], fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(alpha=0.5, linestyle='--')
    plt.legend(title="Jour de la semaine", loc='upper right', fontsize=10)
    plt.tight_layout()
    line_path = os.path.join(output_dir, "Graphique_trajets_repartition.png")
    plt.savefig(line_path, dpi=300)
    plt.close()
    print(f"Graphique en courbes sauvegardé sous : {line_path}")

# Appeler la fonction
analyse_trajets(file_path)
