import pandas as pd
from mapping import dict_plotly, dict_echelle_score
import plotly.express as px
import plotly.graph_objects as go

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

    fig.update_traces(hovertemplate="<b>Election :</b> %{customdata[0]}<br>"+
                                    "<b>ID Bureau de vote :</b> %{customdata[8]}<br>"+
                                    "<b>Bureau de vote :</b> %{customdata[1]}<br>"+
                                    "<b>Candidat ou liste :</b> %{customdata[4]}<br>"+
                                    "<b>Nuance :</b> %{customdata[7]}<br>"+
                                    "<b>Score :</b> %{customdata[6]}%<br>"+
                                    "<b>Abstention :</b> %{customdata[3]}%<br>"+
                                    "<b>N° inscrits :</b> %{customdata[2]}<br>")
    
    fig.update_layout(
        legend_title_text="",
        legend=dict(yanchor="top", y=0.98, xanchor="right", x=0.99),
        mapbox=dict(center=dict(lat=48.8566, lon=2.3522), zoom=12,
                    bounds=dict(west=2.1441, east=2.5699, south=48.056, north=49.0021))
    )

    return fig

def map_results_spec(data_source: pd.DataFrame):
    
    customdata = [
        "election_clean",
        "adresse_bv",
        "inscrits",
        "perc_abstentions",
        "candidat_ou_liste",
        "perc_voix_exprimes",
        "id_brut_bv_reu",
        "score_arr_moyen"
    ]

    bucket_order = ['[<=10%]', '[11%-15%]', '[16%-20%]','[21%-25%]', '[26%-30%]', '[>30%]']
    data_source['echelle_score'] = pd.Categorical(data_source['echelle_score'], categories=bucket_order, ordered=True)
    data_source.sort_values(by='echelle_score', inplace=True)
    
    fig = px.scatter_mapbox(
        data_source,
        lat="latitude",
        lon="longitude",
        color="echelle_score",
        mapbox_style="open-street-map",
        size="size",
        size_max=3,
        color_discrete_map=dict_echelle_score,
        width=1400,
        height=1000,
        custom_data=customdata
    )

    fig.update_traces(hovertemplate="<b>Election :</b> %{customdata[0]}<br>"+
                                    "<b>ID Bureau de vote :</b> %{customdata[6]}<br>"+
                                    "<b>Bureau de vote :</b> %{customdata[1]}<br>"+
                                    "<b>Candidat ou liste :</b> %{customdata[4]}<br>"+
                                    "<b>Score :</b> %{customdata[5]}%<br>"+
                                    "<b>Score moyen de l'arrondissement :</b> %{customdata[7]}%<br>"+
                                    "<b>Abstention :</b> %{customdata[3]}%<br>"+
                                    "<b>N° inscrits :</b> %{customdata[2]}<br>")
    
    fig.update_layout(
        legend_title_text="",
        legend=dict(yanchor="top", y=0.98, xanchor="right", x=0.99),
        mapbox=dict(center=dict(lat=48.8566, lon=2.3522), zoom=12,
                    bounds=dict(west=2.1441, east=2.5699, south=48.056, north=49.0021))
    )

    return fig

def map_results_go(data_source: pd.DataFrame):
    # List of fields to include in hover data
    customdata_cols = [
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

    # Prepare customdata array
    customdata = data_source[customdata_cols].values

    # Color mapping by "Libellé"
    traces = []
    for label in data_source["Libellé"].unique():
        df_subset = data_source[data_source["Libellé"] == label]
        subset_customdata = df_subset[customdata_cols].values

        trace = go.Scattermapbox(
            lat=df_subset["latitude"],
            lon=df_subset["longitude"],
            mode="markers",
            marker=dict(
                size=5,
                sizemode="area",
                sizeref=5,  # match px size scaling
                sizemin=1,
                color=dict_plotly[label]
            ),
            name=label,
            customdata=subset_customdata,
            hovertemplate="<b>Election :</b> %{customdata[0]}<br>" +
                          "<b>ID Bureau de vote :</b> %{customdata[8]}<br>" +
                          "<b>Bureau de vote :</b> %{customdata[1]}<br>" +
                          "<b>Candidat ou liste :</b> %{customdata[4]}<br>" +
                          "<b>Nuance :</b> %{customdata[7]}<br>" +
                          "<b>Score :</b> %{customdata[6]}%<br>" +
                          "<b>Abstention :</b> %{customdata[3]}%<br>" +
                          "<b>N° inscrits :</b> %{customdata[2]}<br><extra></extra>"
        )

        traces.append(trace)

    # Create the figure with all traces
    fig = go.Figure(data=traces)

    fig.update_layout(
        mapbox=dict(
            style="open-street-map",
            center=dict(lat=48.8566, lon=2.3522),
            zoom=12,
            bounds=dict(west=2.1441, east=2.5699, south=48.056, north=49.0021)
        ),
        legend_title_text="",
        legend=dict(yanchor="top", y=0.98, xanchor="right", x=0.99),
        width=1400,
        height=1000,
        margin=dict(l=0, r=0, t=0, b=0)
    )

    return fig


def map_results_spec_go(data_source: pd.DataFrame):
    # Define the customdata fields to include in hover
    customdata_cols = [
        "election_clean",
        "adresse_bv",
        "inscrits",
        "perc_abstentions",
        "candidat_ou_liste",
        "perc_voix_exprimes",
        "id_brut_bv_reu",
        "score_arr_moyen",
        "candidat_ou_liste_en_tete",
        "perc_voix_exprimes_vainqueur"
    ]

    # Define and enforce category order for legend
    bucket_order = ['[<=10%]', '[11%-15%]', '[16%-20%]', '[21%-25%]', '[26%-30%]', '[>30%]']
    data_source['echelle_score'] = pd.Categorical(
        data_source['echelle_score'],
        categories=bucket_order,
        ordered=True
    )
    data_source.sort_values(by='echelle_score', inplace=True)

    traces = []

    for bucket in bucket_order:
        df_bucket = data_source[data_source['echelle_score'] == bucket]
        if df_bucket.empty:
            continue

        trace = go.Scattermapbox(
            lat=df_bucket["latitude"],
            lon=df_bucket["longitude"],
            mode="markers",
            marker=dict(
                size=5,
                sizemode="area",
                sizeref=5,
                sizemin=1,
                color=dict_echelle_score[bucket]
            ),
            name=bucket,
            customdata=df_bucket[customdata_cols].values,
            hovertemplate="<b>Election :</b> %{customdata[0]}<br>" +
                          "<b>ID Bureau de vote :</b> %{customdata[6]}<br>" +
                          "<b>Bureau de vote :</b> %{customdata[1]}<br>" +
                          "<b>Candidat ou liste :</b> %{customdata[4]}<br>" +
                          "<b>Score :</b> %{customdata[5]}%<br>" +
                          "<b>Candidat ou liste arrivé(e) en tête :</b> %{customdata[8]}<br>" +
                          "<b>Score candidat ou liste arrivé(e) en tête :</b> %{customdata[9]}%<br>" +
                          "<b>Score moyen de l'arrondissement :</b> %{customdata[7]}%<br>" +
                          "<b>Abstention :</b> %{customdata[3]}%<br>" +
                          "<b>N° inscrits :</b> %{customdata[2]}<br><extra></extra>"
        )

        traces.append(trace)

        # Assemble the figure
    fig = go.Figure(data=traces)

    fig.update_layout(
        mapbox=dict(
            style="open-street-map",
            center=dict(lat=48.8566, lon=2.3522),
            zoom=12,
            bounds=dict(west=2.1441, east=2.5699, south=48.056, north=49.0021)
        ),
        legend_title_text="",
        legend=dict(yanchor="top", y=0.98, xanchor="right", x=0.99),
        width=1400,
        height=1000,
        margin=dict(l=0, r=0, t=0, b=0)
    )

    return fig