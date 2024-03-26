"""
Récupérez les données du fichier csv et les preparer pour l'analyse
"""
import pandas as pd
import matplotlib.pyplot as plt
import igraph as ig
import streamlit as st

def fetch_and_filter_data(noms_pour_filtrer):
    """
    Récuperer les données du fichier csv et les filtrer par nom
    """
    data = pd.read_csv("rbe.csv")

    filtered_data = data[data["nom"].isin(noms_pour_filtrer)]

    return filtered_data

def plot_relationships(data):
    """
    Créer une graphe
    """
    g = ig.Graph(directed=False)
    vertices = set(data["unique_key"]).union(set(data["siren"]))
    g.add_vertices(list(vertices))
    for _, row in data.iterrows():
        g.add_edge(row["unique_key"], row["siren"])

    # Set visual attributes
    visual_style = {
        "vertex_size": 20,
        "vertex_label_dist": 1.5,
        "vertex_label_color": "black",
        "vertex_label_size": 10,
        "edge_width": 1,
        "edge_color": "gray"
    }

    ig.plot(g, **visual_style)

    # relationships = {}
    # for _, row in data.iterrows():
    #     if row["siren"] not in relationships:
    #         relationships[row["siren"]] = set()
    #     relationships[row["siren"]].add(row["unique_key"])

    # plt.figure(figsize=(8, 6))
    # plt.title("Graphe")

    # for siren, personnes in relationships.items():
    #     for personne1 in personnes:
    #         for personne2 in personnes:
    #             if personne1 != personne2:
    #                 plt.plot([personne1, personne2], [siren, siren], marker='o', color='blue')

    # plt.yticks(range(len(relationships)), list(relationships.keys()))
    # plt.xlabel("Personne")
    # plt.ylabel("Siren")
    # plt.grid(axis='x')
    # plt.tight_layout()
    # plt.show()

    # return plt

if __name__ == "__main__":
    exemple_de_noms_pour_filtrage = ["PICOT", "NOBLET", "LEVRAT"]
    df = fetch_and_filter_data(exemple_de_noms_pour_filtrage)

    with st.sidebar:
        st.title("Bénéficiaires effectifs")
        st.divider()

    plot_relationships(df)
