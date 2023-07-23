import streamlit as st
import pandas as pd

from PIL import Image

# halaman tentang data

def load_view():
    # load style
    with open('./assets/tentang_data.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
    # load csv data
    df = pd.read_csv('./assets/datas/data persentase penduduk miskin.csv', sep=";")
    kab_kota = df['Kabupaten/Kota'].copy()

    # section 1
    st.header('DATA SATELIT')

    left_co, right_co = st.columns([3, 1])

    with right_co:
        st.subheader("PARAMETER DATA SATELIT")
        img_type = st.radio(
            'Pilih tipe data satelit',
            ('Citra Satelit', 'Nighttime Light')
        )
        year = st.radio(
            'Pilih tahun data satelit',
            ('2020', '2021')
        )
        kab_kota_option = st.selectbox('Pilih kabupaten/kota', (kab_kota))
        image_path = './assets/images/' + img_type + ' ' + year + '/' + kab_kota_option + '.png'
    
    if img_type == 'Citra Satelit': sumber = "Google Earth Engine, berdasarkan Harmonized Sentinel-2 MSI: MultiSpectral Instrument, Level-2A (https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR_HARMONIZED)"
    elif img_type == 'Nighttime Light': sumber = "Earth Observation Group (EOG) yang dapat diakses melalui https://eogdata.mines.edu/nighttime_light/annual/v21/"
    keterangan = "Data satelit " + kab_kota_option + " berikut merupakan " + img_type + " tahun " + str(year) + " yang diperoleh dari " + sumber
    
    with left_co:
        image = Image.open(image_path)
        st.markdown(keterangan)
        st.image(image)

    # section 2
    st.header("CITRA SATELIT BERDASARKAN CLUSTER INTENSITAS CAHAYA")
    st.write('''Dalam kasus analisa ini, daerah dengan intensitas cahaya malam hari yang lebih tinggi menggambarkan daerah dengan 
             tingkat ekonomi yang lebih baik. Melalui potongan gambar berdasarkan cluster berikut, kita dapat melihat perbedaan 
             citra satelit dari setiap cluster intensitas cahaya''')

    columns = st.columns(6)
    with columns[0]: 
        st.subheader('PARAMETER')
        cluster_option = st.radio('Pilih Cluster Intensitas Cahaya', ('Intensitas Cahaya Rendah', 'Intensitas Cahaya Sedang', 'Intensitas Cahaya Tinggi'))

    if(cluster_option == 'Intensitas Cahaya Rendah'): cluster = 'low'
    elif(cluster_option == 'Intensitas Cahaya Sedang'): cluster = 'med'
    elif(cluster_option == 'Intensitas Cahaya Tinggi'): cluster = 'high'

    for i in range(1, 6):
        with columns[i]:
            img = Image.open('./assets/images/patches/' + cluster + '_' + str(i) +'.png').resize((400,400))
            st.image(img)
        
        
    # section 3
    st.header('DATA PERSENTASE PENDUDUK MISKIN (P0)')

    left_co_2, right_co_2 = st.columns([3, 1])
    with right_co_2:
        st.subheader('PARAMETER')
        plot_year = st.radio("Data Persentase Penduduk Miskin Tahun", ('2020', '2021'))
    with left_co_2:
        st.bar_chart(df, x='Kabupaten/Kota', y=('P0 ' + plot_year))
    