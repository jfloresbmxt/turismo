import streamlit as st
from graphs.graph1 import gen_graph, table_style, gen_table

st.set_page_config(
    page_title="Indicadores Nacionales",
    page_icon="airplane",
)

st.title("Indicadores Nacionales")

df = table_style()
fig = gen_graph()


# Plot!
st.plotly_chart(fig, use_container_width=True)

st.divider()

hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """

# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)

st.header("PIB turístico")
# Table
st.table(df)

@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index = False).encode('latin1')

csv = convert_df(gen_table())

st.download_button(
    label="Descargar Tabla",
    data=csv,
    file_name='pib_turismo.csv',
    mime='text/csv',
)