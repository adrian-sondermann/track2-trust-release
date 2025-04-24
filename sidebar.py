import streamlit as st
import os

def render_sidebar_logo():
    """Render the logo in the sidebar from the static images folder using the working directory."""
    BASE_DIR = os.getcwd()
    image_path = os.path.join(BASE_DIR, "static", "images", "logo.png")
    st.sidebar.image(image_path, use_container_width=True)

