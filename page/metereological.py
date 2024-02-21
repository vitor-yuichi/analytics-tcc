
def windy_map_with_options():
    
    import pandas as pd 
    from PIL import Image
    import streamlit as st
    import requests
    from datetime import datetime
    from plotly.subplots import make_subplots
    import plotly.graph_objects as go
    import pandas as pd
    import json 
    import os


    @st.cache_data
    def windy_api(API_KEY_WINDY, lat, long):
        url = 'https://api.windy.com/api/point-forecast/v2'
        myobj = {
        "lat": lat,
        "lon": long,
        "model": "gfs",
        "parameters": ["temp", "precip", "convPrecip", "wind", "rh", 'ptype'],
        "levels": ["surface", "800h", "300h"],
        "key": API_KEY_WINDY
        }
        x = requests.post(url, json = myobj)
        values = json.loads(x.text)
        return values




    def convert_int_to_timestamp(values, key):
        # Example list of integer values representing timestamps
        timestamps_milliseconds =  values[key]

        # Converter para segundos dividindo por 1000
        timestamps_seconds = [timestamp / 1000 for timestamp in timestamps_milliseconds]

        # Criar objetos datetime para cada timestamp
        datas_correspondentes = [datetime.utcfromtimestamp(ts) for ts in timestamps_seconds]

        return datas_correspondentes

    def make_windy_plots(windy_prec):
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=("Temperatura (K)", "Velocidade dos ventos (ms-1)", "Umidade Relativa", "Acumulado de chuva"))

        # Gráfico 1 com 3 linhas
        fig.add_trace(go.Scatter(x=windy_prec['timestamp'], y=windy_prec['temp_surface'], mode='lines', name='Temp superfície (K)'),
                    row=1, col=1)
        fig.add_trace(go.Scatter(x=windy_prec['timestamp'], y=windy_prec['temp-300h'], mode='lines', name='Temp em 300hPa (K)'),
                    row=1, col=1)
        fig.add_trace(go.Scatter(x=windy_prec['timestamp'], y=windy_prec['temp-800h'], mode='lines', name='Temp em 800hPa (K)'),
                    row=1, col=1)

        # Gráfico 2 com 3 linhas
        fig.add_trace(go.Scatter(x=windy_prec['timestamp'], y=windy_prec['wind_v-surface'], mode='lines', name='Vel. vento superfície (ms-1)'),
                    row=1, col=2)
        fig.add_trace(go.Scatter(x=windy_prec['timestamp'], y=windy_prec['wind_u-300h'], mode='lines', name='Vel. vento superfície (300hPa) (ms-1)'),
                    row=1, col=2)
        fig.add_trace(go.Scatter(x=windy_prec['timestamp'], y=windy_prec['wind_u-800h'], mode='lines', name='Vel. vento superfície (800hPa) (ms-1)'),
                    row=1, col=2)

        # Gráfico 3 com 3 linhas
        fig.add_trace(go.Scatter(x=windy_prec['timestamp'], y=windy_prec['rh-surface'], mode='lines', name='Umidade relativa'),
                    row=2, col=1)
        fig.add_trace(go.Scatter(x=windy_prec['timestamp'], y=windy_prec['rh-300h'], mode='lines', name='Umidade relativa (300hPa)'),
                    row=2, col=1)
        fig.add_trace(go.Scatter(x=windy_prec['timestamp'], y=windy_prec['rh-800h'], mode='lines', name='Umidade relativa (800hPa)'),
                    row=2, col=1)

        # Gráfico 4 com 3 linhas
        fig.add_trace(go.Scatter(x=windy_prec['timestamp'], y=windy_prec['past3hprecip-surface'], mode='lines', name='Acumulado precip após 3h'),
                    row=2, col=2)
        fig.add_trace(go.Scatter(x=windy_prec['timestamp'], y=windy_prec['past3hconvprecip-surface'], mode='lines', name='Acumulado precip. convectiva'),
                    row=2, col=2)


        fig.update_layout(height=500, width=1000,
                        title_text="Previsões com previso GFS", 
                        legend=dict(orientation="h", x=0.5, y=-0.3, xanchor='center')
                        ) 

        return fig

    def generate_dataframe_from_api(values, datas_correspondentes):
        dataframe =  pd.DataFrame({
                    'timestamp':datas_correspondentes,
                    'temp_surface': values['temp-surface'],
                    'temp-300h': values['temp-300h'],
                    'temp-800h': values['temp-800h'],
                    'wind_v-surface': values['wind_v-surface'],
                    'wind_u-300h': values['wind_u-300h'],
                    'wind_u-800h': values['wind_u-800h'],
                    'ptype-surface': values['ptype-surface'],
                    'rh-surface':values['rh-surface'],
                    'rh-300h': values['rh-300h'],
                    'rh-800h': values['rh-800h'],
                    'past3hprecip-surface': values['past3hprecip-surface'],
                    'past3hconvprecip-surface': values['past3hconvprecip-surface']
                        }
                    )
        return dataframe

    # Load the image
    image = Image.open(os.path.join(os.getcwd(), 'page/images/clima1.jpg'))

    # Resize the image (optional)
    resized_image = image.resize((800, 300))   
    st.image(resized_image)

    @st.cache_data
    def import_dataframe_windy():
        windy_df = pd.read_excel(os.path.join(os.getcwd(), 'page/windy.xlsx'))
        return windy_df

    @st.cache_data
    def import_municipios():
        municipios = pd.read_csv(os.path.join(os.getcwd(), 'page/municipios.csv'))
        municipios =  municipios[municipios['codigo_uf'] == 35]
        return municipios[['nome', 'latitude', 'longitude']]
    
    API = st.secrets.windy_api.API

    municipios = import_municipios()
 
    windy_df = import_dataframe_windy()

    if 'windy_call_api' not in  st.session_state:
        st.session_state['windy_call_api'] = windy_df   

    if 'api_use' not in st.session_state:
        st.session_state['api_use'] = 'not_used'
    
    if 'mun_selecionado' not in st.session_state:
        st.session_state['mun_selecionado'] = 'São José dos Campos'

    def pass_option_value(option):
        values = windy_api(API, municipios[municipios.nome == option]['latitude'].values[0], municipios[municipios.nome == option]['longitude'].values[0])
        datas_correspondentes = convert_int_to_timestamp(values, 'ts')
        dataframe = generate_dataframe_from_api(values, datas_correspondentes)
        st.session_state['windy_call_api'] = dataframe
        st.session_state['api_use'] = 'user_api_state'
        st.session_state['mun_selecionado'] = option



    st.header("Explore dados metereológicos :earth_americas:", divider  = 'blue')
    st.subheader(""":blue[Windy] é uma plataforma online que fornece informações meteorológicas e mapas interativos relacionados ao clima, vento, ondas, chuva e outros dados meteorológicos.A plataforma oferece visualizações em tempo real e previsões para várias partes do mundo.
             """, divider = 'blue')
    
    with st.expander(":green[Atualmente, o modelo conta 8 sistemas de predição]:"):
        st.write("""
            - :violet[Arome] - abrange a França e áreas circundantes
            - :violet[IconEU] - abrange a Europa e áreas circundantes
            - :violet[GFS] - um modelo global
            - :violet[GFS Wave] - um modelo global EXCLUINDO a Baía de Hudson (parcialmente), Mar Negro, Mar Cáspio, a maior parte do Oceano Ártico.
            - :violet[namConus] - abrange os Estados Unidos e áreas circundantes (Canadá, México)
            - :violet[namHawaii] - abrange o Havaí
            - :violet[namAlaska] - abrange o Alasca e áreas circundantes
            - :violet[geos5] - um modelo global   
        """)
    


    
    with st.container():
        st.write('**Selecione a visualização do mapa no canto esquerdo superior** :earth_americas:')
        # Coordenadas para São José dos Campos
        latitude = -23.1896
        longitude = -45.8840


        

        # Construir a URL do Windy map com base nas opções selecionadas
        windy_map_url = f"https://embed.windy.com/embed2.html?lat={latitude}&lon={longitude}&zoom=8"
        
        windy_map_url += "&overlay=temperature"

        windy_map_url += "&menu=&message=&marker=&calendar=&pressure=&type=map&location=coordinates&detail="
        windy_map_url += f"&detailLat={latitude}&detailLon={longitude}&metricWind=default&metricTemp=default&radarRange=-1"

        # Código do mapa Windy
        windy_map_code = f"""
        <iframe
            width="100%"
            height="400"
            src="{windy_map_url}"
            frameborder="0"
        ></iframe>
        """

        st.markdown('''
        :violet[No canto inferior esquerdo, você pode pressionar o botão de reprodução para observar a evolução temporal
                    da predição através do mapa]''')    

        # Exibir o mapa Windy com Streamlit
        st.markdown(windy_map_code, unsafe_allow_html=True)

        st.header("Utilize o previsor :blue[Windy]", divider  = 'blue')



        option = st.selectbox('Selecione o município:',  municipios['nome'])
        botao_mun = st.button('Previsão para o local', on_click = pass_option_value, args= [option])

        st.subheader(f"Previsão para :violet[{st.session_state['mun_selecionado']}]")
        if st.session_state['api_use'] == 'not_used':
            st.plotly_chart(make_windy_plots(st.session_state['windy_call_api']),  use_container_width=True)
        elif st.session_state['api_use'] == 'user_api_state':
            st.plotly_chart(make_windy_plots(st.session_state['windy_call_api']),  use_container_width=True)


    @st.cache_data
    def convert_to_format(format, df):
  
            return df.to_csv().encode('utf-8')
        

    csv = convert_to_format(format, st.session_state['windy_call_api'])
    st.download_button(
        label="Baixar tabela como CSV",
        data=csv,
        file_name='previsor_clima.csv',
        mime='text/csv'
    )

# if __name__ == "__main__":
#     windy_map_with_options()
