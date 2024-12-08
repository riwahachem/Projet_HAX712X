import sys
import os
import osmnx
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import atvm

from atvm.preprocess.carte_stations import output_path

def test_carte_stations():
    """Vérifie que le fichier de carte des stations est généré."""
    assert os.path.exists(output_path), f"Le fichier {output_path} n'a pas été généré."

from atvm.preprocess.map_informative import ville

def test_map_informative():
    """Vérifie que le fichier HTML de la carte est généré."""
    output_path = 'montpellier_bike_stations_same_color.html'
    assert os.path.exists(output_path), f"Le fichier {output_path} n'a pas été généré."