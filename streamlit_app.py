import ee
import os
import datetime
import fiona
import geopandas as gpd
import folium
import streamlit as st
import geemap.colormaps as cm
import geemap.foliumap as geemap
from datetime import date

def app():
    st. set_page_config(layout="wide")
    st.title(":calendar: Crop Planner App")
    
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
    
    if st.session_state.get("zoom_level") is None:
        st.session_state["zoom_level"] = 4

    st.session_state["ee_asset_id"] = None
    st.session_state["bands"] = None
    st.session_state["palette"] = None
    st.session_state["vis_params"] = None

    row1_col1, row1_col2 = st.columns([1, 1])

    with row1_col1:
        row2_col1, row2_col2 = st.columns([1, 1])
        with row2_col1:
            keyword = st.text_input("Search for a location:", "")   
        with row2_col2:
            w = st.file_uploader("Upload a GeoJSON file", type="geojson")
        m = geemap.Map(
        center=[20,77], 
        zoom=4,
        basemap="HYBRID",
        plugin_Draw=True,
        Draw_export=True,
        locate_control=False,
        plugin_LatLngPopup=False)
        m.to_streamlit(width=1300, height=360)
        if keyword:
            locations = geemap.geocode(keyword)
            if locations is not None and len(locations) > 0:
                str_locations = [str(g)[1:-1] for g in locations]
                location = st.selectbox("Select a location:", str_locations)
                #st.write(str_locations[0])
                loc_index = str_locations.index(location)
                selected_loc = locations[loc_index]
                lat, lng = selected_loc.lat, selected_loc.lng
                print(lat)
                print(lng)
                folium.Marker(location=[lat, lng], popup=location).add_to(m)
                m.set_center(lng, lat, 12)
                st.session_state["zoom_level"] = 12

    with row1_col2:
        st.write("hi")

    

# Call the app function to run the Streamlit app
app()
