import pandas as pd

def charger_donnees():
    fichiers = [
        'TAM_MMM_CoursesVelomagg_2022.csv',
        'TAM_MMM_CoursesVelomagg_2023.csv',
        'TAM_MMM_CoursesVelomagg.csv'  # Fichier pour 2024
    ]
    dataframes = {fichier.split('_')[-1].split('.')[0]: pd.read_csv(fichier) for fichier in fichiers}
    return dataframes

def nettoyer_donnees(df: pd.DataFrame) -> pd.DataFrame:
    df['Departure'] = pd.to_datetime(df['Departure'], errors='coerce')
    df['Return'] = pd.to_datetime(df['Return'], errors='coerce')
    df.dropna(subset=['Departure', 'Return'], inplace=True)  # Supprime les lignes avec des valeurs manquantes
    return df

def filtrer_par_periode(df: pd.DataFrame, periode: str) -> pd.DataFrame:
    df['Departure'] = pd.to_datetime(df['Departure'], errors='coerce')  # Convertit les dates
    maintenant = pd.Timestamp.now()
    if periode == 'mois':
        return df[df['Departure'] >= (maintenant - pd.DateOffset(months=1))]
    elif periode == 'annee':
        return df[df['Departure'] >= (maintenant - pd.DateOffset(years=1))]
    elif periode == 'tout':
        return df.copy()  # Retourne toutes les données
    else:
        raise ValueError("Période non valide. Choisissez 'mois', 'annee' ou 'tout'.")
    
def obtenir_statistiques_descriptives(df: pd.DataFrame) -> pd.DataFrame:
        return df[['Covered distance (m)', 'Duration (sec.)']].describe()
    
def prevoir_trafic_jour_suivant(df: pd.DataFrame) -> pd.DataFrame:
    moyenne_journaliere = df.groupby(df['Departure'].dt.date).size().mean()
    return pd.DataFrame({'Prevision trafic': [moyenne_journaliere]}, index=[pd.Timestamp.now().date() + pd.DateOffset(days=1)])


# Charger les données
dataframes = charger_donnees()

# Tester la fonction sur les données chargées
for annee, df in dataframes.items():
    print(f"Statistiques descriptives pour {annee}:")
    print(obtenir_statistiques_descriptives(df))
    print("\n")

# Filtrer les données par mois ou par année et afficher les résultats
for annee, df in dataframes.items():
    print(f"Filtrage des données pour l'année {annee}:")
    
     #Filtrer les données du dernier mois
    donnees_filtrees_mois = filtrer_par_periode(df, 'mois')
    print("Données filtrées pour le dernier mois:")
    print(donnees_filtrees_mois.head())  # Afficher les premières lignes pour vérification
    
    # Filtrer les données de la dernière année
    donnees_filtrees_annee = filtrer_par_periode(df, 'annee')
    print("Données filtrées pour la dernière année:")
    print(donnees_filtrees_annee.head())
    
    print("\n")





