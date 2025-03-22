import pandas as pd
import plotly.express as px
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
    "2024_t1_legislatives": "2024-Législatives-Tour 1",
    "2024_t2_legislatives": "2024-Législatives-Tour 2"
}

dict_plotly = {'Ensemble ! (Majorité présidentielle)': 'rgb(114, 9, 183)',
 'Union de la Gauche': 'rgb(255, 0, 84)',
 'Divers droite': 'rgb(63, 55, 201)',
 'Divers gauche': 'rgb(232, 93, 4)',
 'Divers centre': 'rgb(108, 117, 125)'}

def map_results(data_source: pd.DataFrame):
    
    customdata = [
        "election_clean",
        "adresse_bv",
        "inscrits",
        "perc_abstentions",
        "nom_prenom",
        "perc_voix_exprimes",
        "Libellé"
    ]

    fig = px.scatter_mapbox(
        data_source,
        lat="latitude",
        lon="longitude",
        color="Libellé",
        animation_frame="election_clean",
        mapbox_style="open-street-map",
        zoom=4,
        center={"lat": 48.8566, "lon": 2.3522},
        size="size",
        size_max=3,
        color_discrete_map=dict_plotly,
        width=1400,
        height=1000,
        custom_data=customdata
    )

    fig.update_traces(
        hovertemplate=
        "<b>Election :</b> %{customdata[0]}<br>"+
        "<b>Bureau de vote :</b> %{customdata[1]}<br>"+
        "<b>Nb inscrits :</b> %{customdata[2]}<br>"+
        "<b>Abstention :</b> %{customdata[3]}<br>"+
        "<b>Candidat arrivé en tête :</b> %{customdata[4]}<br>"+
        "<b>Score :</b> %{customdata[5]}<br>"+
        "<b>Nuance :</b> %{customdata[6]}"
    )
    
    fig.update_layout(
        mapbox_bounds={"west": 2.25, "east": 2.45, "south": 48.81, "north": 48.91},
        legend=dict(
            orientation="v",
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99,
            title=""
        ),
        updatemenus=[{
            "buttons": [],
            "direction": "left",
            "pad": {"r": 10, "t": 10},
            "showactive": False,
            "type": "buttons",
            "x": 0.1,
            "xanchor": "right",
            "y": 1.12,
            "yanchor": "top"
        }],
        sliders=[{
            "active": 0,
            "yanchor": "top",
            "xanchor": "left",
            "currentvalue": {
                "font": {"size": 20, "color": "black"},
                "prefix": '',
                "visible": True,
                "xanchor": "center"
            },
            "transition": {"duration": 500, "easing": "linear"},
            "pad": {"b": 10, "t": 50},
            "len": 0.85,
            'x': 0.1,
            'y': 1.2,
            'steps': [{
                'args': [[year], {'frame': 
                                {'duration': 500, 'redraw': True},
                                'mode': 'immediate', 
                                'transition': {'duration': 500, 'easing': 'linear'}}],
                'label': year,
                'method': 'animate'
            } for year in data_source['election_clean'].unique()]
        }]
    )
    
    return fig
   
st.set_page_config(
    page_title="carte_elections_paris",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.cache_data()
def st_load_data():
    df = pd.read_parquet(os.path.join("data", "output", "st_results_per_adress.parquet"))
    df["election_clean"] = df["election"].map(election_name_clean)
    df_results_per_adress = df.query("type != 'Bureau de vote'")
    df_results_per_bv = pd.read_parquet(os.path.join("data", "output", "st_results_per_bv.parquet"))
    return df_results_per_adress, df_results_per_bv

geodata_final_copy_adresses_only, results_per_bv = st_load_data()

# Streamlit app
st.title("🗳️ Résultats des élections locales et nationales à Paris")
st.write("""
    💡 Depuis 2019, un fichier de correspondance entre les **bureaux de vote** et \
    les **adresses des électeurs** est élaboré à partir du Répertoire Electoral Unique (REU). \
    Ce fichier est mis à jour tous les 5 ans. ([source](https://www.data.gouv.fr/fr/datasets/bureaux-de-vote-et-adresses-de-leurs-electeurs/))

    🗺️ Chaque point sur la carte représente ainsi l’**adresse d’un électeur** \
    et la couleur du point le **résultat du bureau de vote** auquel l’électeur est rattaché.

    📬 À ce stade, seuls les résultats des **premier et second tours des élections législatives anticipées de 2024** \
    sont intégrés (les résultats des élections antérieures seront ajoutés ultérieurement).
    """)

st.cache_data()
def get_map():
    map_plotly = map_results(geodata_final_copy_adresses_only)
    return map_plotly

st.plotly_chart(get_map(), use_container_width=True, config={"scrollZoom": True})

with st.container(border=True):
    st.subheader("📊 Données détaillées des résultats par bureau de vote")
    results_per_bv.sort_values(
        by=["id_brut_bv_reu","election","perc_voix_exprimes"],
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
            "nom_prenom",
            "Libellé",
            "perc_voix_exprimes",
            "elu"
        ]
    ].reset_index(drop=True)

    st.dataframe(filter_dataframe(st_df), hide_index=True)


