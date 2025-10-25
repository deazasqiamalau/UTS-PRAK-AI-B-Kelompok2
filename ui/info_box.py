"""
Professional Info Box Components
"""

import streamlit as st


def render_info_box(title: str, content: str, icon: str = "ℹ️"):
    """Render professional info box"""
    st.markdown(f"""
    <div class="info-box">
        <h4>{icon} {title}</h4>
        {content}
    </div>
    """, unsafe_allow_html=True)


def render_success_box(title: str, content: str, icon: str = "✅"):
    """Render success box"""
    st.markdown(f"""
    <div class="info-box success-box">
        <h3>{icon} {title}</h3>
        {content}
    </div>
    """, unsafe_allow_html=True)


def render_warning_box(title: str, content: str, icon: str = "⚠️"):
    """Render warning box"""
    st.markdown(f"""
    <div class="info-box warning-box">
        <h3>{icon} {title}</h3>
        {content}
    </div>
    """, unsafe_allow_html=True)


def render_danger_box(title: str, content: str, icon: str = "🚨"):
    """Render danger box"""
    st.markdown(f"""
    <div class="info-box danger-box">
        <h3>{icon} {title}</h3>
        {content}
    </div>
    """, unsafe_allow_html=True)


def render_instructions():
    """Render diagnosis instructions"""
    content = """
    <ol>
        <li><strong>Pilih gejala</strong> yang dialami smartphone Anda dari kategori di bawah</li>
        <li><strong>Tentukan tingkat keyakinan</strong> Anda terhadap setiap gejala (0-100%)</li>
        <li>Anda dapat <strong>memilih lebih dari satu gejala</strong> untuk hasil yang lebih akurat</li>
        <li>Klik tombol <strong>"🔍 Diagnosa Sekarang"</strong> untuk mendapatkan hasil</li>
    </ol>
    <div style="margin-top: 1rem; padding: 1rem; background: rgba(59, 130, 246, 0.1); border-radius: 8px; border-left: 3px solid #3b82f6;">
        <strong>💡 Tips Profesional:</strong> Semakin banyak gejala yang dipilih dengan akurat, 
        semakin presisi diagnosis yang diberikan sistem!
    </div>
    """
    render_info_box("📋 Petunjuk Penggunaan", content)


def render_welcome_message():
    """Render welcome message on home page"""
    content = """
    <p style="font-size: 1.05rem; line-height: 1.8; color: #374151; margin-bottom: 1rem;">
        Selamat datang di <strong>Smartphone Expert System</strong>, sistem pakar berbasis 
        <em>rule-based reasoning</em> yang dirancang untuk membantu Anda mengidentifikasi 
        kerusakan pada smartphone dengan cepat dan akurat.
    </p>
    
    <div style="background: white; padding: 1.5rem; border-radius: 10px; border: 2px solid #e5e7eb; margin-top: 1.5rem;">
        <h4 style="color: #1f2937; margin-bottom: 1rem;">✨ Keunggulan Sistem:</h4>
        <ul style="line-height: 1.8; color: #374151;">
            <li><strong>80+ Expert Rules</strong> - Berbasis jurnal ilmiah internasional</li>
            <li><strong>Multi-Level Diagnosis</strong> - Dari 1 gejala sudah dapat hasil!</li>
            <li><strong>Certainty Factor</strong> - Menunjukkan tingkat kepercayaan diagnosis</li>
            <li><strong>Explanation Facility</strong> - Transparansi proses reasoning</li>
            <li><strong>Evidence-Based</strong> - Rekomendasi solusi yang actionable</li>
        </ul>
    </div>
    
    <div style="margin-top: 1.5rem; padding: 1.25rem; background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%); border-radius: 10px; border-left: 4px solid #3b82f6;">
        <p style="margin: 0; font-size: 1rem; color: #1e40af;">
            <strong>🚀 Siap memulai?</strong> Pilih menu <strong>Diagnosis</strong> di sidebar 
            untuk mengidentifikasi masalah smartphone Anda!
        </p>
    </div>
    """
    render_info_box("👋 Selamat Datang!", content, icon="")