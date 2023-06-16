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
    st.header('CITRA SATELIT')

    left_co, right_co = st.columns([3, 1])

    with right_co:
        st.subheader("PARAMETER CITRA SATELIT")
        img_type = st.radio(
            'Pilih tipe citra satelit',
            ('Citra Satelit Siang Hari', 'Citra Satelit Malam Hari')
        )
        year = st.radio(
            'Pilih tahun citra satelit',
            ('2020', '2021')
        )
        kab_kota_option = st.selectbox('Pilih kabupaten/kota', (kab_kota))
        image_path = './assets/images/' + img_type + ' ' + year + '/' + kab_kota_option + '.png'
    
    if img_type == 'Citra Satelit Siang Hari': sumber = "Google Earth Engine, berdasarkan Harmonized Sentinel-2 MSI: MultiSpectral Instrument, Level-2A"
    elif img_type == 'Citra Satelit Malam Hari': sumber = "https://eogdata.mines.edu/nighttime_light/monthly/v10/"
    keterangan = "Citra satelit " + kab_kota_option + " berikut merupakan citra satelit tahun " + str(year) + " yang diperoleh dari " + sumber
    
    with left_co:
        image = Image.open(image_path).resize((1000, 500))
        st.markdown(keterangan)
        st.image(image)
    
    # section 2
    st.header('DATA PERSENTASE PENDUDUK MISKIN (P0)')

    left_co, right_co = st.columns([3, 1])
    with right_co:
        plot_year = st.radio("Data Persentase Penduduk Miskin Tahun", ('2020', '2021'))
    with left_co:
        st.bar_chart(df, x='Kabupaten/Kota', y=('P0 ' + plot_year))
    