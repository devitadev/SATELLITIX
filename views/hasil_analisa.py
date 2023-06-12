import streamlit as st
import folium
import pandas as pd
import numpy as np
import geopandas as gpd

from folium import Choropleth
from streamlit_folium import folium_static
from sklearn.preprocessing import StandardScaler

# halaman hasil analisa

def load_view():
    # load style
    with open('./assets/hasil_analisa.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    # load csv data
    data_complete = pd.read_csv('./assets/datas/full_data.csv')

    # load shape data
    shp_data = gpd.read_file('./assets/datas/BATAS KABUPATEN KOTA DESEMBER 2019 DUKCAPIL/BATAS KABUPATEN KOTA DESEMBER 2019 DUKCAPIL.shp')

    # section 1
    st.header('PETA PREDIKSI PERSENTASE PENDUDUK MISKIN (P0) BERDASARKAN KABUPATEN/KOTA TAHUN 2021')

    # merge shape file and bps data
    merged_data = pd.merge(shp_data, data_complete, on='KAB_KOTA')

    # Create a Folium map object
    map_pred = folium.Map(location=[-7.242536378184681, 110.21476125405597], scrollWheelZoom = False, zoom_start = 8)
    map_pred_with_other_features = folium.Map(location=[-7.242536378184681, 110.21476125405597], scrollWheelZoom = False, zoom_start = 8)

    # Add the poverty index as a choropleth map layer
    Choropleth(geo_data = merged_data, data = merged_data, columns = ['KAB_KOTA','y pred with light and extracted features'],
            key_on = 'feature.properties.KAB_KOTA', fill_color = 'RdYlGn_r', fill_opacity = 0.8, line_opacity = 0.4,
            legend_name='Prediksi Persentase Penduduk Miskin (P0)').add_to(map_pred)
    Choropleth(geo_data = merged_data, data = merged_data, columns = ['KAB_KOTA','y pred with light, extracted, and other features'],
            key_on = 'feature.properties.KAB_KOTA', fill_color = 'RdYlGn_r', fill_opacity = 0.8, line_opacity = 0.4,
            legend_name='Prediksi Persentase Penduduk Miskin (P0)').add_to(map_pred_with_other_features)

    # Display the map using Streamlit
    map_state = st.text('Loading Map...')
    left_co, right_co = st.columns([1, 1])
    with left_co:
        st.subheader('Peta Sebaran Prediksi Persentase Penduduk Miskin Berdasarkan Light Features dan Extracted Features')
        folium_static(map_pred)
    with right_co:
        st.subheader('Peta Sebaran Prediksi Persentase Penduduk Miskin Berdasarkan Light Features, Extracted Features, Other Indicators')
        folium_static(map_pred_with_other_features)
    map_state.text("")


    # section 2
    st.header('PETA VISUALISASI DATA BERDASARKAN KABUPATEN/KOTA TAHUN 2021')

    # quantile classification for mean light
    num_quantiles = 6
    quantiles =  np.linspace(0, 1, num_quantiles + 1)
    merged_data['Quantile'] = pd.qcut(merged_data['2'], q=quantiles, labels=False)

    # Create a Folium map object
    map_y_actual = folium.Map(location=[-7.242536378184681, 110.21476125405597], scrollWheelZoom = False, zoom_start = 8)
    map_mean_light = folium.Map(location=[-7.242536378184681, 110.21476125405597], scrollWheelZoom = False, zoom_start = 8)

    # Add the poverty index as a choropleth map layer
    Choropleth(geo_data = merged_data, data = merged_data, columns = ['KAB_KOTA','y actual'],
            key_on = 'feature.properties.KAB_KOTA', fill_color = 'RdYlGn_r', fill_opacity = 0.7, line_opacity = 0.2,
            legend_name='Persentase Penduduk Miskin (P0)').add_to(map_y_actual)
    Choropleth(geo_data = merged_data, data = merged_data, columns = ['KAB_KOTA','Quantile'],
            key_on = 'feature.properties.KAB_KOTA', fill_opacity = 0.9, line_opacity = 0.4,
            legend_name='Rata-rata Kecerahan', fill_color = 'YlGnBu_r', showscale = True).add_to(map_mean_light)


    map_state = st.text('Loading Map...')
    left_co, right_co = st.columns([1, 1])
    with left_co:
        st.subheader('Peta Sebaran Persentase Penduduk Miskin Berdasarkan BPS')
        folium_static(map_y_actual)
    with right_co:
        st.subheader('Peta Sebaran Kecerahan Setiap Kabupaten/Kota Berdasarkan Citra Satelit Malam Hari')
        folium_static(map_mean_light)
        map_state.text("")