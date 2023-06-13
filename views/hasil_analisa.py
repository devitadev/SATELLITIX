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

    st.subheader("KETERANGAN DATA")
    df_ket_features = pd.DataFrame()
    df_ket_features['DATA'] = ['Light Features', 'Extracted Features', 'Other Indicators']
    df_ket_features['KETERANGAN'] = [
        'Data kecerahan dari masing-masing kabupaten/kota yang terdiri dari 5 variabel yaitu, max light, min light, mean light, std light, dan std light', 
        'Data hasil extraksi fitur layer ke-2 terakhir dari model VGG16 dengan augmentasi dan fine-tuning',
        'Data persentase rumah tangga yang memiliki akses air minum layak, jumlah bayi yang lahir bergizi kurang, dan persentase rumah tangga menggunakan sumber listrik PLN'
    ]
    st.table(df_ket_features)


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


    # section 3
    st.header('DATA')

    # prepare data frame
    df = pd.DataFrame()
    df['Kabupaten/Kota'] = [kab_kota.lower().title() for kab_kota in merged_data['KAB_KOTA']]
    df['Max Light'] = merged_data['0']
    df['Min Light'] = merged_data['1']
    df['Mean Light'] = merged_data['2']
    df['Median Light'] = merged_data['3']
    df['Std Light'] = merged_data['4']
    df['Air Minum Layak'] = merged_data['5']
    df['Bayi Kurang Gizi'] = merged_data['6']
    df['Pengguna PLN'] = merged_data['7']
    df['P0 actual'] = merged_data['y actual']
    df['P0 pred 1'] = merged_data['y pred with light and extracted features']
    df['P0 pred 2'] = merged_data['y pred with light, extracted, and other features']
    
    st.dataframe(df, width = 2000)

    st.subheader('KETERANGAN')

    df_keterangan = pd.DataFrame()
    df_keterangan['VARIABEL'] = df.columns.values.tolist()
    df_keterangan['KETERANGAN'] = [
        'Nama kabupaten/kota',
        'Kecerahan maksimun dari setiap pixel pada kabupaten/kota berdasarkan citra satelit malam hari',
        'Kecerahan minimum dari setiap pixel pada kabupaten/kota berdasarkan citra satelit malam hari',
        'Rata-rata kecerahan dari setiap pixel pada kabupaten/kota berdasarkan citra satelit malam hari',
        'Median dari kecerahan setiap pixel pada kabupaten/kota berdasarkan citra satelit malam hari',
        'Standar deviasi dari kecerahan setiap pixel pada kabupaten/kota berdasarkan citra satelit malam hari',
        'Persentase rumah tangga yang memiliki akses air minum layak berdasarkan BPS',
        'Jumlah bayi yang lahir bergizi kurang berdasarkan BPS',
        'Persentase rumah tangga menggunakan sumber listrik PLN berdasarkan BPS',
        'Persentase Penduduk Miskin berdasarkan BPS',
        'Persentase Penduduk Miskin berdasarkan hasil prediksi menggunakan Light Features dan Extracted Features',
        'Persentase Penduduk Miskin berdasarkan hasil prediksi menggunakan Light Features, Extracted Features, dan Other Indicators'
    ]
    st.table(df_keterangan)


     # section 4
    st.header('EVALUASI MODEL')

    df_evaluasi = pd.DataFrame()
    df_evaluasi['MODEL'] = ['Ridge Regression', 'Ridge Regression']
    df_evaluasi['INDIKATOR'] = ['Light Features dan Extracted Features', 'Light Features, Extracted Features, dan Other Indicators']
    df_evaluasi['Mean Absolute Error (MAE)'] = [1.706283723, 1.691530268]
    df_evaluasi['Mean Absolute Percentage Error (MAPE) (%)'] = [14.13133291, 14.01198108]
    df_evaluasi['R-Square'] = [0.5786875014, 0.5757788748]
    
    st.table(df_evaluasi)
