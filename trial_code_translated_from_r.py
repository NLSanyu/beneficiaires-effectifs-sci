import pandas as pd
import requests
from requests.auth import HTTPBasicAuth

# Chargement d'un csv avec les codes siren qui vont être requêté
# il doit avoir le format suivant :
# pd.DataFrame({"siren": ["352761290", "505305300", "450675343", "438246498"]})
df = pd.read_csv("../donnees/donnees_exemple.csv")

# Date requêtée
date = "2022-01-01"

# Requête de connexion à l'API
url = "https://registre-national-entreprises.inpi.fr/api/sso/login"
email = input("Entrez votre email : ")
password = input("Entrez votre mot de passe : ")
body = {"username": email, "password": password}
response = requests.post(url, json=body)
token = response.json()["token"]

# Fonctions pour renvoyer un NA en cas d'absence d'information
def NAifNull(x):
    return x if x is not None else None

# Fonction pour récupérer les infos d'un bénéficiaire
def info_beneficiaire(i, data):
    return pd.DataFrame({
        "nom": NAifNull(data[i]["beneficiaire"]["descriptionPersonne"]["nom"].lower()),
        "prenoms": NAifNull(",".join(map(str, data[i]["beneficiaire"]["descriptionPersonne"]["prenoms"]))),
        "dnss": NAifNull(data[i]["beneficiaire"]["descriptionPersonne"]["dateDeNaissance"]),
        "nationalite": NAifNull(data[i]["beneficiaire"]["descriptionPersonne"]["nationalite"]),
        "pays_residence": NAifNull(data[i]["beneficiaire"]["adresseDomicile"]["pays"]),
        "role": NAifNull(",".join(filter(None, [names for names in unlist(data[i]["modalite"]) if data[i]["modalite"][names] == 1])))
    })

# Fonction qui effectue la requête, extrait les infos sur l'entreprise, sa gouvernance et ses bénéficiaires
# et alimente un csv
def write_entre_data(siren):
    # début de la boucle
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"https://registre-national-entreprises.inpi.fr/api/companies/{siren}?date={date}", headers=headers)
    rx = response.json()

    if rx["formality"]["content"]["natureCessation"] is None:
        entreprise = pd.DataFrame({
            "siren": rx["siren"],
            "date_creation": NAifNull(rx["formality"]["content"]["natureCreation"]["dateCreation"]),
            "societe_etrangere": NAifNull(rx["formality"]["content"]["natureCreation"]["societeEtrangere"]),
            "forme_juridique": NAifNull(rx["formality"]["content"]["natureCreation"]["formeJuridique"]),
            "forme_exercice": NAifNull(rx["formality"]["content"]["formeExerciceActivitePrincipale"]),
            "denomination": NAifNull(rx["formality"]["content"]["personneMorale"]["identite"]["entreprise"]["denomination"]),
            "code_ape": NAifNull(rx["formality"]["content"]["personneMorale"]["identite"]["entreprise"]["codeApe"]),
            "num_voie": NAifNull(rx["formality"]["content"]["personneMorale"]["adresseEntreprise"]["adresse"]["numVoie"]),
            "type_voie": NAifNull(rx["formality"]["content"]["personneMorale"]["adresseEntreprise"]["adresse"]["typeVoie"]),
            "voie": NAifNull(rx["formality"]["content"]["personneMorale"]["adresseEntreprise"]["adresse"]["voie"]),
            "code_postal": NAifNull(rx["formality"]["content"]["personneMorale"]["adresseEntreprise"]["adresse"]["codePostal"]),
            "commune": NAifNull(rx["formality"]["content"]["personneMorale"]["adresseEntreprise"]["adresse"]["commune"]),
            "pays": NAifNull(rx["formality"]["content"]["personneMorale"]["adresseEntreprise"]["adresse"]["pays"]),
            "code_insee": NAifNull(rx["formality"]["content"]["personneMorale"]["adresseEntreprise"]["adresse"]["codeInseeCommune"]),
            "capital": NAifNull(rx["formality"]["content"]["personneMorale"]["identite"]["description"]["montantCapital"])
        })

        ben = rx["formality"]["content"]["personneMorale"]["beneficiairesEffectifs"]

        beneficiaires = pd.concat([info_beneficiaire(x, ben) for x in range(len(ben))], ignore_index=True)
        beneficiaires["siren"] = rx["siren"]

        pouvoirs = rx["formality"]["content"]["personneMorale"]["composition"]["pouvoirs"]
        vec_length = [len(pouvoirs[x]) for x in range(len(pouvoirs))]

        if 5 in vec_length:
            pv_entr = pd.concat([
                pd.concat([pd.DataFrame(pouvoirs[x]["entreprise"]), pd.DataFrame(pouvoirs[x]["adresseEntreprise"])]) for x in
                range(len(pouvoirs)) if len(pouvoirs[x]) == 5], ignore_index=True)
            pv_entr["siren_source"] = rx["siren"]

        if 3 in vec_length:
            pv_ind = pd.concat([
                pd.DataFrame({
                    "id": x,
                    "variable": name.replace("individu.descriptionPersonne.", ""),
                    "values": pouvoirs[x][name]
                }) for x in range(len(pouvoirs)) if len(pouvoirs[x]) == 3 for name in pouvoirs[x]
            ], ignore_index=True).pivot(index="id", columns="variable", values="values").reset_index()
            pv_ind["siren_source"] = rx["siren"]

        if "entreprise" in locals():
            entreprise.to_csv("../donnees/table_entreprise.csv", sep=";", mode="a", header=not pd.io.common.file_exists("../donnees/table_entreprise.csv"), index=False)

        if "beneficiaires" in locals():
            beneficiaires.to_csv("../donnees/table_beneficiaires.csv", sep=";", mode="a", header=not pd.io.common.file_exists("../donnees/table_beneficiaires.csv"), index=False)

        if "pv_ind" in locals():
            pv_ind.to_csv("../donnees/table_dirigeants_individus.csv", sep=";", mode="a", header=not pd.io.common.file_exists("../donnees/table_dirigeants_individus.csv"), index=False)

        if "pv_entr" in locals():
            pv_entr.to_csv("../donnees/table_dirigeants_entreprise.csv", sep=";", mode="a", header=not pd.io.common.file_exists("../donnees/table_dirigeants_entreprise.csv"), index=False)

    print(siren)

# Suppression des codes invalides
df = df[df["dsiren"].str[0] != "U"]

# Boucle
[df.apply(lambda row: write_entre_data(row["dsiren"]), axis=1) for _, row in df.iterrows()]
