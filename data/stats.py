import pandas as pd

#Charge le fichier CSV contenant les données des trajets.
def charger_donnees(file_path):
    return pd.read_csv(file_path).dropna()

def corriger_encodage(station_name):
    try:
        return station_name.encode('latin1').decode('utf-8')
    except UnicodeEncodeError as e:
        print(f"Erreur d'encodage pour {station_name}: {e}")
        return station_name

#Corrige les adresses des stations en nettoyant les caractères.
def corriger_adresses(data):
    data['Departure station'] = data['Departure station'].apply(corriger_encodage)
    data['Return station'] = data['Return station'].apply(corriger_encodage)
    return data

#Calcule les statistiques sur les trajets.
def calculer_statistiques(trajets):
    distance_totale = trajets['Covered distance (m)'].sum() / 1000  # Convertir en km
    temps_total = trajets['Duration (sec.)'].sum() / 60  # Convertir en minutes
    nombre_de_trajets = len(trajets)
    
    distance_moyenne = trajets['Covered distance (m)'].mean() / 1000 if nombre_de_trajets > 0 else 0  # Convertir en km
    temps_moyen = trajets['Duration (sec.)'].mean() / 60 if nombre_de_trajets > 0 else 0  # Convertir en minutes
    
    return {
        "Distance totale": distance_totale,
        "Distance moyenne": distance_moyenne,
        "Temps total": temps_total,
        "Temps moyen": temps_moyen,
        "Nombre total de trajets": nombre_de_trajets
    }

# Retourne le nombre de trajets par station de départ.
def trajets_par_station(trajets):
    return trajets.groupby('Departure station').size()

# Retourne le nombre de trajets par jour.
def trajets_par_jour(trajets):
    trajets['Date'] = pd.to_datetime(trajets['Departure']).dt.date
    return trajets.groupby('Date').size()


# Affiche les statistiques calculées.
def afficher_statistiques(stats):
    print("\n--- Statistiques des Trajets ---")
    for key, value in stats.items():
        print(f"{key}: {value:.2f} {'km' if 'Distance' in key else 'minutes' if 'Temps' in key else ''}")


# Affiche les dates disponibles et permet à l'utilisateur de choisir une date.
def choisir_date(data):
    dates_disponibles = data['Departure'].str[:10].unique()  # Extraire les dates uniques
    print("\nDates disponibles :")
    for date in dates_disponibles:
        print(f"- {date}")

    while True:
        date_choisie = input("Veuillez choisir une date (YYYY-MM-DD) : ")
        if date_choisie in dates_disponibles:
            return date_choisie
        else:
            print("Date invalide, veuillez réessayer.")


# Affiche le nombre de trajets par station de départ.
def afficher_nombre_trajets_par_station(trajets):
    print("\n--- Nombre de Trajets par Station de Départ ---")
    trajets_par_station_resultat = trajets_par_station(trajets)
    print(trajets_par_station_resultat)


# Affiche le nombre de trajets par jour.
def afficher_nombre_trajets_par_jour(trajets):
    print("\n--- Nombre de Trajets par Jour ---")
    trajets_par_jour_resultat = trajets_par_jour(trajets)
    print(trajets_par_jour_resultat)

def main():
    # Chemin vers le fichier CSV
    file_path = 'C:/Users/welma/HAX712X_Wahel/Projet_HAX712X/data/TAM_MMM_CoursesVelomagg.csv'
    
    # Charger les données
    data = charger_donnees(file_path)
    data = corriger_adresses(data)

    while True:
        # Choisir une date
        date_choisie = choisir_date(data)
        trajets_du_jour = data[data['Departure'].str.startswith(date_choisie)]

        # Calculer les statistiques
        stats = calculer_statistiques(trajets_du_jour)
        afficher_statistiques(stats)

        # Choix de l'utilisateur pour afficher des statistiques supplémentaires
        while True:
            choix = input("\nSouhaitez-vous afficher le nombre de trajets par station (1), par jour (2) ou quitter (q) ? ")
            if choix == '1':
                afficher_nombre_trajets_par_station(trajets_du_jour)
            elif choix == '2':
                afficher_nombre_trajets_par_jour(trajets_du_jour)
            elif choix.lower() == 'q':
                print("Merci d'avoir utilisé le programme ! À bientôt.")
                return
            else:
                print("Choix invalide, veuillez réessayer.")

if __name__ == "__main__":
    main()
