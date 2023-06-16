import streamlit as st
import pandas as pd
import streamlit_theme as stt

from PIL import Image

# halaman tentang data

def load_view():
    # load style
    with open('./assets/tentang_data.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
    # load csv data
    df = pd.read_csv('./assets/datas/full_data.csv')
    kab_kota = [kab_kota_name.lower().title() for kab_kota_name in df['KAB_KOTA']]
    
    with st.sidebar:
        st.header("PARAMETERS")
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
        
    
    st.header('CITRA SATELIT')
    if img_type == 'Citra Satelit Siang Hari': sumber = "Google Earth Engine, berdasarkan Harmonized Sentinel-2 MSI: MultiSpectral Instrument, Level-2A"
    elif img_type == 'Citra Satelit Malam Hari': sumber = "https://eogdata.mines.edu/nighttime_light/monthly/v10/"
    keterangan = "Citra satelit " + kab_kota_option + " berikut merupakan citra satelit tahun " + str(year) + " yang diperoleh dari " + sumber

    image = Image.open(image_path).resize((1000, 500))
    st.markdown(keterangan)
    st.image(image)
        
