import streamlit as st
import whisper
from PIL import Image
import pytesseract
import io
import os

st.set_page_config(layout="wide", page_title="Transcriptor de Textos")

@st.cache_resource
def load_whisper_model():
    return whisper.load_model("base")

st.title("✍️ Herramienta 2: Transcriptor de Textos")
st.markdown("Extrae texto de archivos de audio, video o imágenes.")
model = load_whisper_model()

tab1, tab2 = st.tabs(["🎤 Audio/Video a Texto", "🖼️ Imagen a Texto (OCR)"])

with tab1:
    st.header("Transcripción de Audio y Video")
    uploaded_file = st.file_uploader("Sube un archivo de audio o video", type=["mp3", "wav", "mp4", "m4a", "avi", "mov"])
    language = st.radio("Idioma del audio:", ('Español', 'Inglés'), horizontal=True)
    if st.button("Transcribir", key="transcribe_btn"):
        if uploaded_file:
            with st.spinner(f"Transcribiendo... Esto puede tardar varios minutos."):
                file_path = uploaded_file.name
                with open(file_path, "wb") as f: f.write(uploaded_file.getbuffer())
                result = model.transcribe(file_path, language='es' if language == 'Español' else 'en')
                os.remove(file_path)
                st.subheader("Texto Transcrito:")
                st.text_area("Resultado", result["text"], height=250)
                st.download_button(label="📥 Descargar como .txt", data=result["text"].encode('utf-8'), file_name=f"transcripcion.txt", mime="text/plain")
        else: st.warning("Por favor, sube un archivo.")

with tab2:
    st.header("Extracción de Texto desde Imagen (OCR)")
    uploaded_image = st.file_uploader("Sube una imagen", type=["png", "jpg", "jpeg"])
    ocr_language = st.radio("Idioma del texto en la imagen:", ('Español', 'Inglés'), horizontal=True, key="ocr_lang")
    if st.button("Extraer Texto", key="ocr_btn"):
        if uploaded_image:
            with st.spinner("Procesando imagen..."):
                image = Image.open(uploaded_image)
                extracted_text = pytesseract.image_to_string(image, lang='spa' if ocr_language == 'Español' else 'eng')
                st.subheader("Texto Extraído:")
                st.text_area("Resultado", extracted_text, height=250, key="ocr_result")
                st.download_button(label="📥 Descargar como .txt", data=extracted_text.encode('utf-8'), file_name=f"ocr.txt", mime="text/plain", key="download_ocr")
        else: st.warning("Por favor, sube una imagen.")
