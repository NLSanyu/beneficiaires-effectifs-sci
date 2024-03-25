import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pyvis.network import Network

import streamlit as st

def prep_data():
    df = pd.read_csv("rbe.csv")

    # Créer une clé unique basée sur le nom, le premier prénom et la date de naissance
    df["unique_key"] = df["nom"].str.upper() + "_" + df["prenoms"].str.split(pat=",").str[0] + "_" + df["date_naissance"]

    # Group by unique key
    # df2 = df.groupby("unique_key")["siren"].apply(list).reset_index()
    return df


if __name__ == "__main__":
    df = prep_data()

    # Convertir les colonnes "siren" et "unique_key" en type string
    df["siren"] = df["siren"].astype(str)
    df["unique_key"] = df["unique_key"].astype(str)

    # Prendre un échantillon de 1000 colonnes
    # sample = df.sample(1000, random_state = 1)

    with st.sidebar:
        st.title("Bénéficiaires effectifs")
        st.divider()

    net = Network(notebook = False, cdn_resources = "remote",
                bgcolor = "#222222",
                font_color = "white",
                height = "750px",
                width = "100%",
    )
    nodes = list(set([*df.unique_key,*df.siren]))
    edges = df.values.tolist()
    net.add_nodes(nodes)
    net.add_edges(edges)
    net.show("graph.html")

    st.write("Placeholder")
