import streamlit as st
import numpy as np
from graphs.state_info import gen_map
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
    ('Extranjeros', 'Nacionales'))


fig = gen_map(option)
st.plotly_chart(fig, use_container_width=True)

st.divider()

tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])
data = np.random.randn(10, 1)

tab1.subheader("A tab with a chart")
tab1.line_chart(data)

tab2.subheader("A tab with the data")
tab2.write(data)