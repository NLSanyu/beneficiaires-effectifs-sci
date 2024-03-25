"""
Visualisation des données avec Streamlit
"""

import streamlit as st


with st.sidebar:
    st.title("Bénéficiaires effectifs")
    st.divider()

    data_option = st.radio(
        "Choix de type de recherche",
        ["Par nom du bénéficiaire effectif", "Par entreprise"],
        captions=[
            "Nom du bénéficiaire effectif",
            "Siren de l'entreprise"
        ]
    )

    if data_option == "Par nom du bénéficiaire effectif":
        input_nom = st.text_input("Saisir un nom", "XYZ")
    else:
        input_siren = st.text_input("Saisir un numero SIREN", "123456789")


if data_option == "Par nom du bénéficiaire effectif":
    pass
else:
    pass
