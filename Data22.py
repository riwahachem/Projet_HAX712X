import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# Charger le fichier de données de 2022
chemin_fichier =  r'C:\Users\Clara\Desktop\dossier Projet\TAM_MMM_CoursesVelomagg_2022.csv' 
df_2022 = pd.read_csv(chemin_fichier)

# Nettoyer et convertir les dates
df_2022['Departure'] = pd.to_datetime(df_2022['Departure'], errors='coerce')
df_2022['Return'] = pd.to_datetime(df_2022['Return'], errors='coerce')
df_2022.dropna(subset=['Covered distance (m)', 'Duration (sec.)', 'Departure', 'Return'], inplace=True)

# Calculer les statistiques descriptives
statistiques_descriptives = df_2022[['Covered distance (m)', 'Duration (sec.)']].describe()
print("Statistiques descriptives pour l'année 2021 :")
print(statistiques_descriptives)
display(statistiques_descriptives)  # Utiliser display pour afficher les résultats

# Visualisation avec un swarm plot
print("figure ")
plt.figure(figsize=(12, 6))
sns.stripplot(x='Covered distance (m)', y='Duration (sec.)', data=df_2022.sample(500), alpha=0.7)
plt.title('Swarm Plot de la Durée des Trajets par Distance Parcourue (2022)')
plt.xlabel('Distance Parcourue (m)')
plt.ylabel('Durée (sec.)')
plt.grid(True)
plt.show()