import streamlit as st

def render_footer():
    st.markdown("""
    <div class="sidebar-footer">
        <p>© 2025 Kelompok 2</p>
        <p>INF313 - Kecerdasan Artifisial</p>
        <p>Version 1.0</p>
    </div>
    """, unsafe_allow_html=True)
