import streamlit as st
from page.alagamentos_sp import floods_2019_data_sp
from page.metereological import windy_map_with_options
import os 

st.set_page_config(
        page_title="Analytics Project",
        page_icon=":bar_chart:"
    )

def intro():

    st.write("# Bem vindo à plataforma de Analytics voltados à dados metereológicos e hidrológicos")
    st.sidebar.success("Selecione a página")

    st.markdown(
        """
        Este projeto reune dados do INMET, alagamentos de 2019 registrados pela defesa civil e dados metereológicos de diversas plataformas.

        **👈 Selecione os dados que deseja visualizar** to see some examples
        of what Streamlit can do!

        ### Want to learn more?

        - Check out [streamlit.io](https://streamlit.io)
        - Jump into our [documentation](https://docs.streamlit.io)
        - Ask a question in our [community
          forums](https://discuss.streamlit.io)

        ### See more complex demos

        - Use a neural net to [analyze the Udacity Self-driving Car Image
          Dataset](https://github.com/streamlit/demo-self-driving)
        - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
    """
    )



page_names_to_funcs = {
    "Página inicial": intro,
    "Analytics Windy": windy_map_with_options,
    "Alagamentos SP 2019": floods_2019_data_sp
    }

st.sidebar.image(os.path.abspath('assets/imgs/AV01F-9EiLtRWpK-transformed.png'))
demo_name = st.sidebar.selectbox("Selecione a página", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()