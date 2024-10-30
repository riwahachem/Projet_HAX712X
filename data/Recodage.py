import pandas as pd
# Charger le fichier CSV
file_path = 'C:/Users/welma/HAX712X_Wahel/Projet_HAX712X/data/TAM_MMM_CoursesVelomagg.csv'
data = pd.read_csv(file_path)
# Fonction pour réparer les caractères mal encodés
def corriger_encodage(station_name):
    try:
        # D'abord on encode en bytes avec l'encodage latin1, puis on décode en utf-8
        return station_name.encode('latin1').decode('utf-8')
    except UnicodeEncodeError as e:
        # En cas de problème d'encodage, on affiche un message et retourne le nom original
        print(f"Erreur d'encodage pour {station_name}: {e}")
        return station_name

# Exemple d'utilisation
noms_de_stations = ["PÃ©rols Etang de l'Or", "PrÃ©s d'ArÃ¨nes", 'ComÃ©die']
for nom in noms_de_stations:
    print(f"Avant : {nom}, Après : {corriger_encodage(nom)}")
