import streamlit as st

def hide_menu():
    hide_menu = """
    <style>
    #MainMenu {
        visibility: hidden;
    }
    </style>
    """
    st.markdown(hide_menu, unsafe_allow_html=True)