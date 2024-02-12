from api_pappers import fetch_data_beneficiaires_effectifs, fetch_data_entreprises


def recherche_par_nom(nom=None):
    """Recherche par nom du bénéficiaire effectif"""
    data_nom = fetch_data_beneficiaires_effectifs(nom)
    benef_list = []

    for item_n in data_nom["resultats"][1]["entreprises"]:
        siren = item_n["siren"]
        nom_entreprise = item_n["nom_entreprise"]
        data_entreprise = fetch_data_entreprises(siren)
        for item_e in data_entreprise["beneficiaires_effectifs"]:
            benef_list.append({nom_entreprise: f"{item_e['nom']} {item_e['prenom']}"})

    return f"Nom : {nom}, Entreprises : {benef_list}"

def recherche_par_entreprise(siren=None):
    """Recherche par siren entreprise"""
