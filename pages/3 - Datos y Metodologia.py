import streamlit as st
from graphs.maps import gen_map


st.title("Indicadores Estatales")
option = st.selectbox(
    'How would you like to be contacted?',
    ('Extranjeros', 'Nacionales'))


fig = gen_map(option)
st.plotly_chart(fig, use_container_width=True)