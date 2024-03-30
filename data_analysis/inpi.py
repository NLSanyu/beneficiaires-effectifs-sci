"""
Récupérez les données (INPI) du fichier csv et les preparer pour l'analyse
"""
import pandas as pd
import igraph as ig
import matplotlib.pyplot as plt

def fetch_and_filter_data(names_to_filter):
    """
    Récuperer les données du fichier csv et les filtrer par nom
    """
    data = pd.read_csv("data/inpi-rbe.csv")

    if names_to_filter:
        filtered_data = data[data["nom"].isin(names_to_filter)]
        return filtered_data

    return data

def plot_relationships(data):
    """
    Créer une graphe
    """
    g = ig.Graph(directed=False)

    unique_names = data["unique_key"].unique()
    unique_sirens = data["siren"].unique()
    id_mapping = {name: idx for idx, name in enumerate(unique_names)}
    id_mapping.update({siren: idx + len(unique_names) for idx, siren in enumerate(unique_sirens)})

    # g.add_vertices(len(unique_names) + len(unique_sirens))
    vertex_labels = list(unique_names) + list(unique_sirens)
    g.add_vertices(len(vertex_labels))
    g.vs["label"] = vertex_labels

    for _, row in data.iterrows():
        person_id = id_mapping[row["unique_key"]]
        siren_id = id_mapping[row["siren"]]
        g.add_edge(person_id, siren_id)

    visual_style = {
        "vertex_size": 20,
        "vertex_label_dist": 1.5,
        "vertex_label_color": "black",
        "vertex_label_size": 10,
        "edge_width": 1,
        "edge_color": "gray"
    }

    fig, ax = plt.subplots()
    ig.plot(g, target=ax, **visual_style)

    return fig
