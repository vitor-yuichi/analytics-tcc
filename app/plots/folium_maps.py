import folium 
import pandas 
import datetime


def plot_floods_folium(floods, start_date = datetime.date(2019, 1, 3), end_date = datetime.date(2019, 1, 10), tile = 'CartoDB dark_matter'):
    #filtrando por data 
    floods = floods[(floods.DATA.dt.date >= start_date) & (floods.DATA.dt.date <= end_date)]


    # Create a Folium map centered at a specific location
    my_map = folium.Map(location=[floods['LATITUDE'].mean(), floods['LONGITUDE'].mean()],
                         zoom_start=11,
                        tiles=tile,
                        )

    # Iterate through the DataFrame and add markers
    for index, row in floods.iterrows():
        folium.Marker([row['LATITUDE'], row['LONGITUDE']], popup=row['LOCAL_ED'],
                       icon=folium.Icon(color="blue", icon="fa-solid fa-house-flood-water", prefix='fa')
                       ).add_to(my_map)
    # Display the map
    return my_map