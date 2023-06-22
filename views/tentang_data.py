import streamlit as st
import pandas as pd

from PIL import Image

# halaman tentang data

from PIL import Image

def resize_and_add_transparency(image):
    # Menghitung lebar dan tinggi baru dengan mempertahankan aspek rasio dan batasan maksimum
    aspect_ratio = image.width / image.height
    if aspect_ratio > (5/2) :
        new_width = 1200
        new_height = int(new_width / aspect_ratio)
    else:
        new_height = 480
        new_width = int(new_height * aspect_ratio)

    # Membuat latar belakang transparan dengan ukuran baru
    background = Image.new('RGBA', (1200, 480), (0, 0, 0, 0))

    # Menempelkan gambar asli ke latar belakang transparan
    offset = ((1200 - new_width) // 2, (480 - new_height) // 2)
    background.paste(image.resize((new_width, new_height)), offset)
    return background


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
    
    if img_type == 'Citra Satelit': sumber = "Google Earth Engine, berdasarkan Harmonized Sentinel-2 MSI: MultiSpectral Instrument, Level-2A"
    elif img_type == 'Nighttime Light': sumber = "Earth Observation Group (EOG) yang dapat diakses melalui https://eogdata.mines.edu/nighttime_light/annual/v21/"
    keterangan = "Data satelit " + kab_kota_option + " berikut merupakan " + img_type + " tahun " + str(year) + " yang diperoleh dari " + sumber
    
    with left_co:
        image = Image.open(image_path)
        # make the image consistent
        # .resize((1000, 500))


        st.markdown(keterangan)
        st.image(resize_and_add_transparency(image))

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

    left_co, right_co = st.columns([3, 1])
    with right_co:
        st.subheader('PARAMETER')
        plot_year = st.radio("Data Persentase Penduduk Miskin Tahun", ('2020', '2021'))
    with left_co:
        st.bar_chart(df, x='Kabupaten/Kota', y=('P0 ' + plot_year))
    