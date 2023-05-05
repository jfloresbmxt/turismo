import streamlit as st
import numpy as np
from graphs.state_info import gen_map, get_list, get_centers
from graphs.remove_hamburger import hide_menu

st.set_page_config(
    page_title="Indicadores Estatales",
    page_icon="airplane",
)

# Esconder Menu por default
hide_menu()

st.title("Indicadores Estatales")
option = st.selectbox(
    'Selecciona la variable de interes',
    ('Extranjeros', 'Nacionales', "Cuartos", "Ocupacion"))

fig = gen_map(option)
st.plotly_chart(fig, use_container_width=True)

st.divider()
st.header("Información por Estado y Centro Turistico")

col1, col2 = st.columns(2)
with col1:
    option = st.selectbox('Estado', get_list())

with col2:
    st.selectbox("Centro Turistico", get_centers(option))
