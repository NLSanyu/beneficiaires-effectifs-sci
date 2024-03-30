"""
Visualisation des données avec Streamlit
"""

import pandas as pd
import streamlit as st

from inpi import fetch_and_filter_data
from pappers import fetch_data

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

with st.sidebar:
    st.title("Bénéficiaires effectifs")
    st.divider()

matches = get_correspondances()
st.header("Croisement des bénéficiaires effectifs des SCI avec les bénéficiaires effectifs des entreprises attributaires d'un marché public")
st.markdown(f"Nombre de personnes présentes dans les deux bases : {len(matches)}")
st.dataframe(matches, use_container_width=True)
