import streamlit as st
import pandas as pd 
import numpy as np
from streamlit_folium import st_folium
import datetime

import os 
## BIBLIOTECAS PERSONALIZADAS##
from plots.folium_maps import plot_floods_folium
from widgets.date_widgets import set_date_widget
##--------------------------##

#---------------SESSION STATE ------------------
"st.session_state object", st.session_state





## ----DADOS TEMPORARIOS---##
##-----------------------------##

def import_floods():
    floods = pd.read_excel(r'/home/ayumi/final_project_university/analytics-project/analytics-tcc/app/database/floods.xlsx')
    return floods

floods = import_floods()
##-----------------------------##

##------------------------SIDE BAR------------------------#
# Using "with" notation
with st.sidebar:
    #"""Logo imagem UNESP"""
    st.image(os.path.abspath('assets/imgs/AV01F-9EiLtRWpK-transformed.png'), 
             caption = 'Universidade Estadual de São Paulo')
    add_radio = st.radio(
        "Choose a shipping method",
        ("Standard (5-15 days)", "Express (2-5 days)")
    )

# # Using object notation
# add_selectbox = st.sidebar.selectbox(


    
st.header("Alagamentos em São Paulo em 2019", divider = 'blue' )

col1, col2 = st.columns(2)

"st.session_state object", st.session_state

opt = ['Calcular data', 'Mostrar total']

# Initialize session_state variables if not present
if 'calculate_date' not in st.session_state:
    st.session_state['Calcular data'] = None 

if 'temporal_interval' not in st.session_state:
    st.session_state['temporal_interval'] = (None, None)


def set_date_widget(df, column):
    initial_date = pd.to_datetime(df[column]).dt.date.min()
    final_date = pd.to_datetime(df[column]).dt.date.max()

    d = st.date_input(
        "Selecione a série temporal que deseja visualizar",
        (initial_date, datetime.date(initial_date.year, initial_date.month+1, initial_date.day)),
        initial_date,
        final_date,
        format="YYYY-MM-DD",
    )
    return d


with col1:
    # Form for date selection and calculation
    # Date input widget
    selected_dates = set_date_widget(floods, 'DATA')
    # Submit button
    
    option = st.selectbox('Selecione uma opção',  opt)
    # Update temporal_interval only if the selected dates have changed
    if selected_dates != st.session_state['temporal_interval']:
        st.session_state['temporal_interval'] = selected_dates
        st.session_state['state_change'] = True
    else: 
        st.session_state['state_change'] = False

    st.text(selected_dates)
    # Check if 'Calcular' button is clicked and state has changed
    # Check if 'Calcular' button is clicked
    if option=='Calcular data':
        if st.session_state['temporal_interval'][0] is not None and st.session_state['temporal_interval'][1] is not None:
            filtered_floods = floods[(floods.DATA.dt.date >= st.session_state['temporal_interval'][0]) &
                                    (floods.DATA.dt.date <= st.session_state['temporal_interval'][1])]
            st.metric("total", value=len(filtered_floods))
        else:
            st.warning("Por favor, selecione um intervalo de datas antes de calcular.")
    else:
        st.metric("total", value=len(floods))


with col2:
    if option=='Calcular data':
        st_data = st_folium(plot_floods_folium(floods, st.session_state['temporal_interval'][0], st.session_state['temporal_interval'][1]), width=725)
    else:
        st_folium(plot_floods_folium(floods))







