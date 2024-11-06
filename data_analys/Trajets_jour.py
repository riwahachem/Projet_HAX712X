import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
#packages pour la prédiction...
#from sklearn.model_selection import train_test_split
#from sklearn.linear_model import LinearRegression
#from sklearn.metrics import r2_score


# Charger le fichier de données 
chemin_fichier =  r'TAM_MMM_CoursesVelomagg.csv' 
df = pd.read_csv(chemin_fichier)

# Nettoyer et convertir les dates
df['Departure'] = pd.to_datetime(df['Departure'], errors='coerce')
df.dropna(subset=['Departure'], inplace=True)
df['Return'] = pd.to_datetime(df['Return'], errors='coerce')
df.dropna(subset=['Covered distance (m)', 'Duration (sec.)', 'Departure', 'Return'], inplace=True)

# Entrer une date et afficher les trajets correspendant à cette date.
# Demander à l'utilisateur d'entrer une date
date_input = input("Veuillez entrer une date (format AAAA-MM-JJ) pour voir les trajets de cette journée : ")

# Filtrer le DataFrame pour obtenir les trajets correspondant à la date saisie
date_filter = pd.to_datetime(date_input, errors='coerce')
if date_filter is not pd.NaT:
    trajets_date = df[df['Departure'].dt.date == date_filter.date()]
    if trajets_date.empty:
        print(f"Aucun trajet trouvé pour le {date_input}.")
    else:
        print(f"Trajets effectués le {date_input} :")
        print(trajets_date[['Departure', 'Return', 'Covered distance (m)', 'Duration (sec.)']])
else:
    print("La date saisie est invalide. Veuillez entrer une date au format AAAA-MM-JJ.")



# Calculer les statistiques descriptives
statistiques_descriptives = df[['Covered distance (m)', 'Duration (sec.)']].describe()
print("Statistiques descriptives :")
print(statistiques_descriptives)


"""# Visualisation avec un swarm plot
print("figure ")
plt.figure(figsize=(12, 6))
sns.stripplot(x='Covered distance (m)', y='Duration (sec.)', data=df.sample(500), alpha=0.7)
plt.title('Swarm Plot de la Durée des Trajets par Distance Parcourue')
plt.xlabel('Distance Parcourue (m)')
plt.ylabel('Durée (sec.)')
plt.grid(True)
plt.show()"""

# Limiter l'échantillon pour améliorer la lisibilité
sample_df = df.sample(500, random_state=42)

# Créer le plot
plt.figure(figsize=(12, 8))
sns.stripplot( 
    x='Covered distance (m)', 
    y='Duration (sec.)', 
    data=sample_df, 
    #hue='Festive Color',
    palette=colors,
    alpha=0.7, 
    size=5,  # Taille de base des points
    jitter=0.5,
    legend =False   # Jitter horizontal pour espacer les points
)

# Déco du plot
plt.title('Durée des Trajets par Distance Parcourue')
plt.xlabel('Distance Parcourue (m)')
plt.ylabel('Durée (sec.)')
plt.grid(True, linestyle='--', alpha=0.3)

plt.show()

"""# Créer une nouvelle colonne avec seulement la date (sans heure)
df['Date'] = df['Departure'].dt.date

#prédire le nombre de trajets pour le jour suivant
# Calculer le nombre de trajets par jour
trajets_par_jour = df.groupby('Date').size().reset_index(name='Nombre_de_trajets')

# Créer les variables d'entraînement pour le modèle
trajets_par_jour['Jour_precedent'] = trajets_par_jour['Nombre_de_trajets'].shift(1)
trajets_par_jour.dropna(inplace=True)"""

