import streamlit as st

# halaman metode analisa

def load_view():   
    # load style
    with open('./assets/metode_analisa.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    st.header('METODE ANALISA')

    st.write('''
        Untuk melakukan prediksi Persentase Penduduk Miskin (P0) berdasarkan kabupaten/kota di Jawa Tengah, berikut 
        langkah-langkah yang dilakukan :
    ''')

    st.subheader('PENGUMPULAN DATA')
    st.write('''
        Data yang digunakan dalam analisis adalah data persentase penduduk miskin berdasarkan kabupaten/kota di Jawa Tengah, 
        nighttime light di Jawa Tengah, dan citra satelit siang hari di Jawa Tengah.
    ''')

    st.subheader('PRA-PEMROSESAN DATA')
    st.write('''
        Sebelum memulai analisis, citra satelit siang hari dan nighttime light diubah menjadi format PNG dan kemudian dipotong 
        menjadi potongan-potongan kecil dengan ukuran 1km x 1km.
    ''')

    st.subheader('EKSTRAKSI TINGKAT INTENSITAS CAHAYA DARI NIGHTTIME LIGHT')
    st.write('''
        Mengekstraksi tingkat intensitas cahaya dari setiap potongan nighttime light berukuran 1km x 1km. 
        Kemudian, menghitung intensitas cahaya minimum, maksimum, rata-rata, median, dan standar deviasi dari setiap 
        potongan-potongan nighttime light di setiap kabupaten/kota.
    ''')
    
    st.subheader('CLUSTERING TINGKAT INTENSITAS CAHAYA')
    st.write('''
        Pada tahap ini, tingkat intensitas cahaya dari potongan-potongan nighttime light dikelompokan menjadi 3 
        yaitu, tingkat intensitas cahaya rendah, sedang, dan tinggi menggunakan metode Gaussian Mixture.
    ''')

    st.subheader('MODEL DEEP LEARNING MEMPREDIKSI CLUSTER TINGKAT INTENSITAS CAHAYA')
    st.write('''
        Model deep learning  yang digunakan dalam penelitian adalah Convolutional Neural Network (CNN), tepatnya
        VGG16, ResNet, dan Inception. Variabel prediktor yang digunakan adalah potongan citra satelit siang hari, 
        sementara variabel targetnya adalah cluster intensitas cahaya. Setelah dilakukan evaluasi model, akurasi model menunjukkan 
        bahwa model terbaik adalah model Inception setelah dilakukan augmentasi gambar.
    ''')

    st.subheader('EKSTRAKSI FITUR')
    st.write('''
        Ekstraksi fitur pada layer ke-2 model Inception dengan augmentasi gambar yang sudah dilatih. Ekstraksi fitur 
        ini dilakukan pada setiap potongan citra satelit siang hari dan kemudian dihitung rata-rata fitur untuk setiap 
        kabupaten/kota. Dengan mengambil rata-rata fitur, didapatkan representasi informasi dari potongan-potongan citra 
        satelit untuk memprediksi persentase penduduk miskin di setiap kabupaten/kota.
    ''')

    st.subheader('PREDIKSI PERSENTASE PENDUDUK MISKIN DENGAN MODEL REGRESI')
    st.write('''
        Berdasarkan fitur-fitur yang diekstraksi dari citra satelit siang hari dan fitur intensitas cahaya dari masing-masing 
        kabupaten/kota, dibuat model regressi (Ridge dan LASSO) untuk memprediksi persentase penduduk miskin.
    ''')