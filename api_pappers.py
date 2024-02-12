"""
Un script pour la recherche des données des
bénéficiaires effectifs avec l'API Pappers
"""

import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

PAPPERS_API_KEY = os.getenv("PAPPERS_API_KEY")
PAPPERS_BASE_URL = "https://api.pappers.fr/v2"

def fetch_data_entreprises(siren=None):
    """Recherche d'une entreprise"""

    siren = "444979314" # exemple d'un numéro SIREN pour la recherche
    url = f"{PAPPERS_BASE_URL}/entreprise?api_token={PAPPERS_API_KEY}&siren={siren}"
    response = requests.request("GET", url, timeout=10)
    print(response.json())

    with open('data/api_pappers_entreprises.json', 'w', encoding='utf-16') as f:
        json.dump(response.json(), f)

    return response.json()

def fetch_data_beneficiaires_effectifs(nom=None):
    """Recherche d'un(e) bénéficiaire effectif"""

    nom = "Xavier Niel" # exemple d'un nom pour la recherche
    url = f"{PAPPERS_BASE_URL}/recherche-beneficiaires?api_token={PAPPERS_API_KEY}&q={nom}"
    response = requests.request("GET", url, timeout=10)
    print(response.json())

    with open('data/api_pappers_beneficiaire_effectif.json', 'w', encoding='utf-16') as f:
        json.dump(response.json(), f)

    return response.json()

if __name__ == "__main__":
    fetch_data_entreprises()
    fetch_data_beneficiaires_effectifs()
