import streamlit as st
import base64
from streamlit.components.v1 import html

from PATHS import NAVBAR_PATHS


def inject_custom_css():
    with open('assets/styles.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def get_current_route():
    try:
        return st.experimental_get_query_params()['nav'][0]
    except:
        return None


def navbar_component():
    with open("assets/images/SATELLITIX.png", "rb") as image_file:
        image_logo_as_base64 = base64.b64encode(image_file.read())

    with open("assets/images/icon-menu.png", "rb") as image_file:
        image_menu_as_base64 = base64.b64encode(image_file.read())

    navbar_items = ''
    for key, value in NAVBAR_PATHS.items():
        navbar_items += (f'<a class="navitem navbar-link" href="/?nav={value}">{key}</a>')
    
    component = rf'''
        <nav class="container navbar">
            <div class="nav-container">
                <img class="nav-logo" src="data:image/png;base64, {image_logo_as_base64.decode("utf-8")}"/>
                <img class="navbar-toogle" id="toogle" src="data:image/png;base64, {image_menu_as_base64.decode("utf-8")}"/>
            </div>
            <div id="navbar"> {navbar_items} </div>
        </nav>
        '''
    
    st.markdown(component, unsafe_allow_html=True)
    
    nav_js = '''
    <script>
        // navbar elements
        var navigationTabs = window.parent.document.getElementsByClassName("navitem");
        var cleanNavbar = function(navigation_element) {
            navigation_element.removeAttribute('target');
        }
        for (var i = 0; i < navigationTabs.length; i++) {
            cleanNavbar(navigationTabs[i]);
        }

        var toogle = window.parent.document.getElementById("toogle");
        var navbar = window.parent.document.getElementById("navbar");
        toogle.addEventListener("click", () => {
            if (navbar.style.display == "none") navbar.style.display = "flex";
            else if (navbar.style.display == "") navbar.style.display = "flex";
            else navbar.style.display = "none";
        });

        window.addEventListener("resize", () => {
            if (toogle.style.display == "none") navbar.style.display = "flex";
        });
    </script>
    '''
    html(nav_js)
