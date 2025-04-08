import streamlit as st
from utils import filter_dataframe
from data_source import st_load_data, get_map

# Configuration of the page
st.set_page_config(
    page_title="carte_elections_paris",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and introduction
st.title("🗳️ Résultats des élections locales et nationales à Paris")
st.write("""
    💡 Depuis 2019, un fichier de correspondance entre les **bureaux de vote** et \
    les **adresses des électeurs** est élaboré à partir du Répertoire Electoral Unique (REU). \
    Ce fichier est mis à jour tous les 5 ans. ([source](https://www.data.gouv.fr/fr/datasets/bureaux-de-vote-et-adresses-de-leurs-electeurs/))

    🗺️ Chaque point sur la carte représente ainsi l’**adresse d’un électeur** \
    et la couleur du point le **résultat du bureau de vote (candidat arrivé en tête)** auquel l’électeur est rattaché.

    📬 Tous les résultats des élections **municipales, présidentielles, législatives et européennes depuis 2014** sont inclus.
    """)


# Loading data
geodata_final_copy_adresses_only, results_per_bv = st_load_data()

# Selection Box for election choice
selected_election = st.selectbox(
    label="Sélectionner une élection", 
    options = geodata_final_copy_adresses_only["election_clean"].unique(),
    index = len(geodata_final_copy_adresses_only["election_clean"].unique()) - 1
    )

# Filter data based on selection
filtered_data = geodata_final_copy_adresses_only[geodata_final_copy_adresses_only["election_clean"] == selected_election]

# Showing map
if not filtered_data.empty:
    st.plotly_chart(get_map(filtered_data), use_container_width=True, config={"scrollZoom": True})

# Showing detailed results
with st.container(border=True):
    st.subheader("📊 Données détaillées des résultats par bureau de vote")
    results_per_bv.sort_values(
        by=["election_order","id_brut_bv_reu","perc_voix_exprimes"],
        ascending=[True, True, False],
        inplace=True
        )
    st_df = results_per_bv[
        [
            "election",
            "id_brut_bv_reu",
            "adresse_bv",
            "nom_bv",
            "inscrits",
            "perc_abstentions",
            "nom_cand_ou_liste",
            "Libellé",
            "perc_voix_exprimes"
        ]
    ].reset_index(drop=True)

    st.dataframe(filter_dataframe(st_df), hide_index=True)


