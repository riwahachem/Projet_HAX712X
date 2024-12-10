

from .coord_arrets import get_station_coordinates
from .graphique import analyse_trajets
#from .map import couleur_par_distance
#from .stats import charger_donnees, corriger_adresses, calculer_statistiques, trajets_par_station, trajets_par_jour, afficher_statistiques, choisir_date, afficher_nombre_trajets_par_station, afficher_nombre_trajets_par_jour
from .trajets_jour import trajets_analys
from .utils import corriger_encodage
#from .visualisation import corriger_nom_station, calcul_chemin_vélo, init,  mettre_a_jour_trajets
from .prediction import determination_jour,  données_jour_semaine, stats_jour_semaine, intensity_jour_stats, stat_heure_jour, poids_heure, route_prediction_jour, couleur_intensity, couleur_intensity_heure, carte_prediction_jour, carte_prediction_jour_heure