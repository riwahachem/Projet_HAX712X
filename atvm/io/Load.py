import os 
import pandas as pd
import pooch
from atvm.io import url_courses_24


class Load:
    """
    Cette classe télécharge toutes les données.

    Paramètres:
    -----------
    url_courses_24 : (string) url des données de l'année en cours
    path_target : (string) chemin pour accéder aux données
    """

