import pooch
print(pooch.__version__)
import pandas as pd

# Définir le chemin vers le répertoire où on souhaite stocker les fichiers
data_dir = pooch.os_cache("dataset")  # utiliser un cache pour stocker les fichiers

# Dictionnaire avec les fichiers et leurs URL
files = {
    "TAM_MMM_CoursesVelomagg.csv": "https://data.montpellier3m.fr/node/12468/TAM_MMM_CoursesVelomagg.csv",
    #"table2.csv": "https://   .csv",  
    #"table3.csv": "https://   .csv",  # 
}

# Télécharger les fichiers si nécessaire
for filename, url in files.items():
    pooch.retrieve(
        url,                # L'URL du fichier
        fname=filename,     # Nom du fichier pour le stocker
        path=data_dir / filename,     # Où le stocker (dans le cache)
        known_hash=None,
    )



# Charger les données dans des DataFrames
data_courses_velomagg = pd.read_csv(pooch.retrieve("TAM_MMM_CoursesVelomagg.csv", base_dir=data_dir))
  #data_table2 = pd.read_csv(pooch.retrieve("table2.csv", base_dir=data_dir))
  #data_table3 = pd.read_csv(pooch.retrieve("table3.csv", base_dir=data_dir))

# Afficher les premières lignes des DataFrames pour vérifier
print(data_courses_velomagg.head())
#print(data_table2.head())
#print(data_table3.head())