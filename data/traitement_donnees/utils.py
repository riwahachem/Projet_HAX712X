"""
Module utilitaire contenant des fonctions réutilisables.

Auteur : Wahel El Mazzouji
"""

import re
from unidecode import unidecode

def corriger_encodage(station_name):
    """
    Corrige les problèmes d'encodage des noms de stations et nettoie le texte.

    Args:
        station_name (str): Nom brut de la station.

    Returns:
        str: Nom corrigé de la station.
    """
    if isinstance(station_name, str):
        try:
            station_name = station_name.encode('latin1').decode('utf-8')
        except (UnicodeEncodeError, UnicodeDecodeError):
            station_name = unidecode(station_name)
        station_name = re.sub(r'^\d+\s*', '', station_name).strip()  # Supprime les numéros en début
    return station_name
