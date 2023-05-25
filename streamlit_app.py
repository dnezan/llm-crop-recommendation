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
from datetime import date
from io import BytesIO
buf = BytesIO(b'test')

def save_uploadedfile(uploadedfile):
     with open(os.path.join("tempDir",uploadedfile.name),"wb") as f:
         f.write(uploadedfile.getbuffer())

def app():
    st. set_page_config(layout="wide")
    st.title(" ")
    
    st.markdown("""
        <style>        
        #MainMenu {visibility: hidden;}
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
        center=[20,77], 
        zoom=4,
        basemap="SATELLITE",
        plugin_Draw=True,
        Draw_export=True,
        locate_control=False,
        plugin_LatLngPopup=False, 
        measure=True)    
        m.to_streamlit(width=700, height=670)
 
    
        

    with row1_col2:
        with st.form("my_form"):
            st.header(":calendar: Crop Planning App")
            w = st.file_uploader("", type="geojson")
            if w is not None:
                save_uploadedfile(w)
                st.write("chung")

                df = gpd.read_file("./tempDir/" + w.name)

            #Find the center point
                df['Center_point'] = df['geometry'].centroid
            #Extract lat and lon from the centerpoint
                df["lat"] = df.Center_point.map(lambda p: p.x)
                df["long"] = df.Center_point.map(lambda p: p.y)
                uploaded_lat_val = (df["lat"][0])
                uploaded_long_val = (df["long"][0])
                st.write(uploaded_lat_val)
                st.write(uploaded_long_val)
                ee_object = geemap.geojson_to_ee("./tempDir/" + w.name)
                m.addLayer(ee_object, {}, 'Layer name')
                m.centerObject(ee_object, 19)


            #folium_map = folium.Map(location=[uploaded_long_val, uploaded_lat_val], zoom_start=17, width=1000, height=350, tiles=tile_url, attr='Tiles &copy; Esri', control_scale=True)
           

            d = st.date_input("When do you want to plant your crop?")
        
        
   # Every form must have a submit button.
            submitted = st.form_submit_button("Submit")
            if submitted:
                func(uploaded_long_val, uploaded_lat_val,d)
        
        row2_col1, row2_col2 = st.columns([1, 1])
     
        #swith row2_col2:

def func(uploaded_long_val, uploaded_lat_val,d):
    st.write(d)      

    

# Call the app function to run the Streamlit app
app()
