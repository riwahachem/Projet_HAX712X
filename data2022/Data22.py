import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# Charger le fichier de données 
chemin_fichier =  r'C:\Users\Clara\Desktop\dossier Projet\TAM_MMM_CoursesVelomagg.csv' 
df = pd.read_csv(chemin_fichier)

# Nettoyer et convertir les dates
df['Departure'] = pd.to_datetime(df['Departure'], errors='coerce')
df['Return'] = pd.to_datetime(df['Return'], errors='coerce')
df.dropna(subset=['Covered distance (m)', 'Duration (sec.)', 'Departure', 'Return'], inplace=True)

# Calculer les statistiques descriptives
statistiques_descriptives = df[['Covered distance (m)', 'Duration (sec.)']].describe()
print("Statistiques descriptives :")
print(statistiques_descriptives)
display(statistiques_descriptives)  # Utiliser display pour afficher les résultats

# Visualisation avec un swarm plot
print("figure ")
plt.figure(figsize=(12, 6))
sns.stripplot(x='Covered distance (m)', y='Duration (sec.)', data=df.sample(500), alpha=0.7)
plt.title('Swarm Plot de la Durée des Trajets par Distance Parcourue')
plt.xlabel('Distance Parcourue (m)')
plt.ylabel('Durée (sec.)')
plt.grid(True)
plt.show()
