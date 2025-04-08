import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from filter_df import filter_dataframe
import os

color_nuance = {
    'UG': [255, 0, 84], 
    'REC': [0, 29, 61], 
    'EXG': [208, 0, 0], 
    'ENS': [114, 9, 183], 
    'LR': [58, 12, 163], 
    'RN': [0, 53, 102], 
    'DIV': [173, 181, 189], 
    'DVD': [63, 55, 201], 
    'REG': [234, 200, 188], 
    'DVC': [108, 117, 125],
    'ECO': [118, 200, 147], 
    'DVG': [232, 93, 4], 
    'UXD': [0, 0, 0], 
    'EXD': [17, 0, 28],
    'DSV': [53, 1, 44]
}
election_name_clean = {
    "2024_t1_legislatives": "2024-Législatives-T1",
    "2024_t2_legislatives": "2024-Législatives-T2",
    "2024_europeennes": "2024-Européennes",
    "2022_t1_legislatives": "2022-Législatives-T1",
    "2022_t2_legislatives": "2022-Législatives-T2",
    "2022_t1_presidentielles": "2022-Présidentielles-T1",
    "2022_t2_presidentielles": "2022-Présidentielles-T2",
    "2020_t1_municipales": "2020-Municipales-T1",
    "2020_t2_municipales": "2020-Municipales-T2",
    "2019_europeennes": "2019-Européennes",
    "2017_t1_legislatives": "2017-Législatives-T1",
    "2017_t2_legislatives": "2017-Législatives-T2",
    "2017_t1_presidentielles": "2017-Présidentielles-T1",
    "2017_t2_presidentielles": "2017-Présidentielles-T2",
    "2014_t1_municipales": "2014-Municipales-T1",
    "2014_t2_municipales": "2014-Municipales-T2"
}

election_order = {
    "2024_t1_legislatives": 1,
    "2024_t2_legislatives": 0,
    "2024_europeennes": 2,
    "2022_t1_legislatives": 4,
    "2022_t2_legislatives": 3,
    "2022_t1_presidentielles": 6,
    "2022_t2_presidentielles": 5,
    "2020_t1_municipales": 8,
    "2020_t2_municipales": 7,
    "2019_europeennes": 9,
    "2017_t1_legislatives": 11,
    "2017_t2_legislatives": 10,
    "2017_t1_presidentielles": 13,
    "2017_t2_presidentielles": 12,
    "2014_t1_municipales": 15,
    "2014_t2_municipales": 14
}

dict_plotly = {'Ensemble ! (Majorité présidentielle)': 'rgb(114, 9, 183)',
 'Union de la Gauche': 'rgb(255, 0, 84)',
 'Divers droite': 'rgb(63, 55, 201)',
 'Divers gauche': 'rgb(232, 93, 4)',
 'Divers centre': 'rgb(108, 117, 125)',
 'Liste Union de la Gauche':'rgb(255, 0, 84)',
 'Liste Union de la Droite':'rgb(58, 12, 163)',
 'Liste Union du Centre':'rgb(108, 117, 125)',
 'Liste divers droite':'rgb(63, 55, 201)',
 'Nouvelle union populaire écologique et sociale': 'rgb(255, 186, 8)',
 'La France insoumise':'rgb(157, 2, 8)',
 'Rassemblement National':'rgb(34, 34, 59)',
 'Les Républicains':'rgb(58, 12, 163)',
 'La République en marche': 'rgb(114, 9, 183)',
 'Socialiste': 'rgb(232, 93, 4)',
 'Modem': 'rgb(108, 117, 125)',
 'Liste Union pour un Mouvement Populaire':'#0466c8',
 'Union des Démocrates et Indépendants': 'rgb(108, 117, 125)',
 'LA FRANCE INSOUMISE':'rgb(157, 2, 8)',
 'RENAISSANCE': 'rgb(114, 9, 183)',
 'EUROPE ÉCOLOGIE': 'rgb(56, 176, 0)',
 'PRENEZ LE POUVOIR': 'rgb(34, 34, 59)'
 }

def map_results(data_source: pd.DataFrame):
    
    customdata = [
        "election_clean",
        "adresse_bv",
        "inscrits",
        "perc_abstentions",
        "nom_cand_ou_liste",
        "intitulé_hover",
        "perc_voix_exprimes",
        "Libellé",
        "id_brut_bv_reu"
    ]

    fig = px.scatter_mapbox(
        data_source,
        lat="latitude",
        lon="longitude",
        color="Libellé",
        mapbox_style="open-street-map",
        size="size",
        size_max=3,
        color_discrete_map=dict_plotly,
        width=1400,
        height=1000,
        custom_data=customdata
    )

    fig.update_traces(hovertemplate="<b>ID Bureau de vote :</b> %{customdata[8]}<br>"+
                                    "<b>Election :</b> %{customdata[0]}<br>"+
                                    "<b>Bureau de vote :</b> %{customdata[1]}<br>"+
                                    "<b>N° inscrits :</b> %{customdata[2]}<br>"+
                                    "<b>Abstention :</b> %{customdata[3]}%<br>"+
                                    "<b>% voix exprimées :</b> %{customdata[6]}%<br>"+
                                    "<b>Score :</b> %{customdata[4]}<br>"+
                                    "<b>Nuance :</b> %{customdata[7]}")
    
    fig.update_layout(
        legend_title_text="",
        legend=dict(yanchor="top", y=0.98, xanchor="right", x=0.99),
        mapbox=dict(center=dict(lat=48.8566, lon=2.3522), zoom=12,
                    bounds=dict(west=2.1441, east=2.5699, south=48.056, north=49.0021))
    )

    return fig


st.cache_data()
def st_load_data():
    df = pd.read_parquet(os.path.join("data", "st_source", "st_results_per_adress.parquet"))
    df["election_clean"] = df["election"].map(election_name_clean)
    df["election_order"] = df["election"].map(election_order)
    df_results_per_adress = df.query("type != 'Bureau de vote'")
    # df_results_per_adress["color"] = df_results_per_adress["Libellé"].map(dict_plotly)
    df_results_per_adress.sort_values(by=["election_order"], ascending=False, inplace=True)
    df_results_per_bv = pd.read_parquet(os.path.join("data", "st_source", "st_results_per_bv.parquet"))
    df_results_per_bv["election_order"] = df_results_per_bv["election"].map(election_order)
    return df_results_per_adress, df_results_per_bv

# Streamlit app
st.set_page_config(
    page_title="carte_elections_paris",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🗳️ Résultats des élections locales et nationales à Paris")
st.write("""
    💡 Depuis 2019, un fichier de correspondance entre les **bureaux de vote** et \
    les **adresses des électeurs** est élaboré à partir du Répertoire Electoral Unique (REU). \
    Ce fichier est mis à jour tous les 5 ans. ([source](https://www.data.gouv.fr/fr/datasets/bureaux-de-vote-et-adresses-de-leurs-electeurs/))

    🗺️ Chaque point sur la carte représente ainsi l’**adresse d’un électeur** \
    et la couleur du point le **résultat du bureau de vote (candidat arrivé en tête)** auquel l’électeur est rattaché.

    📬 Tous les résultats des élections **municipales, présidentielles, législatives et européennes depuis 2014** sont inclus.
    """)

st.cache_data()
def get_map(data):
    map_plotly = map_results(data)
    return map_plotly

geodata_final_copy_adresses_only, results_per_bv = st_load_data()

# Selection Box
selected_election = st.selectbox(
    label="Sélectionner une élection", 
    options = geodata_final_copy_adresses_only["election_clean"].unique(),
    index = len(geodata_final_copy_adresses_only["election_clean"].unique()) - 1
    )

# Filter data based on selection
filtered_data = geodata_final_copy_adresses_only[geodata_final_copy_adresses_only["election_clean"] == selected_election]

if not filtered_data.empty:
    st.plotly_chart(get_map(filtered_data), use_container_width=True, config={"scrollZoom": True})

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


