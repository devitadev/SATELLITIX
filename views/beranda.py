import streamlit as st
from PIL import Image

# halaman beranda

def load_view():
    # load style
    with open('./assets/beranda.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
    # section 1: description
    logo = Image.open('./assets/images/SATELLITIX-dark.png')
    first_co, cent_co,last_co = st.columns([4, 2, 4])
    with cent_co: st.image(logo)

    st.markdown('''
        <p class="slogan">Empowering Central Java: Illuminating Poverty with Satellite Insights</p>
    ''', unsafe_allow_html=True)

    st.write('''
        <p class="description">
        Selamat datang di <b>SATELLITIX</b>! Situs yang menghadirkan prediksi '<b>Persentase Penduduk Miskin (P0)</b>' di Jawa Tengah, Indonesia, 
        menggunakan <b>deep learning</b> berdasarkan <b>citra satelit</b> dan <b>nighttime light</b>. Dengan antarmuka yang mudah digunakan, Anda dapat menjelajahi visualisasi 
        terperinci, peta interaktif, dan laporan berbasis data yang menyoroti prediksi tingkat kemiskinan di setiap kabupaten/kota 
        di wilayah Jawa Tengah. Jelajahi pola kemiskinan dan dorong perubahan positif guna mengatasi tantangan kemiskinan. </p>
    ''', unsafe_allow_html=True)

    # section 2: manfaat
    st.write('# MANFAAT')

    left_co, right_co = st.columns([2, 1])
    with left_co:
        st.write('''
            <p class="manfaat">
            <b>SATELLITIX</b> menyediakan solusi yang efisien untuk mengumpulkan data Persentase Penduduk Miskin (P0) berdasarkan kabupaten/kota 
            di Jawa Tengah menggunakan <b>citra satelit</b>, <b>nighttime light</b> dan <b>deep learning</b>.</p>
        ''', unsafe_allow_html=True)
    with right_co:
        img_manfaat_1 = Image.open('./assets/images/manfaat-1.jpg')
        st.image(img_manfaat_1)

    left_co_2, right_co_2 = st.columns([1, 2])
    with left_co_2:
        img_manfaat_2 = Image.open('./assets/images/manfaat-2.jpg')
        st.image(img_manfaat_2)
    with right_co_2:
        st.write('''
            <p class="manfaat">
            <b>SATELLITIX</b> memanfaatkan potensi <b>Big Data</b> dalam <b>official statistics</b> dengan memprediksi Persentase Penduduk Miskin (P0)
             di Jawa Tengah dengan cara yang lebih mudah dan efisien.</p>
        ''', unsafe_allow_html=True)

    left_co_3, right_co_3 = st.columns([2, 1])
    with left_co_3:
        st.write('''
            <p class="manfaat">
            <b>SATELLITIX</b> adalah media yang <b>mudah diakses</b> dan <b>intuitif</b> bagi pengguna yang ingin memperoleh informasi mengenai 
            prediksi Persentase Penduduk Miskin (P0) di Jawa Tengah.</p>
        ''', unsafe_allow_html=True)
    with right_co_3:
        img_manfaat_3 = Image.open('./assets/images/manfaat-3.jpg')
        st.image(img_manfaat_3)

    

    



    



    
    

