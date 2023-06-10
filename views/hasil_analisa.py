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

    # load csv data
    data_complete = pd.read_csv('./assets/datas/ridge_extracted_light_other.csv')

    # load shape data
    shp_data = gpd.read_file('./assets/datas/BATAS KABUPATEN KOTA DESEMBER 2019 DUKCAPIL/BATAS KABUPATEN KOTA DESEMBER 2019 DUKCAPIL.shp')

    # section 1
    st.header('PERSENTASE PENDUDUK MISKIN BERDASARKAN KABUPATEN/KOTA TAHUN 2021')

    # merge shape file and bps data
    merged_data = pd.merge(shp_data, data_complete, on='KAB_KOTA')

    # Create a Folium map object
    map_ypred = folium.Map(location=[-7.242536378184681, 110.21476125405597], scrollWheelZoom = False, zoom_start = 8)
    map_yactual = folium.Map(location=[-7.242536378184681, 110.21476125405597], scrollWheelZoom = False, zoom_start = 8)

    # Add the poverty index as a choropleth map layer
    folium.Choropleth(geo_data = merged_data, data = merged_data, columns = ['KAB_KOTA','y pred'],
            key_on = 'feature.properties.KAB_KOTA', fill_color = 'YlOrRd', fill_opacity = 0.7, line_opacity = 0.2,
            legend_name='Hasil Prediksi Persentase Penduduk Miskin (P0)').add_to(map_ypred)
    folium.Choropleth(geo_data = merged_data, data = merged_data, columns = ['KAB_KOTA','y actual'],
            key_on = 'feature.properties.KAB_KOTA', fill_color = 'YlOrRd', fill_opacity = 0.7, line_opacity = 0.2,
            legend_name='Persentase Penduduk Miskin (P0)').add_to(map_yactual)

    # Display the map using Streamlit
    left_co, right_co = st.columns([1, 1])
    with left_co:
        map_ypred_state = st.text('Loading Map...')
        folium_static(map_ypred)
        map_ypred_state.text("Peta Hasil Prediksi Persentase Penduduk Miskin (P0) Tahun 2021")
    with right_co:
        map_yactual_state = st.text('Loading Map...')
        folium_static(map_yactual)
        map_yactual_state.text("Peta Persentase Penduduk Miskin (P0) Tahun 2021")

    