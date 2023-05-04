import streamlit as st
from graphs.pib_info import gen_graph, table_style, gen_table
from graphs.remove_hamburger import hide_menu
from graphs.state_info import arrive, availability

st.set_page_config(
    page_title="Indicadores Nacionales",
    page_icon="airplane",
)

# Esconder Menu por default
hide_menu()

# Title
st.title("Indicadores Nacionales")

# Description
st.markdown("En esta sección podras encontrar los principales indicadores nacionales de Turismo")

def pib_section():
    # Get data and graphs
    df = table_style()
    fig = gen_graph()
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

st.header("PIB turístico")
pib_section()

st.divider()
def arrive_section():
    # Get data and graphs
    df = table_style()
    fig = arrive()

    tab1, tab2 = st.tabs(["Gráfica", "Datos"])

    with tab1:
        # Plot!
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.markdown("Work in progress")
        

st.header("Llegada de Turistas")
arrive_section()

st.divider()
def availability_section():
    # Get data and graphs
    df = table_style()
    fig = availability()

    tab1, tab2 = st.tabs(["Gráfica", "Datos"])

    with tab1:
        # Plot!
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.markdown("Work in progress")

st.header("Disponibilidad de cuartos")
availability_section()