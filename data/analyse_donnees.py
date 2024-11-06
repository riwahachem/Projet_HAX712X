import pandas as pd
#J'ai chargé toutes les dataframes pour les analyser
file_path = "C:/Users/welma/HAX712X_Wahel/Projet_HAX712X/data/TAM_MMM_CoursesVelomagg.csv"
#file_path = "C:/Users/welma/HAX712X_Wahel/Projet_HAX712X/data/MMM_MMM_GeolocCompteurs(1).csv"
#file_path = "C:/Users/welma/HAX712X_Wahel/Projet_HAX712X/data/TAM_MMM_CoursesVelomagg_2021.csv"
#file_path = "C:/Users/welma/HAX712X_Wahel/Projet_HAX712X/data/TAM_MMM_CoursesVelomagg_2022.csv"
# Je charge le fichier CSV
donnees = pd.read_csv(file_path)
# J'affiche les premieres lignes du fichier pour examiner la structure des donnees
print(donnees.head())
# J'affiche les colonnes disponibles
print(donnees.columns)
# Je supprime les lignes avec des valeurs manquantes
new_donnees = donnees.dropna()
# Je supprime les doublons si nécessaire
new_donnees = new_donnees.drop_duplicates()

#print(donnees['Departure'])
