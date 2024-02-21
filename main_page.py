import streamlit as st
from page.alagamentos_sp import floods_2019_data_sp
from page.metereological import windy_map_with_options
import os 
from PIL import Image


st.set_page_config(
        page_title="Analytics Project",
        page_icon=":bar_chart:"
    )

def intro():

    st.header("Open Data Analytics", divider = 'blue')

    st.sidebar.success("Selecione a página")

    st.markdown(
        """
        **Qual é o objetivo deste projeto?**

        - :red[Atualização Dinâmica]: Possibilitar a visualização e análise de dados em tempo real, permitindo aos
        usuários acompanhar mudanças e tendências assim que ocorrem;

        - :red[Streaming de Dados]: Integrar a capacidade de lidar com fluxos contínuos de dados,
          proporcionando uma visão sempre atualizada do cenário analisado;

        - :red[Facilitar o acesso] a dados estruturados, tratados e visualizações 
        robustas sem conhecimentos profundos em operações complexas de dados;

        - :red[Demonstrar que é possível realizar um projeto complexo de dados] sem qualquer custo que utiliza as tecnologias mais modernas como 
        databases e deploys em nuvens; 

        

        **Fonte de Dados:**


        - :violet[INMET (Instituto Nacional de Meteorologia)]: Fornece dados meteorológicos oficiais e confiáveis,
          incluindo informações como temperatura, umidade, velocidade do vento, entre outros. Este dados encontram-se
          tratados e armazenados no banco de dados MongoDB;


        - :violet[Defesa Civil]: Contribui com registros de alagamentos ocorridos em 2019, fornecendo informações valiosas sobre eventos climáticos extremos e suas consequências.

        - :blue[Windy]: Previsão Meteorológica: Integração com a API da Windy permite acesso a dados de previsão meteorológica em tempo real. 
        Esses dados podem incluir previsões de temperatura, precipitação, vento, pressão atmosférica, entre outros.  
    """
    )
    st.subheader('Powered by:')
    col1, col2, col3 = st.columns(3)


    # Page icon
    icon = Image.open('assets/imgs/mongodb-ar21.png')
    plotly_icon = Image.open('assets/imgs/Plotly-logo.png')
    stream_icon = Image.open('assets/imgs/stream.png')
    windy_icon = Image.open('assets/imgs/windy_full.png')
    python_icon = Image.open('assets/imgs/python.png')
    with col1:
        st.image(icon)
        st.image(windy_icon)
    with col2:
        st.image( plotly_icon )
        st.image(python_icon)
    with col3:
        st.image( stream_icon )

page_names_to_funcs = {
    "Página inicial": intro,
    "Analytics Windy": windy_map_with_options,
    "Alagamentos SP 2019": floods_2019_data_sp
    }

st.sidebar.image(os.path.abspath('assets/imgs/AV01F-9EiLtRWpK-transformed.png'))
demo_name = st.sidebar.selectbox("Selecione a página", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()