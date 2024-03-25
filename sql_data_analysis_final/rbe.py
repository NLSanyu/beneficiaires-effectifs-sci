import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import networkx as nx
import streamlit as st

def prep_data():
    df = pd.read_csv("rbe.csv")
    print(df.shape)

    # # Assurez-vous que 'df' et 'final_ubo_df_fixed' sont correctement chargés et préparés
    # df['unique_key'] = df['nom'].str.upper() + "_" + df['prenoms'].apply(lambda x: x.split(", ")[0].upper()) + "_" + df['date_naissance']

    # # Convertir les listes en strings pour une comparaison directe si nécessaire
    # final_ubo_df_fixed['siren_str'] = final_ubo_df_fixed['siren'].apply(lambda x: ', '.join(map(str, x)))

    # # Calculer le nombre de correspondances
    # matches = df['unique_key'].isin(final_ubo_df_fixed['unique_id']).sum()

    # print(f"Nombre de personnes présentes dans les deux bases : {matches}")

    # # Filtrer df pour obtenir seulement les entrées correspondantes
    # matching_persons_df = df[df['unique_key'].isin(final_ubo_df_fixed['unique_id'])]

    # # Afficher les premières lignes du DataFrame filtré pour vérification
    # print(matching_persons_df.head())

    G = nx.Graph()

    # G est votre graphe
    adjacency_matrix_sparse = nx.adjacency_matrix(G)

    # Conversion en matrice dense, si nécessaire
    adjacency_matrix_dense = adjacency_matrix_sparse.todense()

    # Maintenant, `adjacency_matrix_dense` est votre matrice symétrique où
    # 1 indique une connexion directe et 0 l'absence de connexion.

    print(adjacency_matrix_sparse)

    # Création des étiquettes à partir du DataFrame df
    labels = df.apply(lambda row: f"{row['nom']} {row['prenoms']} {row['date_naissance']}", axis=1).tolist()

    # Mise à jour des indices et des colonnes du DataFrame de la sous-matrice
    df_submatrix.index = labels[:len(df_submatrix.index)]
    df_submatrix.columns = labels[:len(df_submatrix.columns)]

    print(df_submatrix)
    
    # Rechercher les nœuds dont l'identifiant commence par "SARKOZY"
    sarkozy_nodes = [node for node in G.nodes if node.startswith("SARKOZY")]

    # Afficher les identifiants des nœuds trouvés
    for node_id in sarkozy_nodes:
        print(f"Nœud trouvé: {node_id}")

    # Si vous souhaitez également obtenir les données associées à ces nœuds
    for node_id in sarkozy_nodes:
        node_data = G.nodes[node_id]
        print(f"Data for {node_id}: {node_data}")


    # Identifiant unique pour Nicolas Sarkozy
    nicolas_id = "SARKOZY DE NAGY-BOCSA_NICOLAS_1955-01"

    # Obtenir tous les voisins directs de Nicolas Sarkozy dans le graphe
    neighbors = list(G[nicolas_id])

    # Ajouter Nicolas Sarkozy lui-même à la liste pour l'inclure dans le sous-graphe
    nodes_to_include = neighbors + [nicolas_id]

    # Créer un sous-graphe avec Nicolas Sarkozy et ses voisins directs
    subgraph = G.subgraph(nodes_to_include)

    # Dessiner le sous-graphe
    plt.figure(figsize=(15, 15))
    nx.draw(subgraph, with_labels=True, node_color='lightblue', edge_color='gray', font_weight='bold')
    plt.title("Sous-graphe autour de Nicolas Sarkozy")
    plt.show()

if __name__ == "__main__":
    prep_data()
    # with st.sidebar:
    #     st.title("Bénéficiaires effectifs")
    #     st.divider()
    
    # st.write("Placeholder")
