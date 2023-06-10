import streamlit as st
import utils as utl
from views import beranda, metode_analisa, tentang_data, hasil_analisa

st.set_page_config(layout="wide", page_title='SATELLITIX')
st.set_option('deprecation.showPyplotGlobalUse', False)
utl.inject_custom_css()
utl.navbar_component()

def navigation():
    route = utl.get_current_route()
    if route == "beranda":
        beranda.load_view()
    elif route == "metode_analisa":
        metode_analisa.load_view()
    elif route == "tentang_data":
        tentang_data.load_view()
    elif route == "hasil_analisa":
        hasil_analisa.load_view()
    elif route == None:
        beranda.load_view()

navigation()