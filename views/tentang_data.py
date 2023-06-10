import streamlit as st
import pandas as pd

from PIL import Image

# halaman tentang data

def load_view():
    # load style
    with open('./assets/tentang_data.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    st.header('TENTANG DATA')

    # load csv data
    bps_2020 = pd.read_csv('./assets/datas/bps_2020.csv', sep=';')
    bps_2021 = pd.read_csv('./assets/datas/bps_2021.csv', sep=';')
    kab_kota = bps_2020['Kabupaten/Kota'].tolist()


    # citra satelit malam hari
    st.subheader('CITRA SATELIT MALAM HARI')
    st.write('Citra satelit malam hari yang digunakan untuk analisa bersumber dari: https://eogdata.mines.edu/nighttime_light/monthly/v10/')
    
    left_co, right_co = st.columns([1, 1])
    with left_co:
        option_malam_20 = st.selectbox('Citra Satelit Malam Hari Tahun 2020', (kab_kota))
        night_2020_img = Image.open('./assets/images/Nightlight_2020_PNG/' + option_malam_20 + '.png')
        night_2020_img = night_2020_img.resize((1600, 800))
        st.image(night_2020_img)
    with right_co:
        option_malam_21 = st.selectbox('Citra Satelit Malam Hari Tahun 2021', (kab_kota))
        night_2021_img = Image.open('./assets/images/Nightlight_2021_PNG/' + option_malam_21 + '.png')
        night_2021_img = night_2021_img.resize((1600, 800))
        st.image(night_2021_img)


    # citra satelit siang hari
    st.subheader('CITRA SATELIT SIANG HARI')
    st.write('''
        Citra satelit siang hari yang digunakan untuk analisa diperoleh dari Google Earth Engine dan berasal dari satelit 
        Harmonized Sentinel-2 MSI: MultiSpectral Instrument, Level-2A.''')
    
    left_co, right_co = st.columns([1, 1])
    with left_co:
        option_siang_20 = st.selectbox('Citra Satelit Siang Hari Tahun 2020', (kab_kota))
        day_2020_img = Image.open('./assets/images/Daylight_2020_PNG/' + option_siang_20 + '.png')
        day_2020_img = day_2020_img.resize((1600, 800))
        st.image(day_2020_img)
    with right_co:
        option_siang_21 = st.selectbox('Citra Satelit Siang Hari Tahun 2021', (kab_kota))
        day_2021_img = Image.open('./assets/images/Daylight_2021_PNG/' + option_siang_21 + '.png')
        day_2021_img = day_2021_img.resize((1600, 800))
        st.image(day_2021_img)


    # data tabular
    st.subheader('DATA TABULAR')
    st.write('Data tabular yang digunakan untuk analisa diperoleh dari BPS.')
    
    left_co, right_co = st.columns([1, 1])
    with left_co:
        st.write('**Data Tabular Tahun 2020**')
        st.dataframe(bps_2020, width=1000)
    with right_co:
        st.write('**Data Tabular Tahun 2021**')
        st.dataframe(bps_2021, width=1000)


    left_co, right_co = st.columns([3, 2])
    with left_co:
        # deskripsi variabel
        st.write('**Deskripsi Variabel**')
        bps_keterangan = pd.read_csv('./assets/datas/bps_keterangan.csv', sep=';')
        st.table(bps_keterangan)   
    with right_co:
        # statistik deskriptif
        option_sd = st.selectbox('###### **Statistik Deskriptif**', ['Tahun 2020', 'Tahun 2021'])
        if (option_sd == 'Tahun 2020'): st.dataframe(bps_2020.describe(), width=1000)
        elif (option_sd == 'Tahun 2021'): st.dataframe(bps_2021.describe(), width=1000)