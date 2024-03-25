import sqlite3
import os
import numpy as np
import pandas as pd
import geopandas as gpd
import contextily as ctx
import matplotlib.pyplot as plt
import matplotlib.colors as clrs
#import matplotlib_scalebar.scalebar as mss
#from mss import ScaleBar
#from matplotlib_scalebar.scalebar import ScaleBar
import seaborn as sns
import datetime as dt
# import pysal as ps
import requests
# from pandas import json_normalize
# from fiona.crs import from_epsg
import geopy
# import dataframe_image as dfi

import pandas as pd
import psycopg2

def fetch_data():
    # Paramètres de connexion à la base de données
    dbname = 'interlend220228'
    user = 'postgres'
    password = 'postgres'
    host = 'localhost'

    # Initialiser une liste vide pour stocker les données extraites
    data_list = []

    try:
        # Connexion à la base de données
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
        cur = conn.cursor()

        # Sélectionner toutes les entrées de la table
        cur.execute('SELECT siren, result FROM rne.siren_info')

        # Pour chaque entrée dans la base de données
        for row in cur.fetchall():
            siren = row[0]  # Le numéro SIREN
            data = row[1]  # Le champ JSON

            # Exemple d'extraction
            if "formality" in data and "content" in data["formality"] and "personneMorale" in data["formality"]["content"]:
                pouvoirs = data["formality"]["content"]["personneMorale"].get("composition", {}).get("pouvoirs", [])
                for pouvoir in pouvoirs:
                    if "individu" in pouvoir and "descriptionPersonne" in pouvoir["individu"]:
                        nom = pouvoir["individu"]["descriptionPersonne"].get("nom", "Inconnu")[0]
                        prenoms_list = pouvoir["individu"]["descriptionPersonne"].get("prenoms", [])
                        prenoms = ", ".join([prenom[0] if isinstance(prenom, list) else prenom for prenom in prenoms_list])
                        date_naissance = pouvoir["individu"]["descriptionPersonne"].get("dateDeNaissance", "Inconnue")[0]
                        data_list.append({"siren": siren, "nom": nom, "prenoms": prenoms, "date_naissance": date_naissance})
    except Exception as e:
        print(f"Une erreur est survenue: {e}")
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

    # Créer un DataFrame à partir de la liste de données
    df = pd.DataFrame(data_list)

    # Afficher le DataFrame pour vérifier
    print(df.head())

    # Vous pouvez maintenant sauvegarder ce DataFrame dans un fichier CSV si nécessaire
    df.to_csv("rbe.csv", index=False)

if __name__ == "__main__":
    fetch_data()

