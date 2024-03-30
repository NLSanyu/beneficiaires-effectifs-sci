"""
Trouver les correspondances entre les deux bases (INPI et Pappers)
"""

from inpi import fetch_and_filter_data
from pappers import fetch_data

def find_matches():
    """
    Trouver les correspondances entre les deux bases
    """
    inpi = fetch_and_filter_data(None)
    pappers = fetch_data()

    # Convertir les listes en strings pour une comparaison directe si nécessaire
    pappers["siren_str"] = pappers["siren"].apply(lambda x: ", ".join(map(str, x)))

    # # Calculer le nombre de correspondances
    # matches = inpi["unique_key"].isin(pappers["unique_id"]).sum()
    # print(f"Nombre de personnes présentes dans les deux bases : {matches}")

    # Filtrer df pour obtenir seulement les entrées correspondantes
    matching_persons_df = inpi[inpi["unique_key"].isin(pappers["unique_id"])]

    # Afficher les premières lignes du DataFrame filtré pour vérification
    print(matching_persons_df.head())

    matching_persons_df.to_csv("data/matches_inpi_pappers.csv", index=False)

    return matching_persons_df

if __name__ == "__main__":
    find_matches()
