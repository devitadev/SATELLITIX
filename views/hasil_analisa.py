import streamlit as st
import folium
import pandas as pd
import geopandas as gpd
import math

from folium import Choropleth
from streamlit_folium import folium_static

# halaman hasil analisa

def load_view():
    # load style
    with open('./assets/hasil_analisa.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    # load csv data
    data_complete = pd.read_csv('./assets/datas/full_data.csv')
    kab_kota = data_complete['KAB_KOTA'].copy()

    # load shape data
    shp_data = gpd.read_file('./assets/datas/BATAS KABUPATEN KOTA DESEMBER 2019 DUKCAPIL/BATAS KABUPATEN KOTA DESEMBER 2019 DUKCAPIL.shp')
    # shp_data.crs = 'EPSG:23839'

    # load latitude longitude information
    lat_long = pd.read_csv('./assets/datas/latitude_longitude.csv')
    
    # section 1
    st.header("VISUALISASI PETA PERSENTASE PENDUDUK MISKIN (P0) TAHUN 2021")

    left_co, right_co = st.columns([9, 4])

    with right_co:
        st.subheader("PARAMETER VISUALISASI PETA")
        map_type = st.radio('PETA PERSENTASE PENDUDUK MISKIN (P0) TAHUN 2021', (
            'Prediksi Berdasarkan Model Ridge Dengan Extracted Features dan Light Features',
            'Prediksi Berdasarkan Model LASSO Dengan Extracted Features dan Light Features',
            'Prediksi Berdasarkan Model Ridge Dengan Extracted Features',
            'Prediksi Berdasarkan Model LASSO Dengan Extracted Features',
            'Prediksi Berdasarkan Model Ridge Dengan Light Features',
            'Prediksi Berdasarkan Model LASSO Dengan Light Features',
            'Berdasarkan Data BPS'
        ))
        ms_kab_kota = st.multiselect('KABUPATEN/KOTA', kab_kota, kab_kota)
        # set selected y column
        if map_type == 'Prediksi Berdasarkan Model Ridge Dengan Extracted Features dan Light Features':
            y_column = 'y pred ridge with extracted features, light features'
        elif map_type == 'Prediksi Berdasarkan Model LASSO Dengan Extracted Features dan Light Features':
            y_column = 'y pred lasso with extracted features, light features'
        elif map_type == 'Prediksi Berdasarkan Model Ridge Dengan Extracted Features':
            y_column = 'y pred ridge with extracted features'
        elif map_type == 'Prediksi Berdasarkan Model LASSO Dengan Extracted Features':
            y_column = 'y pred lasso with extracted features'
        elif map_type == 'Prediksi Berdasarkan Model Ridge Dengan Light Features':
            y_column = 'y pred ridge with light features'
        elif map_type == 'Prediksi Berdasarkan Model LASSO Dengan Light Features':
            y_column = 'y pred lasso with light features'
        elif map_type == 'Berdasarkan Data BPS': y_column = 'y actual'

    
    with left_co:
        st.subheader('PETA ' + map_type.upper() + " TAHUN 2021")

        # merge shape file and bps data and latitude longitude data
        merged_data = pd.merge(shp_data, data_complete, on='KAB_KOTA')
        merged_data['Error'] = abs(merged_data[y_column] - merged_data['y actual'])
        merged_data = pd.merge(merged_data, lat_long, on='KAB_KOTA')

        # filter data
        if (len(ms_kab_kota) == 0): selected_data = merged_data.copy()
        else: selected_data = merged_data[merged_data['KAB_KOTA'].isin(ms_kab_kota)]

        # calculate position
        latitude = selected_data['latitude'].mean()
        longitude = selected_data['longitude'].mean()

        # calculate latitude longitude distance
        dist_lat = selected_data['latitude'].max() - selected_data['latitude'].min()
        dist_long = selected_data['longitude'].max() - selected_data['longitude'].min()

        # calculate zoom_start
        zoom_start = 8
        if (dist_long == 0 and dist_lat == 0):
            zoom_start = 10
        else:
            if ((dist_long/2) < dist_lat): zoom_start = math.sqrt(0.5 / (dist_long)) + 7.8
            else : zoom_start = math.sqrt(0.25 / dist_lat) + 7.8

        # Create a Folium map object
        map_y = folium.Map(location=[latitude, longitude], scrollWheelZoom = False, zoom_start = zoom_start)

        # Add the poverty index as a choropleth map layer
        choropleth = Choropleth(geo_data = merged_data, data = merged_data, columns = ['KAB_KOTA', y_column],
                key_on = 'feature.properties.KAB_KOTA', fill_color = 'RdYlGn_r', fill_opacity = 0.7, line_opacity = 0.4,
                legend_name='Persentase Penduduk Miskin (P0)', highlight=True).add_to(map_y)

        # Create a GeoJson object for the choropleth layer
        geojson = folium.GeoJson(
            merged_data,
            style_function=lambda feature: {
                'fillOpacity': 0 if feature['properties']['KAB_KOTA'] in ms_kab_kota else 0.5,
                'fillColor': 'RdYlGn_r',
                'color': 'black',
                'weight': 0
            },
            highlight_function=lambda feature: {'color': 'black', 'weight': 2}
        )

        feature_tooltip = ['Kabupaten/Kota', y_column]
        if (y_column != 'y actual'): feature_tooltip = ['Kabupaten/Kota', y_column, 'y actual', 'Error']
        choropleth.geojson.add_child(
            folium.features.GeoJsonTooltip(feature_tooltip)
        )

        # Add the GeoJson layer to the map
        geojson.add_to(choropleth.geojson)

        # Display the map using Streamlit
        map_state = st.text('Loading Map...')
        folium_static(map_y)
        map_state.text("")


    # section 2
    st.header("EVALUASI MODEL")

    df = pd.DataFrame()
    df['Model'] = ['Model Regresi Ridge', 'Model LASSO Ridge', 'Model Regresi Ridge', 'Model LASSO Ridge', 'Model Regresi Ridge', 'Model LASSO Ridge']
    df['Indikator'] = ['Extracted Features dan Light Features', 'Extracted Features dan Light Features', 'Extracted Features', 'Extracted Features', 'Light Features', 'Light Features']
    df['MAPE (%)'] = [13.61596641, 21.0630029, 14.17403577, 22.19840047, 20.96039997, 20.77718022]
    df['R2'] = [0.64461209, 0.384482851, 0.627537489, 0.322709919, 0.359154537, 0.357704315]
    df['Keterangan'] = ['Asumsi Linearitas, Homoskedastisitas, Independensi, Normalitas Terpenuhi', 
                        'Asumsi Linearitas, Homoskedastisitas, Independensi, Normalitas Terpenuhi', 
                        'Asumsi Linearitas, Homoskedastisitas, Independensi, Normalitas Terpenuhi', 
                        'Asumsi Linearitas, Homoskedastisitas, Independensi, Normalitas Terpenuhi',
                        'Asumsi Linearitas, Homoskedastisitas, Independensi, Normalitas Terpenuhi', 
                        'Asumsi Linearitas, Homoskedastisitas, Independensi, Normalitas Terpenuhi']

    st.table(df.style.highlight_between(0, color='#829CD0'))