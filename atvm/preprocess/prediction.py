#%%
''' éxécution préliminaire '''
import pandas as pd
import copy 
import json
import osmnx as ox
import folium
import networkx as nx
from geopy.geocoders import Nominatim
import time
import re 
from unidecode import unidecode
import os

# Chemin vers le fichier CSV
file_path =  os.path.abspath(os.path.join(os.path.dirname(__file__),'../data_atvm/TAM_MMM_CoursesVelomagg.csv'))
data = pd.read_csv(file_path)

# Correction des noms de stations
def corriger_encodage(station_name):
    if isinstance(station_name, str):
        try:
            station_name = station_name.encode('latin1').decode('utf-8')
        except (UnicodeEncodeError, UnicodeDecodeError):
            station_name = unidecode(station_name)
        station_name = re.sub(r'^\d+\s*', '', station_name).strip()  # Supprime les numéros en début
        return station_name
    return station_name

data['Departure station'] = data['Departure station'].apply(corriger_encodage)
data['Return station'] = data['Return station'].apply(corriger_encodage)

# Extraction des stations uniques corrigées
stations_uniques = pd.concat([data['Departure station'], data['Return station']]).unique()
stations_uniques = [station for station in stations_uniques if isinstance(station, str)]
stations_uniques = [station.replace("FacdesSciences", "Faculté des sciences") for station in stations_uniques]

# Initialiser le géocodeur et charger le JSON existant
geolocator = Nominatim(user_agent="velomagg_locator")
try:
    with open("station_coords.json", "r") as infile:
        coordonnees_stations = json.load(infile)
except FileNotFoundError:
    coordonnees_stations = {}
    
def get_station_coordinates(station_name):
    if not isinstance(station_name, str):
        return None
    options = [
        f"{station_name}, Montpellier, France",
        f"{station_name.replace('-', ' ')}, Montpellier, France",
        f"{station_name.split('-')[0]}, Montpellier, France",
        f"{station_name.split('-')[-1]}, Montpellier, France",
        f"{station_name}, France"
    ]
    if "Fac" in station_name:
        options.append(station_name.replace("Fac", "Faculté") + ", Montpellier, France")

    for query in options:
        try:
            location = geolocator.geocode(query)
            if location:
                return {"latitude": location.latitude, "longitude": location.longitude}
        except Exception as e:
            print(f"Erreur pour {query}: {e}")
        time.sleep(1)
    return None

# Boucle pour obtenir et sauvegarder les coordonnées
for station in stations_uniques:
    if station not in coordonnees_stations:
        coords = get_station_coordinates(station)
        if coords:
            coordonnees_stations[station] = coords
            print(f"Coordonnées trouvées pour {station}: {coords}")
        else:
            print(f"Coordonnées non trouvées pour {station}")
        
        # Sauvegarde en cours de traitement
        with open("station_coords.json", "w") as outfile:
            json.dump(coordonnees_stations, outfile)
        time.sleep(1)  # Pause pour éviter les limites de requêtes

#%%
''' création des fonctions permettants d'obtenir toutes les données utiles '''


filename =  os.path.abspath(os.path.join(os.path.dirname(__file__),'../data_atvm/TAM_MMM_CoursesVelomagg.csv'))

archives=['data_atvm/donnees_EcoCompt/MMM_EcoCompt_ED223110495_archive.json','data_atvm/donnees_EcoCompt/MMM_EcoCompt_ED223110496_archive.json','data_atvm/donnees_EcoCompt/MMM_EcoCompt_ED223110497_archive.json',
           'data_atvm/donnees_EcoCompt/MMM_EcoCompt_ED223110500_archive.json','data_atvm/donnees_EcoCompt/MMM_EcoCompt_ED223110501_archive.json','data_atvm/donnees_EcoCompt/MMM_EcoCompt_X2H19070220_archive.json',
           'data_atvm/donnees_EcoCompt/MMM_EcoCompt_X2H20042632_archive.json','data_atvm/donnees_EcoCompt/MMM_EcoCompt_X2H20042633_archive.json','data_atvm/donnees_EcoCompt/MMM_EcoCompt_X2H20042634_archive.json',
           'data_atvm/donnees_EcoCompt/MMM_EcoCompt_X2H20042635_archive.json','data_atvm/donnees_EcoCompt/MMM_EcoCompt_X2H20063161_archive.json','data_atvm/donnees_EcoCompt/MMM_EcoCompt_X2H20063162_archive.json',
           'data_atvm/donnees_EcoCompt/MMM_EcoCompt_X2H20063163_archive.json','data_atvm/donnees_EcoCompt/MMM_EcoCompt_X2H20063164_archive.json','data_atvm/donnees_EcoCompt/MMM_EcoCompt_X2H20104132_archive.json',
           'data_atvm/donnees_EcoCompt/MMM_EcoCompt_X2H21070341_archive.json','data_atvm/donnees_EcoCompt/MMM_EcoCompt_X2H21070342_archive.json','data_atvm/donnees_EcoCompt/MMM_EcoCompt_X2H21070343_archive.json',
           'data_atvm/donnees_EcoCompt/MMM_EcoCompt_X2H21070344_archive.json','data_atvm/donnees_EcoCompt/MMM_EcoCompt_X2H21070345_archive.json','data_atvm/donnees_EcoCompt/MMM_EcoCompt_X2H21070346_archive.json',
           'data_atvm/donnees_EcoCompt/MMM_EcoCompt_X2H21070347_archive.json','data_atvm/donnees_EcoCompt/MMM_EcoCompt_X2H21070348_archive.json','data_atvm/donnees_EcoCompt/MMM_EcoCompt_X2H21070349_archive.json',
           'data_atvm/donnees_EcoCompt/MMM_EcoCompt_X2H21070350_archive.json','data_atvm/donnees_EcoCompt/MMM_EcoCompt_X2H21070351_archive.json','data_atvm/donnees_EcoCompt/MMM_EcoCompt_X2H21111120_archive.json',
           'data_atvm/donnees_EcoCompt/MMM_EcoCompt_X2H21111121_archive.json','data_atvm/donnees_EcoCompt/MMM_EcoCompt_X2H22043029_archive.json','data_atvm/donnees_EcoCompt/MMM_EcoCompt_X2H22043030_archive.json',
           'data_atvm/donnees_EcoCompt/MMM_EcoCompt_X2H22043031_archive.json','data_atvm/donnees_EcoCompt/MMM_EcoCompt_X2H22043032_archive.json','data_atvm/donnees_EcoCompt/MMM_EcoCompt_X2H22043033_archive.json',
           'data_atvm/donnees_EcoCompt/MMM_EcoCompt_X2H22043034_archive.json','data_atvm/donnees_EcoCompt/MMM_EcoCompt_X2H22043035_archive.json','data_atvm/donnees_EcoCompt/MMM_EcoCompt_X2H22104765_archive.json',
           'data_atvm/donnees_EcoCompt/MMM_EcoCompt_X2H22104766_archive.json','data_atvm/donnees_EcoCompt/MMM_EcoCompt_X2H22104767_archive.json','data_atvm/donnees_EcoCompt/MMM_EcoCompt_X2H22104768_archive.json',
           'data_atvm/donnees_EcoCompt/MMM_EcoCompt_X2H22104769_archive.json','data_atvm/donnees_EcoCompt/MMM_EcoCompt_X2H22104770_archive.json','data_atvm/donnees_EcoCompt/MMM_EcoCompt_X2H22104771_archive.json',
           'data_atvm/donnees_EcoCompt/MMM_EcoCompt_X2H22104772_archive.json','data_atvm/donnees_EcoCompt/MMM_EcoCompt_X2H22104773_archive.json','data_atvm/donnees_EcoCompt/MMM_EcoCompt_X2H22104774_archive.json',
           'data_atvm/donnees_EcoCompt/MMM_EcoCompt_X2H22104775_archive.json','data_atvm/donnees_EcoCompt/MMM_EcoCompt_X2H22104776_archive.json','data_atvm/donnees_EcoCompt/MMM_EcoCompt_X2H22104777_archive.json',
           'data_atvm/donnees_EcoCompt/MMM_EcoCompt_XTH19101158_archive.json','data_atvm/donnees_EcoCompt/MMM_EcoCompt_XTH21015106_archive.json','data_atvm/donnees_EcoCompt/MMM_EcoCompt_XTH24072390_archive.json',
           'data_atvm/donnees_EcoCompt/MMM_EcoCompt_XTH24072390_archive_01_06_2024.json','data_atvm/donnees_EcoCompt/MMM_EcoCompt_X2H19070220_2020.json','data_atvm/donnees_EcoCompt/MMM_EcoCompt_X2H20042632_2020.json',
           'data_atvm/donnees_EcoCompt/MMM_EcoCompt_X2H20042633_2020.json','data_atvm/donnees_EcoCompt/MMM_EcoCompt_X2H20042634_2020.json','data_atvm/donnees_EcoCompt/MMM_EcoCompt_X2H20042635_2020.json',
           'data_atvm/donnees_EcoCompt/MMM_EcoCompt_X2H20063161_2020.json','data_atvm/donnees_EcoCompt/MMM_EcoCompt_X2H20063162_2020.json','data_atvm/donnees_EcoCompt/MMM_EcoCompt_X2H20063163_2020.json',
           'data_atvm/donnees_EcoCompt/MMM_EcoCompt_X2H20063164_2020.json','data_atvm/donnees_EcoCompt/MMM_EcoCompt_XTH19101158_2020.json']


def determination_jour(j,m,a):
    """
    Fonction qui détermine un jour de la semaine.
    
    Args:
        param: j (int) : jour
        m (int) : mois
        a (int) : annnée
    Returns:
        int: position dans la semaine
        
        
    Cette fonction prend en argument un jour de l'année défini par les entiers j(le jour),m(le mois),a(l'année), et renvoie un entier compris entre 1 et 7 
    qui va définir le positionnement de la journée dans les jours de la semaine (1 représente lundi, 2 represente mardi,...).

    Etapes de la fonction :
    - Détermination du nombre de jours écoulé dans l'année a pour atteindre la journée en question.
    - reste de la division euclidienne de ce nombre par 7.
    - Détermination de la position du jour dans la semaine sachant qu'en 2022, le 1er Janvier était un samedi.

    Auteur : Lucien Duigou
    """
    nombre_jour=0
    for k in range(2020,a):
        if k%4==0:
            nombre_jour+=366
        else :
            nombre_jour+=365
    for i in range(1,m):
        if i%2==0 :
            if i==2:
                if a%4==0:
                    nombre_jour+=29
                else :
                    nombre_jour+=28
            elif i==8:
                nombre_jour+=31
            elif i==10 :
                nombre_jour+=31
            elif i==12 :
                nombre_jour+=31
            else :
                nombre_jour+=30
        if i%2==1:
            if i==9:
                nombre_jour+=30
            elif i==11:
                nombre_jour+=30
            else :
                nombre_jour+=31
    nombre_jour+=j
    jour=2+(nombre_jour%7)
    if jour>=7:
        return jour-7
    else :
        return jour

def données_jour_semaine(j,m,a):
    """
    Fonction qui récupère des données utiles pour la prédiction des trajets.
    
    Args:
        param: j (int) : jour
        m (int) : mois
        a (int) : annnée
    Returns:
        lists: 3 listes de données

    Cette fonction prend en argument un jour de l'année défini par les entiers j(le jour),m(le mois),a(l'année), et renvoie trois liste qui comprennent des éléments
    de la tables de données des trajets Velomagg de la TAM éffectués en 2022. La fonction va parcourir la table de données ajouter des éléments dans les listes
    si ceux-ci remplissent certains critères.

    Etapes de la fonction:
    - Détermination du jour de la semaine de la journée prise en argument de la fonction qu'on appelle par la suite : ''jour'.
    - Création des 3 listes M,L,W que la fonction va renvoyer à la fin de l'éxécution.
    - La liste L va contenir toutes les informations des trajets de la table de données tels que ces trajets soient effectués le même jour de la semaine 
    que 'jour'.
    - La liste M va contenir le jour, le mois, et l'année de chaque trajet de la table de données qui possède le mêmes critère que la liste L et ce, 
    tel que les éléments de cette liste soient contenus une unique fois'
    - La liste W va contenir toutes les stations de départ('Departure station') et toutes les stations d'arrivée('Return station') selon le même critère que
    la liste L et ce, tel que les éléments de cette liste soient contenus une unique fois.

    Auteur : Lucien Duigou
    """
    jour=determination_jour(j,m,a)
    M=[]
    L=[]
    W=[]
    with open(filename) as f :
        for ligne in f :
            if ligne.split(',')[2]!='Departure':
                x=ligne.split(',')
                if determination_jour(int(x[2].split('-')[2].split(' ')[0]),int(x[2].split('-')[1]),int(x[2].split('-')[0]))==jour:
                    L.append(x)
                    if [int(x[2].split('-')[2].split(' ')[0]),int(x[2].split('-')[1]),int(x[2].split('-')[0])] not in M:
                        M.append([int(x[2].split('-')[2].split(' ')[0]),int(x[2].split('-')[1]),int(x[2].split('-')[0])])
                    if [x[5],x[6]] not in W:
                        W.append([x[5],x[6]])
    return L,M,W

def stats_jour_semaine(j,m,a):
    """
    Fonction qui predit les trajets.
    
    Args:
        param: j (int) : jour
        m (int) : mois
        a (int) : annnée
    Returns:
        list: liste des pédiction de trajets

    Cette fonction prend en argument un jour de l'année défini par les entiers j(le jour),m(le mois),a(l'année), et renvoie une liste des prédictions des trajets (Départ , Arrivée), 
    et le nombre de fois qu'ils seront éffectués (en moyenne empirique) pour le jour de la semaine correspondant à la journée prise en argument par cette dite fonction.

    Etapes de la fonction :
    - Récupération des 3 listes que retourne la fonction données_jour_semaine en prenant en argument j,m,a. Elles seront notées respectivement T, M, et W.
    - Création de la liste L qui contient les éléments de la liste W(Départ,Arrivée) auquel on ajoute un 0 qui aura le rôle de compteur.
    - n est égal au nombre d'éléments de la liste M, c'est-à-dire au nombre total de trajets considérés pour le jour de la semaine en question. Ce nombre sera 
    utile pour calculer les moyennes empiriques de chaque trajet.
    - pour chaque élément de la liste T, on verirife que le jour pour lequel le trajet que représente cet élément et dans la liste M. Si c'est le cas, on veut 
    connaître la position de cet élément dans la liste M afin de compter sa contribution dans la liste L qui possède les mêmes éléments de la liste M, au même 
    positionnement. Et pour cet élément, on ajoute 1/n au compteur.
    - Ainsi, après avoir parcouru l'entièreté de la liste T, la liste L contiendra les trajets (sous la forme de station de départ, station d'arrivée) ainsi 
    que le nombre de fois (calculé par une moyenne empirique) que ces dits trajets seront effectués durant le jour de la semaine considéré.

    Dépendance :
        - copy

    Auteur : Lucien Duigou
    """
    T=copy.deepcopy(données_jour_semaine(j,m,a)[0])
    M=copy.deepcopy(données_jour_semaine(j,m,a)[1])
    W=copy.deepcopy(données_jour_semaine(j,m,a)[2])
    L=[[i,0] for i in W]
    n=len(M)
    for x in T:
        if [int(x[2].split('-')[2].split(' ')[0]),int(x[2].split('-')[1]),int(x[2].split('-')[0])] in M:
            j=W.index([x[5],x[6]])
            L[j][1]+=1/n
    return L

def intensity_jour_stats(j,m,a):
    """
    Fonction qui prédit les intensités.
    
    Args:
        param: j (int) : jour
        m (int) : mois
        a (int) : annnée
    Returns:
        list: liste des pédiction des intensités

    Cette fonction prend en argument un jour de l'année défini par les entiers j(le jour),m(le mois),a(l'année), et renvoie une liste des prédictions des intensités 
    (coordonnées en degré de lattitude et longtitude), et le nombre de fois qu'ils seront mesurés (en moyenne empirique) pour le jour de la semaine correspondant à la journée prise en argument par cette dite fonction.

    Etapes de la fonction:
    - Création de liste N et L qui auront leur utilité lors de l'éxécution de la fonction.
    - Détermination du jour de la semaine de la journée prise en argument de la fonction qu'on appelle par la suite : ''jour'.
    - On parcours tous les fichiers .json qui contiennent pour chaque élément, une valeur en intensité, ainsi que la date et les coordonnées pour lesquelles 
    cette intensité a été mesurée en tant que données intéressantes qui vont nous servir. 
    - pour chaque élément de ces fichiers, on verifie si le jour pour lequel les données ont été enregistrées correspond au même jour de la semaine que le 
    jour pris en argument par la fonction. Si c'est le cas, on ajoute la valeur en intensité ainsi que les coordonnées de cette élément dans la liste L'
    - On cherche par la suite à faire en sorte que les valeurs en coordonnées apparaissent une unique fois dans la liste M tout en comptant le nombre de fois où elles 
    apparaissent dans la liste L. à chaque fois qu'une coordonnée apparraît dans la liste L, on y ajoute sa valeur en intensité. après les avoir toutes 
    additionnées, on divise le nombre obtenu par le nombre de fois que cette coordonnée apparaît dans la liste L. Cela nous donnne la moyenne empirique de
    l'intensité mesuré à cette coordonnée. Ensuite, on ajoute la coordonnée et sa moyenne empirique dans la liste M
    
    Dépendance :
        - json

    Auteur : Lucien Duigou
    """
    L=[]
    jour=determination_jour(j, m, a)
    for filename in archives :
        with open(filename,'r') as f:
            json_data=f.read()
            data=json.loads(json_data)
            for i in range(len(data)):
                if data[i].get("intensity")!=None:
                    jour_data=int(data[i].get("dateObserved").split('-')[2][0]+data[i].get("dateObserved").split('-')[2][1]),int(data[i].get("dateObserved").split('-')[1]),int(data[i].get("dateObserved").split('-')[0])
                    if determination_jour(jour_data[0],jour_data[1],jour_data[2])==jour:
                        L.append([data[i].get("intensity"),data[i].get("location").get('coordinates')])
    M=[]
    for i in L:
        n=0
        c=i[0]
        p=0
        k=0
        for j in L:
            if j[1]==i[1]:
                c+=j[0]
                n+=1
        if len(M)>0:
            while p==0 and k<len(M):
                if i[1]==M[k][1]:
                    p=1 
                k+=1 
        if p==0:
            i[0]=c/n 
            M.append(i)
    return M

def stat_heure_jour(j,m,a):
    """
    Fonction qui récupère les données utiles pour la pondération des heures.
    
    Args:
        param: j (int) : jour
        m (int) : mois
        a (int) : annnée
    Returns:
        list: liste de données

    Cette fonction prend en argument un jour de l'année défini par les entiers j(le jour),m(le mois),a(l'année), et renvoie une liste de la pondération 
    des heures de la journée considérée.

    Etapes de la fonction :
    - Création de la liste L qui contiendra les poids 
    - t est un nombre qui contera le nombre de trajets effectués le jour en question
    - Pour chaque éléments de la table de données, on verifie si le trajet enregistré a été effectué le jour considéré. Si c'est le cas, le compteur t 
    gagne +1 on récupère l'heure à laquelle le trajet a été effectué puis on ajoute 1 à l'élément de L dont la position dans cette liste est l'heure 
    en question'
    - on divise tous les éléments de L par t.

    Auteur : Lucien Duigou
    """
    L=[0 for i in range(24)]
    t=0
    with open(filename) as f:
        for ligne in f :
            x=ligne.split(',')
            if x[2]!='Departure':
                if [int(x[2].split('-')[0]),int(x[2].split('-')[1]),int(x[2].split('-')[2].split(' ')[0])]==[a,m,j]:
                    L[int(x[2].split('-')[2].split(' ')[1].split(':')[0])]+=1
                    t+=1
    L=[j/t for j in L]
    return L

def poids_heure(j,m,a):
    """
    Fonction qui calcule la pondération des heures.
    
    Args:
        param: j (int) : jour
        m (int) : mois
        a (int) : annnée
    Returns:
        list: liste des pondérations des heures

    Cette fonction prend en argument un jour de l'année défini par les entiers j(le jour),m(le mois),a(l'année), et renvoie la liste de la pondération 
    des heures du jour de la semaine de la journée considérée. 

    Etapes de la fonction :
    - Création des liste M,L(qui auront une utilité dans l'éxécution de la fonction), et P(qui contiendra les poids)
    - La liste L va récupérer toutes les dates(jour, mois et année) des trajets qui ont été enregistrés le même jour dans la semaine que le jour considéré
    - La liste M va contenir le resultat de la fonction stat_heure_jour pour chaque élément de la liste L.
    - pour chaque élément de la liste M, la position d'un de ces élément représente la pondération de l'heure représentant cette position pour un jour. 
    - Pour une heure de la journée (représentée dans sa position dans la liste P), la liste P additionne donc chaque poids des éléments de M représentant 
    l'heure en question. Ensuite, le nombre obtenu est divisé par le nombre d'élément de la liste M (c'est-à-dire le nombre de jour qui ont été enregistré
    tels que ces jours soient un jour de la semaine identique à celui de la journée que la fonction prend en argument')

    Auteur : Lucien Duigou
    """
    M=[]
    P=[0 for i in range(0,24)]
    L=[]
    with open(filename) as f:
        for ligne in f:
            x=ligne.split(',')
            if x[2]!='Departure':
                if determination_jour(int(x[2].split('-')[2].split(' ')[0]),int(x[2].split('-')[1]),int(x[2].split('-')[0]))==determination_jour(j,m,a):
                    if [int(x[2].split('-')[0]),int(x[2].split('-')[1]),int(x[2].split('-')[2].split(' ')[0])] not in L:
                        L.append([int(x[2].split('-')[0]),int(x[2].split('-')[1]),int(x[2].split('-')[2].split(' ')[0])])
    for k in L:
        M.append(stat_heure_jour(k[2],k[1],k[0]))
    for i in range(0,24):
        for k in M:
            P[i]+=k[i]
    P=[j/len(M) for j in P]
    return P

def route_prediction_jour(jour_trajet):
    """
    Fonction des routes prédictives à tracer.
    
    Args: 
        param: jour_trajet (list): liste issue de la fonction stats_jour_semaine
    Returns:
        list: liste des segments à tracer sur la carte

    Cette fonction prend en argument une liste défini par jour_trajet qui a été retournée par la fonction stats_jour_semaine et renvoie les segments 
    de la prédiction des trajets que l'on souhaite tracer sur une carte. Ces segments seront renseignés une unique fois dans la liste et 
    seront donc accompagné d'un nombre représentant le nombre de fois qu'ils seront traversé selon la prédiction.

    Etapes de la fonction :
    - Pour chaque éléments de la liste jour_trajet on corrige les noms des stations de départ et d'arrivée pour qu'ils soient reconnus dans 
    'coordonnees_stations' qui a été créer plus tôt dans le programme. 
    - On créer les listes A(qui servira dans l'éxécution du code pour permettre l'unicité des segments à tracer dans la liste que la fonction retourne) et B 
    (cette dernière comportera les éléments que l'on souhaite retourner')
    - pour chaque élément de la liste jour_trajet, on récupère la liste 'route_coords' des coordonnées de la route empruntée par le trajet que renseigne cet 
    élément  avec pour départ et arrivée la station de départ et d'arrivée. 
    - pour chaque segment de route_coords, on vérifie s'il est déja présent dans la liste A. Si ce n'est pas le cas, alors on l'ajoute dans A mais aussi 
    dans B(en ajoutant le nombre de fois que ce trajet est censé être emprunté, en tant que compteur). Si c'est déja le cas, on repère la position de ce 
    segment dans la liste A, ce segment ainsi que son compteur aura la même position dans la liste B. Comme ce segment est déja dans la liste B, on ajoute à 
    son compteur déja existant, le nombre de fois qu'il est censé être emprunté.
    
    Dépendances :
        - osmnx
        - folium
        - networkx
        - 

    Auteurs : Wahel El Mazzouji, Lucien Duigou
    """
    for i in jour_trajet :
        if len(i[0][0])>1:
            c=i[0][0].split(' ')[1]
            i[0][0]=i[0][0].split(' ')[2:]
            for j in i[0][0]:
                c=c+' '+j
            i[0][0]=c
        if len(i[0][1])>1:
            c=i[0][1].split(' ')[1]
            i[0][1]=i[0][1].split(' ')[2:]
            for j in i[0][1]:
                c=c+' '+j
            i[0][1]=c
        if i[0][0]=='FacdesSciences':
            i[0][0]='Fac des Sciences'
        elif i[0][0]=='ComÃƒÂ©die':
            i[0][0]='Comédie'
        elif i[0][0]=='PÃƒÂ¨re Soulas':
            i[0][0]='Père Soulas'
        elif i[0][0]=="PÃƒÂ©rols Etang de l'Or":
            i[0][0]="Pérols Etang de l'Or"
        elif i[0][0]=="PrÃƒÂ©s d'ArÃƒÂ¨nes":
            i[0][0]="Prés d'Arènes"
        elif i[0][0]=='Jeu de Mail des AbbÃƒÂ©s':
            i[0][0]='Jeu de Mail des Abbés'
        elif i[0][0]=='HÃƒÂ´tel de Ville':
            i[0][0]='Hôtel de ville'
        elif i[0][0]=='CitÃƒÂ© Mion':
            i[0][0]='Cité Mion'
        elif i[0][0]=='HÃƒÂ´tel du DÃƒÂ©partement':
            i[0][0]='Hôtel du Département'
        elif i[0][0]=='MÃƒÂ©diathÃƒÂ¨que Emile Zola':
            i[0][0]='Médiathèque Emile Zola'
        elif i[0][0]=='EuromÃƒÂ©decine':
            i[0][0]='Euromédecine'
        elif i[0][0]=='Albert 1er - CathÃƒÂ©drale':
            i[0][0]='Albert 1er - Cathédrale'
        if i[0][1]=='FacdesSciences':
            i[0][1]='Fac des Sciences'
        elif i[0][1]=='ComÃƒÂ©die':
            i[0][1]='Comédie'
        elif i[0][1]=='PÃƒÂ¨re Soulas':
            i[0][1]='Père Soulas'
        elif i[0][1]=="PÃƒÂ©rols Etang de l'Or":
            i[0][1]="Pérols Etang de l'Or"
        elif i[0][1]=="PrÃƒÂ©s d'ArÃƒÂ¨nes":
            i[0][1]="Prés d'Arènes"
        elif i[0][1]=='Jeu de Mail des AbbÃƒÂ©s':
            i[0][1]='Jeu de Mail des Abbés'
        elif i[0][1]=='HÃƒÂ´tel de Ville':
            i[0][1]='Hôtel de ville'
        elif i[0][1]=='CitÃƒÂ© Mion':
            i[0][1]='Cité Mion'
        elif i[0][1]=='HÃƒÂ´tel du DÃƒÂ©partement':
            i[0][1]='Hôtel du Département'
        elif i[0][1]=='MÃƒÂ©diathÃƒÂ¨que Emile Zola':
            i[0][1]='Médiathèque Emile Zola'
        elif i[0][1]=='EuromÃƒÂ©decine':
            i[0][1]='Euromédecine'
        elif i[0][1]=='Albert 1er - CathÃƒÂ©drale':
            i[0][1]='Albert 1er - Cathédrale'
            
    ville = "Montpellier, France"
    G = ox.graph_from_place(ville, network_type="all")
    m = folium.Map(location=[43.6114, 3.8767], zoom_start=13)
            
    A=[]
    B=[]
    for i in jour_trajet :
        if i[0][1]!="Pérols Etang de l'Or":
            depart_station = i[0][0]
            retour_station = i[0][1] 
            
            if depart_station in coordonnees_stations and retour_station in coordonnees_stations:
                # Récupérer les coordonnées des stations
                coords_depart = coordonnees_stations[depart_station]
                coords_retour = coordonnees_stations[retour_station]
                
                # Trouver les nœuds les plus proches dans le graphe
                depart_node = ox.distance.nearest_nodes(G, coords_depart['longitude'], coords_depart['latitude'])
                retour_node = ox.distance.nearest_nodes(G, coords_retour['longitude'], coords_retour['latitude'])
        
                # Calculer le chemin le plus court
                route = nx.shortest_path(G, source=depart_node, target=retour_node, weight='length')
                
                # détermination de la liste des segments de route à tracer sur la carte
                route_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in route]
                
                for j in range(len(route_coords)):
                    if j<len(route_coords)-1:
                        x=[route_coords[j],route_coords[j+1]]
                        if x not in A:
                            A.append(x)
                            B.append([x,i[1]])
                        else :
                            k=A.index(x)
                            B[k][1]+=i[1]
    return B

#%%

lundi_trajet=stats_jour_semaine(17,1,2022)
mardi_trajet=stats_jour_semaine(18,1,2022)
mercredi_trajet=stats_jour_semaine(19,1,2022)
jeudi_trajet=stats_jour_semaine(13,1,2022)
vendredi_trajet=stats_jour_semaine(14,1,2022)
samedi_trajet=stats_jour_semaine(15,1,2022)
dimanche_trajet=stats_jour_semaine(16,1,2022)
semaine_trajet=[lundi_trajet,mardi_trajet,mercredi_trajet,jeudi_trajet,vendredi_trajet,samedi_trajet,dimanche_trajet]


lundi_intensity = intensity_jour_stats(22,4,2024)
mardi_intensity = intensity_jour_stats(23,4,2024)
mercredi_intensity = intensity_jour_stats(24,4,2024)
jeudi_intensity = intensity_jour_stats(25,4,2024)
vendredi_intensity = intensity_jour_stats(26,4,2024)
samedi_intensity = intensity_jour_stats(27,4,2024)
dimanche_intensity = intensity_jour_stats(28,4,2024)
semaine_intensity = [lundi_intensity,mardi_intensity,mercredi_intensity,jeudi_intensity,vendredi_intensity,samedi_intensity,dimanche_intensity]


lundi_heure=poids_heure(17, 1, 2022)
mardi_heure=poids_heure(18, 1, 2022)
mercredi_heure=poids_heure(19, 1, 2022)
jeudi_heure=poids_heure(13, 1, 2022)
vendredi_heure=poids_heure(14, 1, 2022)
samedi_heure=poids_heure(15, 1, 2022)
dimanche_heure=poids_heure(16, 1, 2022)
semaine_heure=[lundi_heure,mardi_heure,mercredi_heure,jeudi_heure,vendredi_heure,samedi_heure,dimanche_heure]

lundi_map=route_prediction_jour(lundi_trajet)
mardi_map=route_prediction_jour(mardi_trajet)
mercredi_map=route_prediction_jour(mercredi_trajet)
jeudi_map=route_prediction_jour(jeudi_trajet)
vendredi_map=route_prediction_jour(vendredi_trajet)
samedi_map=route_prediction_jour(samedi_trajet)
dimanche_map=route_prediction_jour(dimanche_trajet)
semaine_carte=[lundi_map,mardi_map,mercredi_map,jeudi_map,vendredi_map,samedi_map,dimanche_map]

semaine=['lundi','mardi','mercredi','jeudi','vendredi','samedi','dimanche']
#%%
''' fonctions permettants de générer les carte de prédiction '''

def couleur_intensity(nombre):
    """
    Fonction qui retourne une couleur.
    
    Args:
        param: nombre (float) : nombre flotant
    Returns:
        str: couleur

    Cette Fonction prend en argument un flotant défini par nombre, et renvoie un string représentant une couleur selon l'intervalle dans lequel
    se trouve le nombre en question. cette fonction servira à définir la couleur des segments que l'on souhaitera tracer sur une carte prédictive 
    pour une journée entière.

    Auteur : Lucien Duigou
    """
    if 0<=nombre<250:
        return 'green'
    if 250<=nombre <500:
        return 'blue'
    elif 500<=nombre<=1000:
        return 'orange'
    else :
        return 'red'

def couleur_intensity_heure(nombre):
    """
    Fonction qui retourne une couleur.
    
    Args:
        param: nombre (float) : nombre flotant
    Returns:
        str: couleur

    Cette Fonction prend en argument un flotant défini par nombre, et renvoie un string représentant une couleur selon l'intervalle dans lequel
    se trouve le nombre en question. cette fonction servira à définir la couleur des segments que l'on souhaitera tracer sur une carte prédictive
    pour une heure particulière d'une journée.

    Auteur : Lucien Duigou
    """
    if 0<=nombre<5:
        return 'green'
    elif 5<=nombre<10:
        return 'blue'
    elif 10<=nombre<20:
        return 'orange'
    else :
        return 'red'

def carte_prediction_jour(j,m,a):
    """
    Fonction qui trace une carte prédictive sur une journée.
    
    Args:
        param: j (int) : jour
        m (int) : mois
        a (int) : annnée
    Returns:
        .html: enregistre une carte prédictive par jour

    Cette fonction prend en argument un jour de l'année défini par les entiers j(le jour),m(le mois),a(l'année), en renvoie une carte des trajets prédis pour
    le jour de la semaine que représente la journée considérée. Elle prend en compte à la fois la prédiction des trajets mais aussi la prédiction des intensité, en 
    supposant qu'une intensité mesurée a une influence sur un rayon de 250m autour du point où elle a été mesurée.

    Etapes de la fonction :
    - Détermination du jour de la semaine de la journée prise en argument de la fonction qu'on appelle par la suite : 'jour'.
    - coord est la liste que renvoit la fonction route_prediction_jour pour le jour de la semaine étudié
    - intensity est la liste des prédiction des intensités (et leurs coordonnées) pour le jour de la semaine étudié
    - Pour tout segment de la liste coord, on verifie si les coordonnées de ce segment est à 250m d'une mesure d'intensité. Si c'est le cas, on additionne
    l'intensité censé être mesuré ce jour-ci par le compteur de ce segement. on défini ainsi la couleur qu'est censé prendre le segment lors du tracer sur la 
    carte.
    - Le segment est ensuite tracé sur la carte avec la couleur définie précédemment 
    - Lorsque tous les segments sont tracés, on écrit la légende et on enregistre la carte dans le même dossier que le projet actuel et portera un nom 
    en fonction du jour de la semaine de la journée prise en argument de la fonction

    Dépendances:
        - copy
        - osmnx
        - folium

    Auteurs : Wahel El Mazzouji, Lucien Duigou
    """
    jour=determination_jour(j,m,a)
    coord=copy.deepcopy(semaine_carte[jour-1])
    intensity=semaine_intensity[jour-1]
    ville = "Montpellier, France"
    G = ox.graph_from_place(ville, network_type="all")
    m = folium.Map(location=[43.6114, 3.8767], zoom_start=13)
    for i in coord:
        n=i[1]
        for k in intensity:
            if abs(i[0][0][0]-(k[1][1]))<=0.0022500022500023:
                if abs(i[0][0][1]-k[1][0])<=0.0031819975307699:
                    n+=k[0]
        couleur=couleur_intensity(n)
        folium.PolyLine(locations=i[0], color=couleur, weight=5, opacity=0.7).add_to(m)
    legend_html = """
    <div style="position: fixed; 
                bottom: 50px; left: 50px; width: 200px; height: auto; 
                background-color: white; opacity: 0.8; z-index: 1000; border:2px solid grey; 
                padding: 10px; font-size: 14px;">
        <h4 style="margin: 0;">Légende des Couleurs</h4>
        <p><span style="color: green;">&#9679;</span> Intensité inférieure à 250 </p>
        <p><span style="color: blue;">&#9679;</span> Intensité entre 250 et 500</p>
        <p><span style="color: orange;">&#9679;</span> Intensité entre 500 et 1000 </p>
        <p><span style="color: red;">&#9679;</span> Intensité supérieure à 1000</p>
    </div>
    """

    m.get_root().html.add_child(folium.Element(legend_html))
    
    name=semaine[jour-1]

    #Sauvegarder la carte dans un fichier HTML
    m.save('carte_prediction_'+name+'.html')

    # Afficher un message pour indiquer que la carte est prête
    print("La carte a été sauvegardée sous 'carte_prediction_"+name+".html'. Ouvrez ce fichier dans votre navigateur pour afficher la carte.")
    
    
    
def carte_prediction_jour_heure(j,m,a,h):
    """
    Fonction qui trace une carte prédictive sur une heure précise d'une journée.
    
    Args:
        param: j (int) : jour
        m (int) : mois
        a (int) : année
        h (str) : heure sous la forme 'heurehminute' où heure est un integer
    Returns:
        .html: enregistre une carte prédictive par jour par heure

    Cette fonction prend en argument un jour de l'année défini par les entiers j(le jour),m(le mois),a(l'année) et une heure définie par un string sous la forme 'heurehminute', en renvoie une carte des trajets prédis pour
    l'heure en question, le jour de la semaine que représente la journée considérée. Elle prend en compte à la fois la prédiction des trajets mais aussi la prédiction des intensité, en 
    supposant qu'une intensité mesurée a une influence sur un rayon de 250m autour du point où elle a été mesurée. Tous les compteurs de trajets et d'intensité sont 
    multipliés par le poids de l'heure considérée.

    Etapes de la fonction :
    - Détermination du jour de la semaine de la journée prise en argument de la fonction qu'on appelle par la suite : 'jour'.
    -h est un entier qui représente l'heure que l'on considère dans la fonction.
    - coord est la liste que renvoit la fonction route_prediction_jour pour le jour de la semaine étudié. Tous les compteurs des segments sont multipliés
    par le poids de l'heure considérée.
    - intensity est la liste des prédiction des intensités (et leurs coordonnées) pour le jour de la semaine étudié. Tous les compteurs des intensités 
    sont multipliés par le poids de l'heure considérée.
    - Pour tout segment de la liste coord, on verifie si les coordonnées de ce segment est à 250m d'une mesure d'intensité. Si c'est le cas, on additionne
    l'intensité censé être mesuré ce jour-ci par le compteur de ce segement. on défini ainsi la couleur qu'est censé prendre le segment lors du tracer sur la 
    carte.
    - Le segment est ensuite tracé sur la carte avec la couleur définie précédemment 
    - Lorsque tous les segments sont tracés, on écrit la légende et on enregistre la carte dans le même dossier que le projet actuel et portera un nom 
    en fonction du jour de la semaine de la journée prise en argument de la fonction
    
    Dépendances:
        - copy
        - osmnx
        - folium

    Auteurs : Wahel El Mazzouji, Lucien Duigou
    """    
    jour=determination_jour(j,m,a)
    heure=int(h.split('h')[0])
    coord=copy.deepcopy(semaine_carte[jour-1])
    coord=[[[i[0][0],i[0][1]],i[1]*lundi_heure[heure]] for i in coord]
    intensity=copy.deepcopy(semaine_intensity[jour-1])
    intensity=[[i[0]*lundi_heure[heure],[i[1][0],i[1][1]]]for i in intensity]
    ville = "Montpellier, France"
    G = ox.graph_from_place(ville, network_type="all")
    m = folium.Map(location=[43.6114, 3.8767], zoom_start=13)
    for i in coord:
        n=i[1]
        for k in intensity:
            if abs(i[0][0][0]-(k[1][1]))<=0.0022500022500023:
                if abs(i[0][0][1]-k[1][0])<=0.0031819975307699:
                    n+=k[0]
        couleur=couleur_intensity_heure(n)
        folium.PolyLine(locations=i[0], color=couleur, weight=5, opacity=0.7).add_to(m)
    legend_html = """
    <div style="position: fixed; 
                bottom: 50px; left: 50px; width: 200px; height: auto; 
                background-color: white; opacity: 0.8; z-index: 1000; border:2px solid grey; 
                padding: 10px; font-size: 14px;">
        <h4 style="margin: 0;">Légende des Couleurs</h4>
        <p><span style="color: green;">&#9679;</span> Intensité inférieure à 5 </p>
        <p><span style="color: blue;">&#9679;</span> Intensité entre 5 et 10 </p>
        <p><span style="color: orange;">&#9679;</span> Intensité entre 10 et 20 </p>
        <p><span style="color: red;">&#9679;</span> Intensité supérieure à 20 </p>
    </div>
    """

    m.get_root().html.add_child(folium.Element(legend_html))

    #Sauvegarder la carte dans un fichier HTML
    name=semaine[jour-1]+'_'+str(heure)+'h'
    m.save('carte_prediction_'+name+'.html')
    # Afficher un message pour indiquer que la carte est prête
    print("La carte a été sauvegardée sous 'carte_prediction_",name,".html'. Ouvrez ce fichier dans votre navigateur pour afficher la carte.")
