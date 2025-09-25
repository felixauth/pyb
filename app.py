import streamlit as st
from utils import filter_dataframe,radio_button_munic_2020, radio_button_pres_2022, radio_button_munic_2020_subfilter, radio_button_pres_2022_subfilter, filter_focus_df
from data_source import st_load_data_all_elections, st_load_data_source, st_load_data_spec_analysis, get_map, get_map_go,get_map_spec, get_map_spec_go

# Configuration of the page
st.set_page_config(
    page_title="carte_elections_paris",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="expanded"
)
# Getting secrets
USERNAME = st.secrets["USERNAME"]
PASSWORD = st.secrets["PASSWORD"]

# Connexion state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("Connexion requise")
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter"):
        if username == USERNAME and password == PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Identifiants incorrects")
else:
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

        🗺️ Chaque point sur la carte représente ainsi l’**adresse d’un électeur**.
        """)

    tab1, tab2, tab3 = st.tabs([
        "Candidats arrivés en tête - 2014-2024",
        "Focus 1er tour Présidentielles 2022",
        "Focus 1er tour Municipales 2020", 
        # "Données source"
        ])

    with tab1:
        
        st.write("📬 Tous les résultats des élections **municipales, présidentielles, législatives et européennes depuis 2014** sont inclus. \
            La couleur du point indique le **résultat du bureau de vote (candidat arrivé en tête)** auquel l’électeur est rattaché.")
        
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
            st.plotly_chart(get_map_go(filtered_data), use_container_width=True, config={"scrollZoom": True})

    with tab2:
        st.write("📬 Cette carte affiche uniquement les résultats du premier tour de l'élection présidentielle 2022, pour le candidat et le filtre choisis. \
            La couleur du point dépend du score du candidat sélectionné.")
        
        election_tab2 = "2022-Présidentielles-T1"
        plac2, candidate_tab2 = radio_button_pres_2022(election_tab2)
        plac2_b, filter_choice_pres = radio_button_pres_2022_subfilter()
        
        # Filtering data
        # filtered_spec_data_tab2 = geodata_final_specific_analysis.query("election_clean == @election_tab2").query("candidat_ou_liste == @candidate_tab2")
        filtered_spec_data_tab2, mean_score_paris_tab2 = filter_focus_df(geodata_final_specific_analysis, election_tab2, candidate_tab2, filter_choice_pres)
        
        # See mean score Paris
        st.write(f"🎯 Score moyen Paris, tous bureaux de vote : **{mean_score_paris_tab2}%**")
        
        # Showing map
        if not filtered_spec_data_tab2.empty:
            st.plotly_chart(get_map_spec_go(filtered_spec_data_tab2), use_container_width=True, config={"scrollZoom": True}, key="pres_t1")

    with tab3:
        st.write("📬 Cette carte affiche uniquement les résultats du premier tour de l'élection municipale 2020, pour le candidat et le filtre choisis. \
            La couleur du point dépend du score du candidat sélectionné.")
        election_tab3 = "2020-Municipales-T1"
        plac3, candidate_tab3 = radio_button_munic_2020(election_tab2)
        plac3_b, filter_choice_munic = radio_button_munic_2020_subfilter()
        
        # Filtering data
        candidate_tab3 = candidate_tab3.replace(" (CEDRIC VILLANI)", "")
        
        # filtered_spec_data_tab3 = geodata_final_specific_analysis.query("election_clean == @election_tab3").query("candidat_ou_liste == @candidate_tab3")
        filtered_spec_data_tab3, mean_score_paris_tab3 = filter_focus_df(geodata_final_specific_analysis, election_tab3, candidate_tab3, filter_choice_munic)
        
        # See mean score Paris
        st.write(f"🎯 Score moyen Paris, tous bureaux de vote : **{mean_score_paris_tab3}%**")
        
        # Showing map
        if not filtered_spec_data_tab3.empty:
            st.plotly_chart(get_map_spec_go(filtered_spec_data_tab3), use_container_width=True, config={"scrollZoom": True}, key="munic_t1")

    if st.button("Se déconnecter"):
        st.session_state.authenticated = False
        st.rerun()