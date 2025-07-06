import pandas as pd
import streamlit as st
import os
from mapping import election_name_clean, election_order
from data_viz import map_results

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

st.cache_data()
def get_map(data):
    map_plotly = map_results(data)
    return map_plotly