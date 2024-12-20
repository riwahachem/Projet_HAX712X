import os 
import pandas as pd
import pooch
import zipfile

class LoadData:
    """
    Classe pour télécharger et gérer des données.

    :param url: (string) URL des données à télécharger
    :param target_name: (string) Chemin local pour stocker les données téléchargées
    """

    def __init__(self, url, target_name):
        """
        Initialise l'instance LoadData.

        :param url : (string) URL des données à télécharger
        :param target_name : (string) Chemin local pour stocker les données téléchargées
        """
        path, fname_compressed = os.path.split(target_name)
       
        pooch.retrieve(url, path=path, fname=fname_compressed, known_hash=None)
        self.fname = target_name

    def extract_zip(self, extract_to):
        """
        Extrait un fichier .zip vers un dossier spécifié.

        :param extract_to: Chemin du dossier cible pour les fichiers extraits.

        :return: Liste des fichiers extraits.
        """
        if not self.fname.endswith(".zip"):
            raise ValueError("Le fichier cible n'est pas une archive .zip")

        # Crée le dossier cible s'il n'existe pas
        os.makedirs(extract_to, exist_ok=True)

        # Extraire le contenu de l'archive .zip
        with zipfile.ZipFile(self.fname, "r") as zip_ref:
            zip_ref.extractall(extract_to)

        # Retourne la liste des fichiers extraits
        return [os.path.join(extract_to, name) for name in zip_ref.namelist()]

    
    def save_as_df(self):
        """
        Charge le fichier CSV en DataFrame.

        :return: pd.DataFrame: Données chargées
        """
        df = pd.read_csv(self.fname)
        return df