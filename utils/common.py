from email.policy import default
import streamlit as st
from sidebar import render_sidebar_logo

def initialize_page():
    """Initialize common page elements like the sidebar logo and language selector."""
    render_sidebar_logo()
    
    # Add language selector (moved from main page) with German being the default
    languages = {
        "🇩🇪 Deutsch": "Deutsch",
        "🇬🇧 English": "English",
        "🇫🇷 Français": "Français"
    }
    lang_choice = st.sidebar.selectbox("Select Language", list(languages.keys()), index=0)
    return languages[lang_choice] 