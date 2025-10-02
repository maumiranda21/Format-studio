import streamlit as st

st.set_page_config(
    page_title="App Multifuncional",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.title("🚀 Bienvenid@ a la App Multifuncional")

st.markdown("""
Esta aplicación ha sido creada con Streamlit para agrupar un conjunto de herramientas útiles en tu día a día.
La estructura está pensada para ser modular y escalable.

**Navega por las herramientas usando el menú de la izquierda.**

### Herramientas Disponibles:

1.  **🔀 Conversor de Audio e Imagen:**
    * Extrae audio de videos.
    * Convierte entre formatos de audio (MP3, WAV, OGG...).
    * Convierte entre formatos de imagen (PNG, JPG, WEBP...).

2.  **✍️ Transcriptor de Textos:**
    * Convierte voz de archivos de audio/video a texto (Español/Inglés).
    * Extrae texto de imágenes (OCR) (Español/Inglés).

3.  **📄 Conversor de Documentos:**
    * Convierte archivos PDF a formatos de Office (Word, Excel, PowerPoint).
    * Transforma entre formatos de texto plano como TXT, DOCX, RTF y Markdown.

4.  **🛠️ Compresor y Editor:**
    * Comprime imágenes, videos y PDFs para reducir su tamaño.
    * Elimina el fondo de imágenes de forma automática.

¡Espero que te sea de gran utilidad!

---
*Desarrollado con pasión y Python.*
""")
