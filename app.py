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
}

election_order = {
    "2024_t1_legislatives": 7,
    "2024_t2_legislatives": 8,
    "2024_europeennes": 6,
    "2022_t1_legislatives": 4,
    "2022_t2_legislatives": 5,
    "2022_t1_presidentielles": 2,
    "2022_t2_presidentielles": 3,
    "2020_t1_municipales": 0,
    "2020_t2_municipales": 1,
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
 'La République en marche': 'rgb(127, 85, 57)',
 }

def map_results(data_source: pd.DataFrame):
    
    customdata = [
        "election",
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
        animation_frame="election",
        mapbox_style="open-street-map",
        zoom=4,
        center={"lat": 48.8566, "lon": 2.3522},
        size="size",
        size_max=3,
        # color_discrete_map=dict_plotly,
        width=1400,
        height=1000,
        # custom_data=customdata
    )

    # fig.update_traces(hovertemplate="<b>ID Bureau de vote :</b> %{customdata[8]}<br>"+
    #     "<b>Election :</b> %{customdata[0]}<br>"+
    #     "<b>Bureau de vote :</b> %{customdata[1]}<br>"+
    #     "<b>Nb inscrits :</b> %{customdata[2]}<br>"+
    #     "<b>Abstention :</b> %{customdata[3]}<br>"+
    #     "<b>%{customdata[5]} :</b> %{customdata[4]}<br>"+
    #     "<b>Score :</b> %{customdata[6]}<br>"+
    #     "<b>Nuance :</b> %{customdata[7]}")
    # for f in fig.frames:
    #     for i in range(len(f.data)):
    #         f.data[i].update(hovertemplate="<b>ID Bureau de vote :</b> %{customdata[8]}<br>"+
    #         "<b>Election :</b> %{customdata[0]}<br>"+
    #         "<b>Bureau de vote :</b> %{customdata[1]}<br>"+
    #         "<b>Nb inscrits :</b> %{customdata[2]}<br>"+
    #         "<b>Abstention :</b> %{customdata[3]}<br>"+
    #         "<b>%{customdata[5]} :</b> %{customdata[4]}<br>"+
    #         "<b>Score :</b> %{customdata[6]}<br>"+
    #         "<b>Nuance :</b> %{customdata[7]}")
    
    #
    return fig

def map_result_bis(data_source):
    data = []
    for election_year in data_source["election"].unique():
        df_filtered = data_source[data_source["election"] == election_year]
        scatter = go.Scattermapbox(
            lat=df_filtered["latitude"],
            lon=df_filtered["longitude"],
            mode="markers",
            marker=dict(
                size=df_filtered["size"],
                sizemode="diameter",
                sizemin=3,
                color=[dict_plotly[label] for label in df_filtered["Libellé"]],
            ),
            customdata=df_filtered[['Libellé', 'election']].values,
            name=f"Election {election_year}",
            hoverinfo="text",
            hovertext=df_filtered["Libellé"],
            visible=(election_year == data_source["election"].min())
        )
        data.append(scatter)

    fig = go.Figure(data=data)
    fig.update_layout(
        mapbox=dict(
            style="open-street-map",
            zoom=4,
            center=dict(lat=48.8566, lon=2.3522)
        ),
        updatemenus=[
            dict(
                buttons=[
                    dict(
                        label=str(year),
                        method="update",
                        args=[{"visible": [election_year == year for election_year in data_source["election"].unique()]}]
                    )
                    for year in data_source["election"].unique()
                ],
                direction="down",
                showactive=True,
                x=0.5,
                xanchor="center",
                y=1.15,
                yanchor="top"
            )
        ],
        width=1400,
        height=1000
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
    df = pd.read_parquet(os.path.join("data", "st_source", "st_results_per_adress.parquet"))
    # df["election_clean"] = df["election"].map(election_name_clean)
    # df["election_order"] = df["election"].map(election_order)
    df_results_per_adress = df.query("type != 'Bureau de vote'")
    df_results_per_adress = df_results_per_adress[df_results_per_adress["election"].isin(["2022_t1_presidentielles","2022_t2_presidentielles"])]
    # df_results_per_adress["color"] = df_results_per_adress["Libellé"].map(dict_plotly)
    # df_results_per_adress.sort_values(by=["election_order"], inplace=True)
    df_results_per_bv = pd.read_parquet(os.path.join("data", "st_source", "st_results_per_bv.parquet"))
    df_results_per_bv["election_order"] = df_results_per_bv["election"].map(election_order)
    return df_results_per_adress, df_results_per_bv

geodata_final_copy_adresses_only, results_per_bv = st_load_data()
geodata_final_copy_adresses_only.query("longitude==2.387518")
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

# st.cache_data()
def get_map():
    map_plotly = map_result_bis(geodata_final_copy_adresses_only)
    return map_plotly

# print(geodata_final_copy_adresses_only.query("election_clean=='2022-Présidentielles-T2'")["Libellé"].unique())
st.plotly_chart(get_map(), use_container_width=True, config={"scrollZoom": True})

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


