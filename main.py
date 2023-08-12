

import streamlit as st
from streamlit_folium import folium_static
import folium as f,folium
import osmnx as ox
import networkx as nx
import geopy
import geopandas
import requests
import json
import geopandas as gpd
import numpy as np
import random
import matplotlib.pyplot as plt




st.image('./map.jpg')

st.title("Shortest Route for Electric Vehicles")
st.header('Using Python OSMNX and Folium Library')
st.write(' ')

input_method = st.sidebar.selectbox("Select the Input method",("Place Name", "Coordinates","Waiting Time"))

network_value = st.sidebar.selectbox("Select the Network type",("Walk","Drive","Bike","All"))

if network_value=='Walk':
    network_value='walk'
elif network_value=='Drive':
    network_value='drive'
elif network_value=='Bike':
    network_value='bike'
else:
    network_value='all'
    
algo_type = st.sidebar.selectbox("Select the Algorithm type",("Dijkstra’s Algorithm","Bellman-Ford Algorithm"))

if algo_type=='Dijkstra’s Algorithm':
    algo_value='dijkstra'
else:
    algo_value='bellman-ford'

input1 = 0.0000  
input2 = 0.0000   
input3 = 0.0000   
input4 = 0.0000  

colors  = ['blue', 'orange', 'green','yellow','purple']

if input_method=='Coordinates':

    st.write("""
    Enter the coordinate of the Source
    """)

    col1, col2 = st.columns(2)
    with col1:
        input1 = st.number_input('Source Lattitude Coordinates')
    with col2:
        input2 = st.number_input('Source Longitude Coordinates')

    st.write("Lattitude:",input1,"Longitude:", input2)

    st.write("""
    Enter the coordinate of the Destination
    """)

    col1, col2 = st.columns(2)
    with col1:
        input3 = st.number_input('Destination Lattitude Coordinates')
    with col2:
        input4 = st.number_input('Destination Longitude Coordinates')

    st.write("Lattitude:",input3,"Longitude:", input4)

    map_type = st.radio(
    'Select map type',
    ['OpenStreetMap', 'CartodbPositron','StamenTerrain']
    )

    k = st.select_slider('Select number of shortest paths', options=[1,'2','3','4','5'])
    k_paths=int(k)

    range = st.select_slider('Select distance range ( in Km )', options=[10,'20','30','40','50','60','70','80','90','100'])

    range_value=int(range)
    range_value*=1000

    st.write("Distance range in metres:",range_value)

    if st.button('Show me the Way'):

        try:
            ox.config(use_cache=True, log_console=True)

            G = ox.graph_from_point((input1, input2),dist=range_value,network_type=network_value,simplify=False)
            
            G = ox.speed.add_edge_speeds(G)

            G = ox.speed.add_edge_travel_times(G)

            orig = ox.get_nearest_node(G, (input1, input2))

            dest = ox.get_nearest_node(G, (input3, input4))
            

            route = nx.shortest_path(G, orig, dest, 'travel_time',method=algo_value)
            
            route_map = ox.plot_route_folium(G, route,route_color='red',tiles=map_type,weight=5)

            k_paths = k_paths - 1
            routes = ox.k_shortest_paths(G, orig, dest, k=k_paths, weight='length')
                
            ind = 0
            for x in routes:
                if (x!=route):
                    route_map = ox.plot_route_folium(G, x,route_color=colors[ind],route_map=route_map,tiles=map_type,weight=2)
                    ind = ind + 1

            tooltip1 = "Source"
            folium.Marker(
            [input1, input2], popup="Source", tooltip=tooltip1,icon=folium.Icon(color='blue')).add_to(route_map)

            tooltip2 = "Destination"
            folium.Marker(
            [input3, input4], popup="Destination", tooltip=tooltip2,icon=folium.Icon(color='red')).add_to(route_map)

            folium_static(route_map)
            st.write("The shortest among all k paths is indicated by red color.")
        
        except:

            st.image('./error.png')
            st.error('Sorry ! No Graph exists for the given inputs.')
            st.text("Please try again with some other input values.")
            
        
elif input_method=='Place Name':

    st.write("""
    Enter the name of the Source
    """)

    place1 = st.text_input('Source')

    place1=place1.replace(" ","+")
    st.write('')

    st.write("""
    Enter the name of the Destination
    """)

    place2 = st.text_input('Destination')

    place2=place2.replace(" ","+")

    map_type = st.radio(
    'Select map type',
    ['OpenStreetMap', 'CartodbPositron','StamenTerrain']
    )

    k = st.select_slider('Select number of shortest paths', options=[1,'2','3','4','5'])
    k_paths=int(k)

    range = st.select_slider('Select distance range ( in Km )', options=[10,'20','30','40','50','60','70','80','90','100'])

    range_value=int(range)
    range_value*=1000

    st.write("Distance range in metres:",range_value) 

    if st.button('Show me the Way'):

        try:
            url = 'https://maps.googleapis.com/maps/api/geocode/json?'

            api_key='AIzaSyCzxwd5wNZIL1PSFciGmZdlzK5o4h_0al8'

            res_ob1 = requests.get(url+'address='+place1+'&key='+api_key)

            results1 = res_ob1.json()['results']
            my_geo1 = results1[0]['geometry']['location']

            source_name_full = results1[0]['formatted_address']
            st.write("Source: ",source_name_full)

            st.write("Latitude:",my_geo1['lat'],"\n","Longitude:",my_geo1['lng'])
            input1 = my_geo1['lat']
            input2 = my_geo1['lng']


            res_ob2 = requests.get(url+'address='+place2+'&key='+api_key)

            results2 = res_ob2.json()['results']
            my_geo2 = results2[0]['geometry']['location']

            dest_name_full= results2[0]['formatted_address']
            st.write("Destination: ",dest_name_full)

            st.write("Latitude:",my_geo2['lat'],"\n","Longitude:",my_geo2['lng'])
            input3 = my_geo2['lat']
            input4 = my_geo2['lng']

            try:
                ox.config(use_cache=True, log_console=True)

                G = ox.graph_from_point((input1, input2),dist=range_value,network_type=network_value,simplify=False)

                G = ox.speed.add_edge_speeds(G)

                G = ox.speed.add_edge_travel_times(G)

                orig = ox.get_nearest_node(G, (input1, input2))

                dest = ox.get_nearest_node(G, (input3, input4))

                route = nx.shortest_path(G, orig, dest, 'travel_time',method=algo_value)

                route_map = ox.plot_route_folium(G, route,route_color='red',tiles=map_type,weight=5)

                k_paths = k_paths - 1
                routes = ox.k_shortest_paths(G, orig, dest, k=k_paths, weight='length')
                
                ind = 0
                for x in routes:
                    if (x!=route):
                        route_map = ox.plot_route_folium(G, x,route_color=colors[ind],route_map=route_map,tiles=map_type,weight=2)
                        ind = ind + 1

                tooltip1 = "Source"
                folium.Marker(
                [input1, input2], popup="Source", tooltip=tooltip1,icon=folium.Icon(color='blue')).add_to(route_map)

                tooltip2 = "Destination"
                folium.Marker(
                [input3, input4], popup="Destination", tooltip=tooltip2,icon=folium.Icon(color='red')).add_to(route_map)

                folium_static(route_map)
                st.write("The shortest among all k paths is indicated by red color.")

            except:
                
                st.image('./error.png')
                st.error('Sorry ! No Graph exists for the given inputs.')
                st.text("Please try again with some other input values.")

        except:

            st.error("Error ! Could not fetch the coordinates of the given inputs.")
            st.write("""
            Possible Reasons:\n
            1) API Key is invalid or not active.\n 
            2) Input is invalid.
            """)


else:

    st.write("""
    Enter the name of the Source
    """)

    place1 = st.text_input('Source')

    place1=place1.replace(" ","+")
    st.write('')

    st.write("""
    Enter the name of the Destination
    """)

    place2 = st.text_input('Destination')

    place2=place2.replace(" ","+")

    map_type = st.radio(
    'Select map type',
    ['OpenStreetMap', 'CartodbPositron','StamenTerrain']
    )

    k = st.select_slider('Select number of shortest paths', options=[1,'2','3','4','5'])
    k_paths=int(k)

    range = st.select_slider('Select distance range ( in Km )', options=[10,'20','30','40','50','60','70','80','90','100'])

    range_value=int(range)
    range_value*=1000

    st.write("Distance range in metres:",range_value) 

    if st.button('Show me the Way'):

        try:
            url = 'https://maps.googleapis.com/maps/api/geocode/json?'

            api_key='AIzaSyC3S0N05MSKjXr9PgN5_YSFX2WTHjSiA1w'

            res_ob1 = requests.get(url+'address='+place1+'&key='+api_key)

            results1 = res_ob1.json()['results']
            my_geo1 = results1[0]['geometry']['location']

            source_name_full = results1[0]['formatted_address']
            st.write("Source: ",source_name_full)

            st.write("Latitude:",my_geo1['lat'],"\n","Longitude:",my_geo1['lng'])
            input1 = my_geo1['lat']
            input2 = my_geo1['lng']


            res_ob2 = requests.get(url+'address='+place2+'&key='+api_key)

            results2 = res_ob2.json()['results']
            my_geo2 = results2[0]['geometry']['location']

            dest_name_full= results2[0]['formatted_address']
            st.write("Destination: ",dest_name_full)

            st.write("Latitude:",my_geo2['lat'],"\n","Longitude:",my_geo2['lng'])
            input3 = my_geo2['lat']
            input4 = my_geo2['lng']

            try:
                ox.config(use_cache=True, log_console=True)

                G = ox.graph_from_point((input1, input2),dist=range_value,network_type=network_value,simplify=False)

                G = ox.speed.add_edge_speeds(G)

                G = ox.speed.add_edge_travel_times(G)

                orig = ox.get_nearest_node(G, (input1, input2))

                dest = ox.get_nearest_node(G, (input3, input4))

                
                routes = ox.k_shortest_paths(G, orig, dest, k=k_paths, weight='length')
                
                node_points=[]


                for r in routes: 
                    for a in r:
                        node_points.append(a)
       
                node_points=list(set(node_points))

                node_points2 = []
                
                node_points2=(np.random.permutation(node_points).tolist())[0:int(len(node_points)*0.3)]

                node_waiting_times = np.random.permutation( np.arange(len(node_points))).tolist()

                
                time_charge=dict(zip(node_points,node_waiting_times))

                for c in node_points2:
                    time_charge[c]=0


                min=1000000

                sum=0

                shortest_route=[]

                routes = ox.k_shortest_paths(G, orig, dest, k=k_paths, weight='length')

                for z in routes:
                    for b in z:
                        sum=sum+time_charge[b]
                    
                    if(sum<min):
                        shortest_route=z
                        min=sum
                    
                    sum=0
                
                route_map = ox.plot_route_folium(G, shortest_route,route_color='red',tiles=map_type,weight=3)

                tooltip1 = "Source"
                folium.Marker(
                [input1, input2], popup="Source", tooltip=tooltip1,icon=folium.Icon(color='blue')).add_to(route_map)

                tooltip2 = "Destination"
                folium.Marker(
                [input3, input4], popup="Destination", tooltip=tooltip2,icon=folium.Icon(color='red')).add_to(route_map)
                folium_static(route_map)

            except:
                st.image('./error.png')
                st.error('Sorry ! No Graph exists for the given inputs.')
                st.text("Please try again with some other input values.")

        
        except:

            st.error("Error ! Could not fetch the coordinates of the given inputs.")
            st.write("""
            Possible Reasons:\n
            1) API Key is invalid or not active.\n 
            2) Input is invalid.
            """)







   
