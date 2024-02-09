import datetime
import streamlit as st
import pandas as pd

def set_date_widget(date_event):
    initial_date = pd.to_datetime(date_event.DATA).dt.date.min()
    final_date = pd.to_datetime(date_event.DATA).dt.date.max()
    

    d = st.date_input(
        "Selecione a série temporal que deseja visualizar",
        (initial_date, datetime.date(initial_date.year, initial_date.month+1, initial_date.day)),
        initial_date,
        final_date,
        format="YYYY-MM-DD",
    )
    return d