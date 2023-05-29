import ee
import os
import datetime
import fiona
import geopandas as gpd
import folium
import streamlit as st
import geemap.colormaps as cm
import geemap.foliumap as geemap
import datetime
from datetime import datetime
from datetime import date
from io import BytesIO
buf = BytesIO(b'test')
import time
import pandas as pd

def save_uploadedfile(uploadedfile):
     with open(os.path.join("tempDir",uploadedfile.name),"wb") as f:
         f.write(uploadedfile.getbuffer())

def check_state(file_name):
    farm_plot_file = file_name
    state_boundary_file = './data/cleaned_district_boundary3.shp'
    farm_plot = gpd.read_file(farm_plot_file)
    state_boundaries = gpd.read_file(state_boundary_file)
    farm_plot = farm_plot.to_crs(state_boundaries.crs)
    for index, state in state_boundaries.iterrows():
        if farm_plot.geometry.within(state.geometry).any():
            district_name = state['District']
            state_name = state['STATE']
            
            return(district_name, state_name)
            

def app():
    st. set_page_config(layout="wide")
    st.title(" ")
    #        #MainMenu {visibility: hidden;}

    st.markdown("""
        <style>        
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        """, unsafe_allow_html=True)

    row1_col1, row1_col2 = st.columns([3, 2])

    with row1_col1:
        m = geemap.Map(
        basemap="SATELLITE",
        plugin_Draw=True,
        Draw_export=True,
        locate_control=False,
        plugin_LatLngPopup=False, 
        measure=True)    
        #center=[20,77], 
        #zoom=4,
 
    with row1_col2:
        with st.form("my_form"):
            st.subheader(":seedling: Crop Planning App")
            w = st.file_uploader(":file_folder: Upload a GeoJSON file", type="geojson")
            if w is None:
                m.set_center(78, 21, zoom=4)
                with row1_col1:
                    m.to_streamlit(width=700, height=670)       

            
            else:
                save_uploadedfile(w)
                df = gpd.read_file("./tempDir/" + w.name)

                df['Center_point'] = df['geometry'].centroid
                df["lat"] = df.Center_point.map(lambda p: p.x)
                df["long"] = df.Center_point.map(lambda p: p.y)
                uploaded_lat_val = (df["lat"][0])
                uploaded_long_val = (df["long"][0])

                district, state = check_state("./tempDir/" + w.name)     

                with row1_col1:
                    m.set_center(uploaded_lat_val, uploaded_long_val, zoom=18)
                    ee_object = geemap.geojson_to_ee("./tempDir/" + w.name)
                    m.addLayer(ee_object,{'color': 'FFFFFF', 'width': 4, 'fillColor': '000000'}, 'Selected plot', True, 0.8)

                    print(ee_object)

                    #m.centerObject(ee_object, 19)
                    m.to_streamlit(width=700, height=670)       

            d = st.date_input(":calendar: When do you want to plant your crop?")
        
            submitted = st.form_submit_button("Submit")
            if submitted:
                season = func(d)
                st.markdown(f"**<font size=6>{district}</font>** &nbsp; {state}", unsafe_allow_html=True)
                row3_col1, row3_col2 = st.columns([1, 1])
                with row3_col1:
                    st.markdown(":blue[**Season:**] " + str(season))
                    st.markdown(":blue[**Date of sowing:**] " + str(d))
                    st.markdown(":blue[**Date of harvesting:**] " + str(d))

                with row3_col2:
                    file_loc = "./data/scraped/" + str(district).lower().title() + ".csv"
                    df = pd.read_csv(file_loc)
                    if season in df['Season'].values:
                        df2=df.loc[df['Season'] == season, 'Varieties'].iloc[0]
                        st.markdown(":green[**Paddy Varieties**] ")
                        st.write(str(df2))
                    else: 
                        st.error("It is not an optimum time to plant paddy in your given location. Try planting in the following seasons:")
                        for value in df.iloc[:, 0]:
                            st.write(value)


def func(d):
    print(d)
    d1 = date(2023,4,1)
    d2 = date(2023,5,1)
 

    if (d1<d<d2):
        szn = 'Sorna'
    else:
        szn = 'Kar'     
    return szn

# Call the app function to run the Streamlit app
app()
