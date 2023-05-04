import streamlit as st

def hide_menu():
    hide_menu = """
    <style>
    #MainMenu {
        visibility: hidden;
    }
    
    footer {
        visibility: visible;
    }
    footer:after {
        content: 'Elaborado por la Dirección de Estudios Economicos';
        display: block;
        position: relative;
        color: green;
        padding: 5px;
        top: 3px;
    }
    </style>
    """
    st.markdown(hide_menu, unsafe_allow_html=True)