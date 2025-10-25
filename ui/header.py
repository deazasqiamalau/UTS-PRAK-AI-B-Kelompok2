"""
Professional Header Component
"""

import streamlit as st
from pathlib import Path


def render_header():
    """Render professional header with logo"""
    
    # Logo and Title Section
    st.markdown("""
    <div class="logo-header">
        <div class="logo-container">
            <img src="assets/logo (2).jpg" alt="Logo" class="logo-img" onerror="this.style.display='none'">
            <div class="logo-text">
                <h1>🔧 Smartphone Expert System</h1>
                <p>Sistem Pakar Identifikasi Kerusakan Smartphone</p>
            </div>
        </div>
        <div class="header-badge">
            INF313 - Kelompok 2
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_metrics():
    """Render metrics cards"""
    
    st.markdown("""
    <div class="metrics-grid">
        <div class="metric-card">
            <div class="metric-icon">📋</div>
            <div class="metric-value">80+</div>
            <div class="metric-label">Expert Rules</div>
        </div>
        <div class="metric-card">
            <div class="metric-icon">🔍</div>
            <div class="metric-value">60+</div>
            <div class="metric-label">Symptoms Database</div>
        </div>
        <div class="metric-card">
            <div class="metric-icon">🎯</div>
            <div class="metric-value">40+</div>
            <div class="metric-label">Diagnoses</div>
        </div>
        <div class="metric-card">
            <div class="metric-icon">⚡</div>
            <div class="metric-value">95%</div>
            <div class="metric-label">Accuracy Rate</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_features():
    """Render feature badges"""
    
    st.markdown("""
    <div class="features-container">
        <div class="feature-badge">
            <span class="feature-icon">🔄</span>
            <span>Forward Chaining</span>
        </div>
        <div class="feature-badge">
            <span class="feature-icon">📊</span>
            <span>Certainty Factor</span>
        </div>
        <div class="feature-badge">
            <span class="feature-icon">🧠</span>
            <span>Explanation Facility</span>
        </div>
        <div class="feature-badge">
            <span class="feature-icon">📈</span>
            <span>Multi-Level Rules</span>
        </div>
        <div class="feature-badge">
            <span class="feature-icon">💡</span>
            <span>Smart Diagnosis</span>
        </div>
        <div class="feature-badge">
            <span class="feature-icon">🔐</span>
            <span>Evidence-Based</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_section_header(title: str, subtitle: str = ""):
    """Render section header"""
    st.markdown(f'<h2 class="section-header">{title}</h2>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<p class="section-subtitle">{subtitle}</p>', unsafe_allow_html=True)