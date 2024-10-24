import pandas as pd

# Charger le fichier CSV
file_path = 'C:/Users/welma/HAX712X_Wahel/Projet_HAX712X/TAM_MMM_CoursesVelomagg.csv'
donnees = pd.read_csv(file_path)

# Afficher les premières lignes pour avoir un aperçu de la structure des données
print("Aperçu des premières lignes du fichier :")
print(donnees.head())

# Afficher les colonnes disponibles
print("\nColonnes disponibles :")
print(donnees.columns)

# Résumé statistique pour les colonnes numériques
print("\nRésumé statistique des colonnes numériques :")
print(donnees.describe())

# Informations générales sur le fichier (types de colonnes, valeurs manquantes)
print("\nInformations sur les données :")
print(donnees.info())

# Analyser les valeurs manquantes
print("\nValeurs manquantes par colonne :")
print(donnees.isnull().sum())

# Stratégie pour gérer les valeurs manquantes :
# Option 1 : Imputer les valeurs manquantes avec une méthode adaptée (par ex: moyenne pour la température)
donnees['Departure temperature (°C)'].fillna(donnees['Departure temperature (°C)'].mean(), inplace=True)
donnees['Return temperature (°C)'].fillna(donnees['Return temperature (°C)'].mean(), inplace=True)

# Option 2 : Supprimer uniquement les lignes où des colonnes critiques sont vides (par exemple stations ou distances)
donnees = donnees.dropna(subset=['Departure station', 'Return station', 'Covered distance (m)', 'Duration (sec.)'])

# Supprimer les doublons si nécessaire
donnees = donnees.drop_duplicates()

# Si la colonne de température contient des dates, les transformer en datetime
# Je vais créer une colonne date depuis l'heure de départ si nécessaire
# Par exemple si tu as les heures dans d'autres colonnes, il faudrait les fusionner en date

# Extraction des colonnes essentielles pour ton projet
colonnes_essentielles = ['Departure station', 'Return station', 'Covered distance (m)', 'Duration (sec.)', 
                         'Departure temperature (°C)', 'Return temperature (°C)']
data_essentiel = donnees[colonnes_essentielles]

print("\nColonnes essentielles extraites :")
print(data_essentiel.head())

# Visualisation de base : Distribution des distances et des durées
import matplotlib.pyplot as plt
import seaborn as sns

# Distribution des distances
plt.figure(figsize=(10, 5))
sns.histplot(data_essentiel['Covered distance (m)'], bins=30, kde=True)
plt.title('Distribution des distances couvertes')
plt.xlabel('Distance (m)')
plt.ylabel('Nombre de trajets')
plt.show()

# Distribution des durées
plt.figure(figsize=(10, 5))
sns.histplot(data_essentiel['Duration (sec.)'], bins=30, kde=True)
plt.title('Distribution des durées des trajets')
plt.xlabel('Durée (secondes)')
plt.ylabel('Nombre de trajets')
plt.show()

# Distribution des températures de départ
plt.figure(figsize=(10, 5))
sns.histplot(data_essentiel['Departure temperature (°C)'], bins=20, kde=True)
plt.title('Distribution des températures de départ')
plt.xlabel('Température (°C)')
plt.ylabel('Nombre de trajets')
plt.show()
