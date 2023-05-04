import streamlit as st
import base64

st.set_page_config(
    page_title="Turismo",
    page_icon="airplane",
)

st.title('Tablero indicadores económicos de Turismo')

st.balloons()

def show_pdf(file_path):
    with open(file_path,"rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="650" height="650" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

with st.expander("Panorama Economico"):
    show_pdf('panorama.pdf')