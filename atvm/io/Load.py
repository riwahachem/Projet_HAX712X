import os 
import pandas as pd
import pooch
from atvm.io import url_courses_24, path_target


class Load:
    """
    Cette classe télécharge toutes les données.

    Paramètres:
    -----------
    url_courses_24 : (string) url des données de l'année en cours
    path_target : (string) chemin pour accéder aux données
    """

    def __init__(self, url=url_courses_24, target_name=path_target):
        path, fname_compressed = os.path.split(target_name)
        # Téléchargement des données avec pooch
        pooch.retrieve(url, path=path, fname=fname_compressed, known_hash=None)
        self.fname = target_name
    
    def save_as_df(self):
        df = pd.read_csv(self.fname)
        return df

