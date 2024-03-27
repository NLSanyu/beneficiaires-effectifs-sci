"""
Visualisation des données avec Streamlit
"""

import streamlit as st

from data_analysis.inpi import fetch_and_filter_data, plot_relationships

with st.sidebar:
    st.title("Bénéficiaires effectifs")
    st.divider()

    names_to_filter = st.text_input("Saisissez un à trois nom(s) de famille, séparés par le virgules :", "DUPONT").split(", ")
    st.divider()

    st.write("Noms :", (name for name in names_to_filter))
    df = fetch_and_filter_data(names_to_filter)
    
st.write(df.head())

graphe = plot_relationships(df)
st.pyplot(graphe)
