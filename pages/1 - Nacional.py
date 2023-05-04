import streamlit as st
from graphs.pib_info import gen_graph, table_style, gen_table
from graphs.remove_hamburger import hide_menu

st.set_page_config(
    page_title="Indicadores Nacionales",
    page_icon="airplane",
)

# Esconder Menu por default
hide_menu()

# Get data and graphs
df = table_style()
fig = gen_graph()

# Title
st.title("Indicadores Nacionales")

# Description
st.markdown("En esta sección podras encontrar los principales indicadores nacionales de Turismo")

st.header("PIB turístico")
tab1, tab2 = st.tabs(["Gráfica", "Datos"])

with tab1:
    # Plot!
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    hide_table_row_index = """
                <style>
                thead tr th:first-child {display:none}
                tbody th {display:none}
                </style>
                """

    # Inject CSS with Markdown
    st.markdown(hide_table_row_index, unsafe_allow_html=True)

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