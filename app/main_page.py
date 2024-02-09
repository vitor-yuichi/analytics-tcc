import streamlit as st
import pandas as pd 
import numpy as np
import os 
from plots.folium_maps import plot_floods_folium
from widgets.date_widgets import set_date_widget

## ----DADOS TEMPORARIOS---##
##-----------------------------##
floods = pd.read_excel(r'/home/ayumi/final_project_university/analytics-project/analytics-tcc/app/database/floods.xlsx')

##-----------------------------##


# Using "with" notation
with st.sidebar:
    #"""Logo imagem UNESP"""
    st.image(os.path.abspath('assets/imgs/AV01F-9EiLtRWpK-transformed.png'), caption = 'Universidade Estadual de São Paulo')
    add_radio = st.radio(
        "Choose a shipping method",
        ("Standard (5-15 days)", "Express (2-5 days)")
    )
    

# Using object notation
add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone")
)


    
st.header("Alagamentos em São Paulo em 2019", divider = 'blue' )

col1, col2 = st.columns(2)




with col1:
    st.metric(label = 'Alagamentos', value = len(floods))

with col1: 
    set_date_widget(floods)
    

