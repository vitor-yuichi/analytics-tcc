import streamlit as st
import pandas as pd 
import numpy as np
from streamlit_folium import st_folium
import datetime
import plotly.graph_objects as go
import os 
from mitosheet.streamlit.v1 import spreadsheet
## BIBLIOTECAS PERSONALIZADAS##
from plots.folium_maps import plot_floods_folium
from widgets.date_widgets import set_date_widget
##--------------------------#




## ----DADOS TEMPORARIOS---##
##-----------------------------##

def import_floods():
    floods = pd.read_excel(r'/analytics-project/analytics-tcc/app/database/floods.xlsx')
    return floods

floods = import_floods()
##-----------------------------##

def indicator(val):
    fig = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = val,
    title = {'text': "Total de alagamentos"},
    domain = {'x': [0, 1], 'y': [0, 1]},
    gauge = {'axis': {'range': [None, 1165]},
             'steps' : [
                 {'range': [0, 550], 'color': "lightgray"},
                 {'range': [551, 1165], 'color': "gray"}],
             'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 490}})
             )
    fig.update_layout(height=300)
    return fig



##------------------------SIDE BAR------------------------#
# # Using "with" notation
# with st.sidebar:
    #"""Logo imagem UNESP"""
    # st.image(os.path.abspath('assets/imgs/AV01F-9EiLtRWpK-transformed.png'))
    # st.markdown("<h4 style='text-align: center; color: Green;'>Engenharia Ambiental - SJC</h4>", unsafe_allow_html=True)
    # add_radio = st.radio(
    #     "Choose a shipping method",
    #     ("Standard (5-15 days)", "Express (2-5 days)")
    # )
# # Using object notation
# add_selectbox = st.sidebar.selectbox(
    
st.header("Alagamentos em São Paulo em 2019", divider = 'blue' )

st.write('Os alagamentos estão entre os desastres desencadeados por chuvas mais frequentes e custosos.')

st.write('Os dados foram obtidos pelo Centro de Gerenciamento de Emergências (CGE), um departamento do governo na cidade de São Paulo responsável por identificar e registrar a geolocalização de incidentes de alagamento resultantes de obstruções nas estradas. Esses registros incluem as horas de início e término do bloqueio da estrada, bem como o nome da rua e a interseção onde ocorreu o alagamento.')

col1, col2 = st.columns(2)



opt = ['Calcular data', 'Mostrar total']

# Initialize session_state variables if not present
if 'calculate_date' not in st.session_state:
    st.session_state['Calcular data'] = None 

if 'temporal_interval' not in st.session_state:
    st.session_state['temporal_interval'] = (None, None)




with col1:
    # Form for date selection and calculation
    # Date input widget
    selected_dates = set_date_widget(floods, 'DATA')
    option = st.selectbox('Selecione uma opção',  opt)
    # Update temporal_interval only if the selected dates have changed
    if selected_dates != st.session_state['temporal_interval']:
        st.session_state['temporal_interval'] = selected_dates
        st.session_state['state_change'] = True
    else: 
        st.session_state['state_change'] = False

    # Check if 'Calcular' button is clicked
    if option=='Calcular data':
        if st.session_state['temporal_interval'][0] is not None and st.session_state['temporal_interval'][1] is not None:
            filtered_floods = floods[(floods.DATA.dt.date >= st.session_state['temporal_interval'][0]) &
                                    (floods.DATA.dt.date <= st.session_state['temporal_interval'][1])]
            # st.metric("Alagamentos", value=len(filtered_floods))
            st.plotly_chart(indicator(len(filtered_floods)),  use_container_width=True)
        else:
            st.warning("Por favor, selecione um intervalo de datas antes de calcular.")
    else:
        st.plotly_chart(indicator(len(filtered_floods)),  use_container_width=True)

def handle_click_tile(new_type):
    st.session_state['tile_theme'] = new_type

if 'tile_theme' not in st.session_state:
    st.session_state['tile_theme'] = 'CartoDB dark_matter'


with col2:
    tile = st.selectbox('Selecione o tema do mapa', ['CartoDB dark_matter', 'CartoDB Positron', 'OpenStreetMap'])
    change = st.button('Alterar tema', on_click = handle_click_tile, args = [tile]) #Callback na função handle_click_tile para manter o session state da página 

    if option=='Calcular data':
        if st.session_state['tile_theme'] == 'CartoDB dark_matter':
            st_folium(plot_floods_folium(floods, st.session_state['temporal_interval'][0], st.session_state['temporal_interval'][1],
                                          tile= st.session_state['tile_theme']), 
                                          width=350, 
                                          height=500)
        elif st.session_state['tile_theme'] == 'CartoDB Positron':
            st_folium(plot_floods_folium(floods, st.session_state['temporal_interval'][0], st.session_state['temporal_interval'][1],
                                          tile= st.session_state['tile_theme']),
                                            width=350,
                                              height=500)
        else: 
            st_folium(plot_floods_folium(floods, st.session_state['temporal_interval'][0], st.session_state['temporal_interval'][1],
                                          tile= st.session_state['tile_theme']),
                                            width=350, 
                                            height=500)            
    else:
        if st.session_state['tile_theme'] == 'CartoDB dark_matter':
            st_folium(plot_floods_folium(floods, tile= st.session_state['tile_theme']), width=350, height=500)
        elif st.session_state['tile_theme'] == 'CartoDB Positron':
            st_folium(plot_floods_folium(floods, tile= st.session_state['tile_theme']), width=350, height=500)
        else:
            st_folium(plot_floods_folium(floods,  tile= st.session_state['tile_theme']), width=350, height=500)



st.title('Consulta de dados de alagamentos')
st.write('Estes dados estão conectados diretamente à API da base de dados MongoDB. Caso necessite comparar com outra base de dados, abaixo você pode importar uma segunda tabela e executar operações entre tabelas.')
spreadsheet(floods)


