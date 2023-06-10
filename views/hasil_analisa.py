import streamlit as st
import folium
import pandas as pd
import geopandas as gpd

from folium import Choropleth
from streamlit_folium import folium_static


# halaman hasil analisa

def display_map(bps_2020, bps_2021, type):
    # read shape data
    shp_data = gpd.read_file('./assets/datas/BATAS KABUPATEN KOTA DESEMBER 2019 DUKCAPIL/BATAS KABUPATEN KOTA DESEMBER 2019 DUKCAPIL.shp')

    # merge shape file and bps data
    data_2020 = pd.DataFrame()
    data_2020['KAB_KOTA'] = [kab_kota.upper() for kab_kota in bps_2020['Kabupaten/Kota']]
    data_2020['P0'] = bps_2020['P0']
    data_2020['Air Minum Layak'] = bps_2020['Air Minum Layak']
    data_2020['Bayi Gizi Kurang'] = bps_2020['Bayi Gizi Kurang']
    data_2020['Pengguna PLN'] = bps_2020['Pengguna PLN']
    merged_data_2020 = pd.merge(shp_data, data_2020, on='KAB_KOTA')

    # data_2021 = pd.DataFrame()
    # data_2021['KAB_KOTA'] = [kab_kota.upper() for kab_kota in bps_2021['Kabupaten/Kota']]
    # data_2021['P0'] = bps_2021['P0']
    # data_2021['Air Minum Layak'] = bps_2021['Air Minum Layak']
    # data_2021['Bayi Gizi Kurang'] = bps_2021['Bayi Gizi Kurang']
    # data_2021['Pengguna PLN'] = bps_2021['Pengguna PLN']
    # merged_data_2021 = pd.merge(shp_data, data_2021, on='KAB_KOTA')


def load_view():
    # load style
    with open('./assets/hasil_analisa.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
    st.header('HASIL ANALISA')

    map_load_state = st.text('Loading Map...')

    # load csv data
    bps_2020 = pd.read_csv('./assets/datas/bps_2020.csv', sep=';')
    bps_2021 = pd.read_csv('./assets/datas/bps_2021.csv', sep=';')

    # read shape data
    shp_data = gpd.read_file('./assets/datas/BATAS KABUPATEN KOTA DESEMBER 2019 DUKCAPIL/BATAS KABUPATEN KOTA DESEMBER 2019 DUKCAPIL.shp')

    # merge shape file and bps data
    data_2020 = pd.DataFrame()
    data_2020['KAB_KOTA'] = [kab_kota.upper() for kab_kota in bps_2020['Kabupaten/Kota']]
    data_2020['P0'] = bps_2020['P0']
    merged_data_2020 = pd.merge(shp_data, data_2020, on='KAB_KOTA')

    # Create a Folium map object
    map = folium.Map(location=[-7.242536378184681, 110.21476125405597], scrollWheelZoom = False, zoom_start = 8)

    # Add the poverty index as a choropleth map layer
    choropleth = folium.Choropleth(geo_data = merged_data_2020, data = merged_data_2020, columns = ['KAB_KOTA','P0'],
        key_on = 'feature.properties.KAB_KOTA', fill_color = 'YlOrRd', fill_opacity = 0.7, line_opacity = 0.2,
        legend_name='Persentase penduduk miskin (P0)').add_to(map)
    choropleth.add_to(map)

    # Display the map using Streamlit
    folium_static(map)
    map_load_state.text("Map Loaded")

    