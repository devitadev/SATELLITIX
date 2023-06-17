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
        Data yang diperlukan untuk analisis adalah data persentase penduduk miskin, citra satelit malam hari, 
        citra satelit siang hari,  persentase rumah tangga yang memiliki akses air minum layak, jumlah bayi lahir 
        bergizi kurang, persentasi rumah tangga menggunakan listrik PLN, dan batas administrasi kabupaten/kota.
    ''')

    st.subheader('PRA-PEMROSESAN DATA')
    st.write('''
        Sebelum memulai analisis, langkah penting yang perlu dilakukan adalah menangani masalah missing value dalam data. 
        Selain itu, gambar citra satelit siang hari diubah menjadi format PNG dan dipotong menjadi potongan-potongan kecil 
        dengan ukuran 1km x 1km.
    ''')

    st.subheader('EKSTRAKSI TINGKAT INTENSITAS CAHAYA DARI CITRA CATELIT MALAM HARI')
    st.write('''
        Mengekstraksi tingkat intensitas cahaya dari setiap potongan citra satelit malam hari berukuran 1km x 1km. 
        Kemudian menghitung in minimum, maksimum, rata-rata, median, dan standar deviasi dari potongan-potongan 
        kecerahan di setiap kabupaten/kota.
    ''')
    
    st.subheader('CLUSTERING TINGKAT KECERAHAN')
    st.write('''
        Pada tahap ini, tingkat kecerahan dari potongan-potongan citra satelit pada malam hari dikelompokan menjadi 3 
        yaitu, tingkat kecerahan rendah, sedang, dan tinggi menggunakan metode Gaussian Mixture.
    ''')

    st.subheader('MODEL DEEP LEARNING MEMPREDIKSI CLUSTER TINGKAT KECERAHAN')
    st.write('''
        Model deep learning  yang digunakan dalam penelitian adalah Convolutional Neural Network (CNN), tepatnya
        VGG16, ResNet, dan Inception. Variabel prediktor yang digunakan adalah potongan citra satelit siang hari, 
        sementara variabel targetnya adalah cluster kecerahan. Setelah dilakukan evaluasi model, akurasi model menunjukkan 
        bahwa model terbaik adalah VGG16 setelah dilakukan augmentasi dan fine-tuning.
    ''')

    st.subheader('EKSTRAKSI FITUR')
    st.write('''
        Ekstraksi fitur pada layer ke-2 model VGG16 dengan augmentasi dan fine-tuning yang sudah dilatih. Ekstraksi fitur 
        ini dilakukan pada setiap potongan citra satelit siang hari dan kemudian dihitung rata-rata fitur untuk setiap 
        kabupaten/kota. Dengan mengambil rata-rata fitur, didapatkan representasi informasi dari potongan-potongan citra 
        satelit untuk memprediksi persentase penduduk miskin di setiap kabupaten/kota.
    ''')

    st.subheader('PREDIKSI PERSENTASE PENDUDUK MISKIN DENGAN MODEL REGRESI')
    st.write('''
        Berdasarkan fitur-fitur yang diekstraksi dari citra satelit siang hari dan fitur intensitas cahaya dari masing-masing 
        kabupaten/kota, dibuat model regressi (Ridge dan LASSO) untuk memprediksi persentase penduduk miskin.
    ''')