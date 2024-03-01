"""
Récupérer les données des bénéficiaires effectifs d'un fichier JSON
"""

import json

def get_data_from_json_file(filename):
    """
    Ouvrir le fichier JSON et récupérer les données
    """

    try:
        with open(filename, encoding="utf-16") as f:
            data = json.load(f)
    except FileNotFoundError as err:
        print(err)
        return None

    return data
