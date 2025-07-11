from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
import pandas as pd
import streamlit as st


def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    modify = st.checkbox("Ajouter des filtres")

    if not modify:
        return df

    df = df.copy()

    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filtrer selon", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 100:
                user_cat_input = right.multiselect(
                    f"Valeur pour {column}",
                    df[column].unique(),
                    # default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Valeur pour {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Text recherché dans {column}",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.lower().str.contains(user_text_input.lower())]

    return df

# def radio_button_election():
#     plac1 = st.empty()
#     election = plac1.radio(
#         "Choisir une élection :",
#         ["2020-Municipales-T1","2022-Présidentielles-T1"],
#         index=1,
#         horizontal=True
#     )
#     return plac1, election

def radio_button_pres_2022(election:str):
    plac2 = st.empty()
    text_button = "Choisir un candidat :"
    choices = [
            "MACRON Emmanuel",
            "PÉCRESSE Valérie",
            "MACRON Emmanuel+PÉCRESSE Valérie"
            ]
    candidate = plac2.radio(
        text_button,
        choices,
        index=0,
        horizontal=True,
        key="pres_2022"
    )
    
    return plac2, candidate

def radio_button_munic_2020(election:str):
    plac3 = st.empty()
    text_button = "Choisir une liste :"
    choices = [
            "ENSEMBLE POUR PARIS AVEC AGNES BUZYN",
            "LE NOUVEAU PARIS (CEDRIC VILLANI)",
            "ENGAGES POUR CHANGER PARIS AVEC RACHIDA DATI",
            "ENSEMBLE POUR PARIS AVEC AGNES BUZYN+LE NOUVEAU PARIS (CEDRIC VILLANI)",
            "ENSEMBLE POUR PARIS AVEC AGNES BUZYN+LE NOUVEAU PARIS (CEDRIC VILLANI)+ENGAGES POUR CHANGER PARIS AVEC RACHIDA DATI"
            ]
    candidate = plac3.radio(
        text_button,
        choices,
        index=0,
        horizontal=True,
        key="munic_2020"
    )
    
    return plac3, candidate