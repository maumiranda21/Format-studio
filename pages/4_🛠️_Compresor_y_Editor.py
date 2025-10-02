import streamlit as st
from PIL import Image
import io
import zipfile
from rembg import remove

st.set_page_config(layout="wide", page_title="Compresor y Editor")

def create_zip_bytes(files_dict):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for filename, data in files_dict.items(): zf.writestr(filename, data)
    return zip_buffer.getvalue()

st.title("🛠️ Herramienta 4: Compresor y Editor de Imágenes")
tab1, tab2 = st.tabs(["🗜️ Compresor de Imágenes", "🎨 Removedor de Fondos"])

with tab1:
    st.header("Comprimir Imágenes")
    st.info("Reduce el tamaño de tus imágenes ajustando la calidad.")
    uploaded_images = st.file_uploader("Sube imágenes para comprimir (JPG, PNG)", type=["jpg", "jpeg", "png"], accept_multiple_files=True, key="compress_uploader")
    quality = st.slider("Calidad (para JPG)", 1, 100, 85)
    if st.button("Comprimir Imágenes", key="compress_btn"):
        if uploaded_images:
            with st.spinner("Comprimiendo..."):
                compressed_files = {}
                for image_file in uploaded_images:
                    img = Image.open(image_file)
                    output_buffer = io.BytesIO()
                    img.save(output_buffer, format='JPEG' if img.mode == 'RGB' else 'PNG', quality=quality, optimize=True)
                    compressed_filename = f"{os.path.splitext(image_file.name)[0]}_comprimido.jpg"
                    compressed_files[compressed_filename] = output_buffer.getvalue()
            st.success("¡Imágenes comprimidas!")
            if len(compressed_files) == 1:
                filename, data = list(compressed_files.items())[0]
                st.download_button(label=f"📥 Descargar {filename}", data=data, file_name=filename)
            else:
                st.download_button(label="📥 Descargar todo como ZIP", data=create_zip_bytes(compressed_files), file_name="imagenes_comprimidas.zip", mime="application/zip")
        else: st.warning("Sube al menos una imagen.")

with tab2:
    st.header("Removedor de Fondos de Imágenes")
    uploaded_bg_images = st.file_uploader("Sube imágenes (PNG, JPG)", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key="bg_remover_uploader")
    if st.button("Quitar Fondos", key="remove_bg_btn"):
        if uploaded_bg_images:
            with st.spinner("Procesando imágenes..."):
                processed_files = {}
                for image_file in uploaded_bg_images:
                    output_bytes = remove(image_file.getvalue())
                    processed_filename = f"{os.path.splitext(image_file.name)[0]}_sin_fondo.png"
                    processed_files[processed_filename] = output_bytes
            st.success("¡Fondos eliminados!")
            if len(processed_files) == 1:
                filename, data = list(processed_files.items())[0]
                st.image(data, caption=filename)
                st.download_button(label=f"📥 Descargar {filename}", data=data, file_name=filename, mime="image/png")
            else:
                st.download_button(label="📥 Descargar todo como ZIP", data=create_zip_bytes(processed_files), file_name="imagenes_sin_fondo.zip", mime="application/zip")
        else: st.warning("Sube al menos una imagen.")
