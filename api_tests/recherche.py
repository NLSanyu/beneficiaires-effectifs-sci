"""
Recherche par nom ou par entreprise
"""

from api_pappers import fetch_data_beneficiaires_effectifs, fetch_data_entreprises


def recherche_par_nom(nom=None):
    """Recherche par nom du bénéficiaire effectif"""

    data_nom = fetch_data_beneficiaires_effectifs(nom)
    beneficiaires_list = []

    for item_n in data_nom["resultats"]:
        for item_e in item_n["entreprises"]:
            siren = item_e["siren"]
            nom_entreprise = item_e["nom_entreprise"]
            data_entreprise = fetch_data_entreprises(siren)
            for item_b in data_entreprise["beneficiaires_effectifs"]:
                beneficiaires_list.append({nom_entreprise: f"{item_b['prenom']} {item_b['nom']}"})

    return (nom, beneficiaires_list)

def recherche_par_entreprise(siren=None):
    """Recherche par siren entreprise"""

    beneficiaires_list = []
    data_entreprise = fetch_data_entreprises(siren)
    nom_entreprise = data_entreprise["nom_entreprise"]

    for item in data_entreprise["beneficiaires_effectifs"]:
        beneficiaires_list.append(f"{item['prenom']} {item['nom']}")

    return (nom_entreprise, beneficiaires_list)
