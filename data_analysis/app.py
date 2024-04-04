"""
Visualisation des données avec Streamlit
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set_theme(style="darkgrid")

st.set_page_config(
    page_title="Bénéficiaires effectifs",
    layout="wide",
    initial_sidebar_state="expanded"
)

def get_correspondances():
    """
    Les correspondances entre les deux bases
    """
    matches_df = pd.read_csv("data/matches_inpi_pappers.csv")
    return matches_df

def fetch_analysis_data():
    """
    Les données traitées pour l'analyse
    """
    analysis_df = pd.read_csv("data/inpi_rbe_metadata.csv")
    return analysis_df

with st.sidebar:
    st.title("Projet tutoré de recherche, M2 Gouvernance des Données")
    st.subheader("L'identification des bénéficiaires effectifs des sociétés civiles immobilières (SCI) en utilisant des sources d'open data comme l'API de l'INPI.")

st.title("Exploitaition et analyse des données")
st.divider()

matches = get_correspondances()
st.subheader("1. Croisement des bénéficiaires effectifs des SCI avec les bénéficiaires effectifs des entreprises attributaires d'un marché public")
st.markdown(f"Nombre de personnes présentes dans les deux bases : {len(matches)}")
st.dataframe(matches, use_container_width=True)

st.divider()

analyse = fetch_analysis_data()

st.subheader("2. Les communes avec le plus grand nombre d'entreprises")
nombre_de_communes = st.number_input("Choisissez un nombre de communes à afficher", min_value=2, max_value=20, value=10)
val_count  = analyse["commune"].value_counts()[:nombre_de_communes]
fig = plt.figure(figsize=(10,5))
sns.barplot(val_count)
plt.xticks(rotation = 70)
st.pyplot(fig)

st.divider()

st.subheader("3. Les sociétés étrangères : y en a-t-il dans cette base de données?")
fig, ax = plt.subplots(figsize=(15, 5))
sns.countplot(data=analyse, x=analyse["societe_etrangere"])
plt.xticks(rotation = 70)
st.pyplot(fig)
st.write("La reponse est non.")

st.divider()

st.subheader("4. Les formes juridiques des entreprises")
fig, ax = plt.subplots(figsize=(15, 5))
sns.countplot(data=analyse, x=analyse["forme_juridique"], order=analyse["forme_juridique"].value_counts().index)
plt.xticks(rotation = 70)
st.pyplot(fig)
