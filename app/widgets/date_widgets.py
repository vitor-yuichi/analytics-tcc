import datetime
import streamlit as st
import pandas as pd

def set_date_widget(df, column):
    initial_date = pd.to_datetime(df[column]).dt.date.min()
    final_date = pd.to_datetime(df[column]).dt.date.max()
    

    d =  st.date_input(
        "Selecione a série temporal que deseja visualizar",
        (initial_date, datetime.date(initial_date.year, initial_date.month+1, initial_date.day)),
        initial_date,
        final_date,
        format="YYYY-MM-DD",
        on_change=handle_click
    )
    return d