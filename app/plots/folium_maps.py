import folium 
import pandas 

def plot_floods_folium(floods, start_date = '2019-01-01', end_date = '2019-01-10'):
    #filtrando por data 
    floods = floods[(floods.DATA > start_date) & (floods.DATA < end_date)]


    # Create a Folium map centered at a specific location
    my_map = folium.Map(location=[floods['LATITUDE'].mean(), floods['LONGITUDE'].mean()],
                         zoom_start=11,
                        tiles='CartoDB dark_matter',
                        )

    # Iterate through the DataFrame and add markers
    for index, row in floods.iterrows():
        folium.Marker([row['LATITUDE'], row['LONGITUDE']], popup=row['LOCAL_ED'],
                       icon=folium.Icon(color="blue", icon="fa-solid fa-house-flood-water", prefix='fa')
                       ).add_to(my_map)
    # Display the map
    return my_map