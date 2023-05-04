import streamlit as st
import base64
from  PIL import Image

st.set_page_config(
    page_title="Turismo",
    page_icon="airplane",
)

st.title('Tablero indicadores económicos de Turismo')

st.header("Objetivo")
st.markdown('Objetivo del tablero')
st.divider()

st.header("Otros estudios")
def show_pdf(file_path):
    with open(file_path,"rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

feature_image1 = Image.open('bmxt.jpg')
with st.container():
    image_col, text_col = st.columns((1,3))
    with image_col:
        st.image(feature_image1)
    with text_col:
        st.markdown(""" <style> .font {
            font-size:22px ; font-family: 'Black'; color: black;} 
            </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">Panorama económico</p>', unsafe_allow_html=True)    
        st.markdown("Conoce el comportamiento de los indicadores económicos mas importantes del país")

with st.container():
    with open("panorama.pdf", "rb") as pdf_file:
        PDFbyte = pdf_file.read()
    st.download_button(label="Descargar el estudio",
                    data=PDFbyte,
                    file_name="panorama_economico.pdf",
                    mime='application/octet-stream')