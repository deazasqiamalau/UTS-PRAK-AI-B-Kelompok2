"""
Professional Sidebar Component
"""

import streamlit as st
import os
from pathlib import Path


def render_sidebar():
    """Render professional sidebar"""
    
    with st.sidebar:
        # Logo Section
        logo_path = Path("assets/logo (2).jpg")
        
        if logo_path.exists():
            st.image(str(logo_path), use_container_width=True)
        else:
            # Fallback gradient logo
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
                padding: 3rem 2rem;
                border-radius: 12px;
                text-align: center;
                color: white;
                margin-bottom: 1.5rem;
                box-shadow: 0 8px 24px rgba(59, 130, 246, 0.3);
            ">
                <div style="font-size: 3rem; margin-bottom: 0.5rem;">📱</div>
                <div style="font-size: 1.1rem; font-weight: 600;">Smartphone</div>
                <div style="font-size: 0.9rem; opacity: 0.9;">Expert System</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Navigation Header
        st.markdown("### 🧭 NAVIGASI")
        
        # Navigation Radio
        page = st.radio(
            "Pilih Halaman:",
            ["🏠 Home", "🔍 Diagnosis", "📜 Riwayat", "ℹ️ Tentang"],
            label_visibility="collapsed"
        )
        
        # Divider
        st.markdown("<hr style='margin: 1.5rem 0; border-color: #374151;'>", 
                   unsafe_allow_html=True)
        
        # Statistics Section
        st.markdown("### 📊 STATISTIK")
        
        total_diagnosis = len(st.session_state.get('diagnosis_history', []))
        
        st.metric(
            label="Total Diagnosis",
            value=total_diagnosis,
            delta="+1 Hari Ini" if total_diagnosis > 0 else None
        )
        
        # Divider
        st.markdown("<hr style='margin: 1.5rem 0; border-color: #374151;'>", 
                   unsafe_allow_html=True)
        
        # Info Section
        st.markdown("""
        <div style="
            text-align: center;
            color: #9ca3af;
            font-size: 0.85rem;
            line-height: 1.6;
        ">
            <div style="font-weight: 600; color: #d1d5db; margin-bottom: 0.5rem;">
                👥 KELOMPOK 2
            </div>
            <div style="margin-bottom: 0.75rem;">
                INF313 - Kecerdasan Artifisial
            </div>
            <div style="font-size: 0.75rem; opacity: 0.7;">
                © 2025 Smartphone Expert System
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick Actions (if needed)
        st.markdown("<hr style='margin: 1.5rem 0; border-color: #374151;'>", 
                   unsafe_allow_html=True)
    
    return page


def render_sidebar_footer():
    """Render sidebar footer"""
    st.sidebar.markdown("""
    <div style="
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid #374151;
        text-align: center;
        font-size: 0.75rem;
        color: #6b7280;
    ">
        <p>Developed with ❤️</p>
        <p>Version 1.0.0</p>
    </div>
    """, unsafe_allow_html=True)