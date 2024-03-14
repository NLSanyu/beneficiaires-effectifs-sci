"""
Visualisation des données par par nom ou par entreprise
"""

import streamlit as st
from recherche import recherche_par_nom, recherche_par_entreprise


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
        input_nom = st.text_input("Saisir un nom", "Xavier Niel") # placeholder Xavier Niel
    else:
        input_siren = st.text_input("Saisir un numero SIREN", "444979314") # placeholder 444979314


if data_option == "Par nom du bénéficiaire effectif":
    nom, beneficiaires_list = recherche_par_nom(input_nom)
    st.subheader(nom)
    for b in beneficiaires_list:
        st.write(b)
else:
    nom_entreprise, beneficiaires_list = recherche_par_entreprise(input_siren)
    st.subheader(nom_entreprise)
    for b in beneficiaires_list:
        st.write(b)
