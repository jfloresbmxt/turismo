import streamlit as st
import base64
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Turismo",
    page_icon="airplane",
)

st.title('Tablero indicadores económicos de Turismo')

# st.balloons()

def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="650" height="650" type="application/pdf"></iframe>'
    # st.markdown(pdf_display, unsafe_allow_html=True)
    components.iframe(src=f"data:application/pdf;base64,{base64_pdf}", width=800, height=800)

show_pdf("panorama.pdf")

# with open("panorama.pdf", "rb") as pdf_file:
#     PDFbyte = pdf_file.read()


# st.download_button(label="Export_Report",
#                     data=PDFbyte,
#                     file_name="test.pdf",
#                     mime='application/octet-stream')

# with st.expander("Panorama Economico"):
    # show_pdf('panorama.pdf')