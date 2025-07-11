import streamlit as st
from utils import filter_dataframe,radio_button_munic_2020, radio_button_pres_2022 
from data_source import st_load_data_all_elections, st_load_data_source, st_load_data_spec_analysis, get_map, get_map_spec

# Configuration of the page
st.set_page_config(
    page_title="carte_elections_paris",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Loading data
geodata_final_copy_adresses_only = st_load_data_all_elections()
results_per_bv = st_load_data_source()
geodata_final_specific_analysis = st_load_data_spec_analysis()
    
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

tab1, tab2, tab3, tab4 = st.tabs([
    "Candidats arrivés en tête - 2014-2024",
    "Focus 1er tour Présidentielles 2022",
    "Focus 1er tour Municipales 2020", 
    "Données source"
    ])

with tab1:

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

with tab2:
    
    election_tab2 = "2022-Présidentielles-T1"
    plac2, candidate_tab2 = radio_button_pres_2022(election_tab2)
    
    # Filtering data
    filtered_spec_data_tab2 = geodata_final_specific_analysis.query("election_clean == @election_tab2").query("candidat_ou_liste == @candidate_tab2")
    
    # Showing map
    if not filtered_spec_data_tab2.empty:
        st.plotly_chart(get_map_spec(filtered_spec_data_tab2), use_container_width=True, config={"scrollZoom": True}, key="pres_t1")

with tab3:
    
    election_tab3 = "2020-Municipales-T1"
    plac3, candidate_tab3 = radio_button_munic_2020(election_tab2)
    
    # Filtering data
    candidate_tab3 = candidate_tab3.replace(" (CEDRIC VILLANI)", "")
    filtered_spec_data_tab3 = geodata_final_specific_analysis.query("election_clean == @election_tab3").query("candidat_ou_liste == @candidate_tab3")
    
    # Showing map
    if not filtered_spec_data_tab3.empty:
        st.plotly_chart(get_map_spec(filtered_spec_data_tab3), use_container_width=True, config={"scrollZoom": True}, key="munic_t1")

with tab4:
    
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


