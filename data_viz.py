import pandas as pd
from mapping import dict_plotly
import plotly.express as px

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
                                    "<b>Candidat arrivé en tête :</b> %{customdata[4]}<br>"+
                                    "<b>Nuance :</b> %{customdata[7]}")
    
    fig.update_layout(
        legend_title_text="",
        legend=dict(yanchor="top", y=0.98, xanchor="right", x=0.99),
        mapbox=dict(center=dict(lat=48.8566, lon=2.3522), zoom=12,
                    bounds=dict(west=2.1441, east=2.5699, south=48.056, north=49.0021))
    )

    return fig