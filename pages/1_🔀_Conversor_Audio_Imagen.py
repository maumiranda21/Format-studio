import streamlit as st
from pydub import AudioSegment
from PIL import Image
import moviepy.editor as mp
import os
import io
import zipfile

st.set_page_config(layout="wide", page_title="Conversor de Audio e Imagen")

st.title("🔀 Herramienta 1: Conversión de Audio e Imagen")
st.markdown("Convierte tus archivos de video, audio e imagen fácilmente.")

def create_zip(files, filenames):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        for i, file_data in enumerate(files):
            zip_file.writestr(filenames[i], file_data.getvalue())
    return zip_buffer.getvalue()

tab1, tab2, tab3 = st.tabs(["🎥 Video a Audio", "🎵 Audio A → Audio B", "🖼️ Imagen A → Imagen B"])

with tab1:
    st.header("Extractor de Audio desde Video")
    uploaded_videos = st.file_uploader("Sube uno o más videos (MP4, AVI, MOV)", type=["mp4", "avi", "mov", "mkv"], accept_multiple_files=True)
    audio_format = st.selectbox("Formato de audio de salida", ["mp3", "wav", "ogg", "flac"], key="video_audio_format")
    if st.button("Extraer Audio", key="extract_audio_btn"):
        if uploaded_videos:
            with st.spinner("Procesando videos..."):
                extracted_audios, audio_filenames = [], []
                for video_file in uploaded_videos:
                    video_name = os.path.splitext(video_file.name)[0]
                    with open(video_file.name, "wb") as f: f.write(video_file.getbuffer())
                    video_clip = mp.VideoFileClip(video_file.name)
                    audio_buffer = io.BytesIO()
                    video_clip.audio.write_audiofile(audio_buffer, codec='libmp3lame' if audio_format == 'mp3' else None, logger=None)
                    extracted_audios.append(audio_buffer)
                    audio_filenames.append(f"{video_name}.{audio_format}")
                    video_clip.close(); os.remove(video_file.name)
            st.success("¡Extracción completada!")
            if len(extracted_audios) == 1:
                st.download_button(label=f"📥 Descargar {audio_filenames[0]}", data=extracted_audios[0], file_name=audio_filenames[0])
            else:
                st.download_button(label="📥 Descargar todo como ZIP", data=create_zip(extracted_audios, audio_filenames), file_name="audios_extraidos.zip", mime="application/zip")
        else: st.warning("Por favor, sube al menos un video.")

with tab2:
    st.header("Conversor de Formatos de Audio")
    uploaded_audios = st.file_uploader("Sube archivos de audio", accept_multiple_files=True, type=["mp3", "wav", "ogg", "flac", "m4a"])
    target_audio_format = st.selectbox("Convertir a:", ["mp3", "wav", "ogg", "flac"], key="target_audio_format")
    if st.button("Convertir Audio", key="convert_audio_btn"):
        if uploaded_audios:
            with st.spinner("Convirtiendo audios..."):
                converted_audios, audio_filenames = [], []
                for audio_file in uploaded_audios:
                    audio_segment = AudioSegment.from_file(audio_file)
                    buffer = io.BytesIO()
                    audio_segment.export(buffer, format=target_audio_format)
                    converted_audios.append(buffer)
                    audio_filenames.append(f"{os.path.splitext(audio_file.name)[0]}.{target_audio_format}")
            st.success("¡Conversión de audio completada!")
            if len(converted_audios) == 1:
                st.download_button(label=f"📥 Descargar {audio_filenames[0]}", data=converted_audios[0], file_name=audio_filenames[0])
            else:
                st.download_button(label="📥 Descargar todo como ZIP", data=create_zip(converted_audios, audio_filenames), file_name="audios_convertidos.zip", mime="application/zip")
        else: st.warning("Por favor, sube al menos un archivo de audio.")

with tab3:
    st.header("Conversor de Formatos de Imagen")
    uploaded_images = st.file_uploader("Sube imágenes", accept_multiple_files=True, type=["png", "jpg", "jpeg", "bmp", "webp"])
    target_image_format = st.selectbox("Convertir a:", ["PNG", "JPEG", "WEBP", "BMP"], key="target_image_format")
    if st.button("Convertir Imágenes", key="convert_image_btn"):
        if uploaded_images:
            with st.spinner("Convirtiendo imágenes..."):
                converted_images, image_filenames = [], []
                for img_file in uploaded_images:
                    image = Image.open(img_file).convert("RGB" if target_image_format.lower() == 'jpeg' else "RGBA")
                    buffer = io.BytesIO()
                    image.save(buffer, format=target_image_format)
                    converted_images.append(buffer)
                    image_filenames.append(f"{os.path.splitext(img_file.name)[0]}.{target_image_format.lower()}")
            st.success("¡Conversión de imágenes completada!")
            if len(converted_images) == 1:
                st.download_button(label=f"📥 Descargar {image_filenames[0]}", data=converted_images[0], file_name=image_filenames[0])
            else:
                st.download_button(label="📥 Descargar todo como ZIP", data=create_zip(converted_images, image_filenames), file_name="imagenes_convertidas.zip", mime="application/zip")
        else: st.warning("Por favor, sube al menos una imagen.")
