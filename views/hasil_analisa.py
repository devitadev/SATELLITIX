import streamlit as st
import folium
import pandas as pd
import geopandas as gpd

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
        else: y_column = 'y actual'

    
    with left_co:
        st.subheader('PETA ' + map_type.upper() + " TAHUN 2021")

        # merge shape file and bps data
        merged_data = pd.merge(shp_data, data_complete, on='KAB_KOTA')

        # filter data
        if (len(ms_kab_kota) == 0): selected_data = merged_data.copy()
        else: selected_data = merged_data[merged_data['KAB_KOTA'].isin(ms_kab_kota)]

        # calculate position
        latitude = selected_data.geometry.centroid.y.mean()
        longitude = selected_data.geometry.centroid.x.mean()

        print(latitude, longitude)

        # Create a Folium map object
        map_y = folium.Map(location=[latitude, longitude], scrollWheelZoom = False, zoom_start = 8)

        print(y_column)

        # Add the poverty index as a choropleth map layer
        choropleth = Choropleth(geo_data = merged_data, data = merged_data, columns = ['KAB_KOTA', y_column],
                key_on = 'feature.properties.KAB_KOTA', fill_color = 'RdYlGn_r', fill_opacity = 0.7, line_opacity = 0.25,
                legend_name='Persentase Penduduk Miskin (P0)').add_to(map_y)

        # Create a GeoJson object for the choropleth layer
        geojson = folium.GeoJson(
            merged_data,
            style_function=lambda feature: {
                'fillOpacity': 0 if feature['properties']['KAB_KOTA'] in ms_kab_kota else 0.7,
                'fillColor': 'RdYlGn_r',
                'color': 'black',
                'weight': 0.1
            }
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
    df['Model'] = ['Model Regresi Ridge', 'Model LASSO Ridge', 'Model Regresi Ridge', 'Model LASSO Ridge']
    df['Indikator'] = ['Extracted Features dan Light Features', 'Extracted Features dan Light Features', 'Extracted Features', 'Extracted Features']
    df['MAPE (%)'] = [14.13783141, 17.22131763, 18.34835365, 17.49600814]
    df['R2'] = [0.579108331, 0.518760325, 0.461738738, 0.502104425]
    df['Keterangan'] = ['Semua asumsi terpenuhi', 'Model tidak memenuhi asumsi normalitas', 'Model tidak memenuhi asumsi normalitas', 'Model tidak memenuhi asumsi normalitas']

    st.table(df.style.highlight_between(0, color='#829CD0'))