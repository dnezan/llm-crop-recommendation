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

from io import BytesIO
buf = BytesIO(b'test')
import time
import pandas as pd
import matplotlib.pyplot as plt


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
    #        

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

            map_type = st.radio(
                        "Choose map",
                        ('Default', 'Agri', 'NVMI', 'Color infrared'), horizontal = True)

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
                    
                    ###LANDSAT CODE
                    collection = ee.ImageCollection('LANDSAT/LC09/C02/T1_L2')\
                        .filterBounds(ee_object) \
                        .filterDate('2023-03-01', '2023-03-31') \
                        .sort('CLOUD_COVER')
                    
                    median = collection.median()

                    def apply_scale_factors(image):
                        opticalBands = image.select('SR_B.').multiply(0.0000275).add(-0.2)
                        thermalBands = image.select('ST_B.*').multiply(0.00341802).add(149.0)
                        return image.addBands(opticalBands, None, True).addBands(thermalBands, None, True)

                    dataset = apply_scale_factors(median)

                    dataset = dataset.clip(ee_object)

                    vis_natural = {
                        'bands': ['SR_B4', 'SR_B3', 'SR_B2'],
                        'min': 0.0,
                        'max': 0.3,
                    }

                    vis_nir = {
                        'bands': ['SR_B5', 'SR_B4', 'SR_B3'],
                        'min': 0.0,
                        'max': 0.3,
                    }

                    vis_agri = {
                        'bands': ['SR_B6', 'SR_B5', 'SR_B2'],
                        'min': 0.0,
                        'max': 0.3,
                    }

                    ###############END OF LANDSAT CODE
                    if map_type =='Default':
                        m.addLayer(ee_object, {'color': 'FFFFFF', 'width': 4, 'fillColor': '000000', 'fillOpacity': 0}, 'Selected plot', True, 0.8)
                        #geemap.ee_export_image(ee_object, filename=filename, scale=90, region=roi, file_per_band=True
)
                    if map_type == 'Agri':
                        m.addLayer(dataset, vis_agri, 'Agri')

                    if map_type == 'NVMI':
                        collection = collection.median()
                        
                        kernel = ee.Kernel.gaussian(5,1,'pixels')
                        collection = collection.convolve(kernel)

                        collection = apply_scale_factors(collection)

                        collection = collection.clip(ee_object)

                        ndvi1999 = collection.normalizedDifference(['SR_B5', 'SR_B6'])

                        ndmi_vis_params = {'min': -1, 'max': 1, 'palette': cm.palettes.Blues}


                        m.addLayer(ndvi1999, ndmi_vis_params, "NDVI 1999")

                    if map_type == 'Color infrared':
                        m.addLayer(dataset, vis_nir, 'Color infrared (543)')

                    print(ee_object)

                    #m.centerObject(ee_object, 19)
                    m.to_streamlit(width=700, height=670)       

            d = st.date_input(":calendar: When do you want to plant your crop?")
        
            submitted = st.form_submit_button("Submit")
            if submitted:
                season = calc_season(d)
                st.markdown(f"**<font size=6>{district}</font>** &nbsp; {state}", unsafe_allow_html=True)
                row3_col1, row3_col2 = st.columns([1, 1])
                with row3_col1:
                    st.markdown(":blue[**Season:**] " + str(season))
                    st.markdown(":blue[**Date of sowing:**] " + str(d))
                    
                    #####CALCULATING HARVESTING DATE
                    newdate = datetime.timedelta(days=120)
                    newdate = d + newdate
                    st.markdown(":blue[**Date of harvesting:**] " + str(newdate))

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


def calc_season(d):
    print(d)
    d1 = datetime.date(2023,4,1)
    d2 = datetime.date(2023,5,1)
    d3 = datetime.date(2023,6,1)
    d4 = datetime.date(2023,7,1)
    d5 = datetime.date(2023,8,1)
    d6 = datetime.date(2023,9,1)
    d7 = datetime.date(2023,10,1)
    d8 = datetime.date(2023,11,1)
    d9 = datetime.date(2024,1,30)
 
    if (d1<=d<d2):
        szn = 'Sorna'
    elif (d2<=d<d3):
        szn = 'Kar'
    elif (d3<=d<d4):
        szn = 'Kuruvai'   
    elif (d4<=d<d5):
        szn = 'Early Samba'
    elif (d5<=d<d6):
        szn = 'Samba'
    elif (d6<=d<d7):
        szn = 'Late Samba/ Thaladi/ Pishanam'
    elif (d7<=d<d8):
        szn = 'Late Thaladi'  
    elif (d8<=d<d9):
        szn = 'Navarai'
    return szn

# Call the app function to run the Streamlit app
app()
