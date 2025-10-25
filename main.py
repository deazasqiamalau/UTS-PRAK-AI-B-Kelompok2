"""
Smartphone Expert System - Professional Modular Version
Sistem Pakar Identifikasi Kerusakan Smartphone
Kelompok 2 - INF313 Kecerdasan Artifisial

Tim Pengembang:
- NADIA MAGHDALENA
- MUHAMMAD SIDQI ALFAREZA  
- IRFAN SYAHPUTRA
- DEA ZASQIA PASARIBU MALAU
- HALIM ELSA PUTRA
- KHAIRUL BARRI FAIZ
"""

import streamlit as st
import json
import sys
from datetime import datetime
from pathlib import Path

# Add directories to path
sys.path.append(str(Path(__file__).parent))

# Import custom modules
try:
    from inference_engine.forward_chaining import ForwardChaining
    from inference_engine.certainty_factor import CFCalculator
    from ui.style_optimized import get_custom_css
    from ui.header import render_header, render_metrics, render_features, render_section_header
    from ui.sidebar import render_sidebar
    from ui.info_box import render_info_box, render_instructions, render_welcome_message
except ImportError as e:
    st.error(f"❌ Error importing modules: {str(e)}")
    st.info("Make sure all files are in the correct directory structure.")
    st.stop()


# ========== PAGE CONFIG ==========
st.set_page_config(
    page_title="Smartphone Expert System",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)


# ========== SESSION STATE ==========
if 'diagnosis_history' not in st.session_state:
    st.session_state.diagnosis_history = []
if 'selected_symptoms' not in st.session_state:
    st.session_state.selected_symptoms = []
if 'current_diagnosis' not in st.session_state:
    st.session_state.current_diagnosis = None


# ========== UTILITY FUNCTIONS ==========
def load_json_file(filepath):
    """Load JSON file with error handling"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading {filepath}: {str(e)}")
        return None


@st.cache_data
def load_knowledge_base():
    """Load all knowledge base files"""
    kb_path = Path("knowledge_base")
    
    rules = load_json_file(kb_path / "rules.json")
    symptoms = load_json_file(kb_path / "symptoms.json")
    diagnoses = load_json_file(kb_path / "diagnoses.json")
    
    return rules, symptoms, diagnoses


# ========== PAGE FUNCTIONS ==========
def home_page():
    """Home page with overview"""
    render_header()
    render_metrics()
    render_features()
    
    st.markdown("<br>", unsafe_allow_html=True)
    render_welcome_message()
    
    # Quick Start Section
    st.markdown("<br>", unsafe_allow_html=True)
    render_section_header("🚀 Quick Start", "Mulai diagnosis dalam 3 langkah mudah")
    st.markdown(
        """
        <div class="quick-start-grid">
            <div class="quick-start-card">
                <div class="quick-start-icon">1️⃣</div>
                <div class="quick-start-title">Pilih Gejala</div>
                <p class="quick-start-text">Pilih gejala yang dialami smartphone dari kategori yang tersedia</p>
            </div>
            <div class="quick-start-card">
                <div class="quick-start-icon">2️⃣</div>
                <div class="quick-start-title">Set Keyakinan</div>
                <p class="quick-start-text">Tentukan seberapa yakin Anda dengan setiap gejala yang dipilih</p>
            </div>
            <div class="quick-start-card">
                <div class="quick-start-icon">3️⃣</div>
                <div class="quick-start-title">Dapatkan Hasil</div>
                <p class="quick-start-text">Sistem akan memberikan diagnosis dengan solusi lengkap</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def diagnosis_page():
    """Main diagnosis page"""
    render_header()
    render_section_header("🔍 Diagnosis Kerusakan Smartphone", 
                         "Sistem akan menganalisis gejala yang Anda pilih menggunakan Forward Chaining")
    
    # Load knowledge base
    rules, symptoms, diagnoses = load_knowledge_base()
    
    if not all([rules, symptoms, diagnoses]):
        st.error("❌ Gagal memuat knowledge base. Pastikan semua file JSON tersedia.")
        return
    
    # Instructions
    render_instructions()
    
    # Symptom selection
    st.markdown("<br>", unsafe_allow_html=True)
    render_section_header("📝 Pilih Gejala yang Dialami")
    
    symptoms_data = symptoms.get('symptoms', {})
    
    # Group symptoms by category
    categories = {}
    for symptom_id, symptom_info in symptoms_data.items():
        category = symptom_info.get('category', 'general')
        if category not in categories:
            categories[category] = []
        categories[category].append((symptom_id, symptom_info))
    
    selected_symptoms_with_cf = {}
    
    # Category names with icons
    category_names = {
        'display': '🖥️ Layar & Display',
        'battery': '🔋 Baterai',
        'charging': '⚡ Charging',
        'performance': '⚙️ Performa',
        'audio': '🔊 Audio',
        'connectivity': '📶 Konektivitas',
        'camera': '📷 Kamera',
        'sensor': '📡 Sensor',
        'button': '🔘 Tombol',
        'physical': '🔨 Kerusakan Fisik',
        'software': '💻 Software',
        'thermal': '🌡️ Suhu',
        'general': '📋 Umum'
    }
    
    # Display symptoms by category
    for category, symptom_list in sorted(categories.items()):
        with st.expander(f"{category_names.get(category, category.title())} ({len(symptom_list)} gejala)", 
                        expanded=False):
            for symptom_id, symptom_info in symptom_list:
                col1, col2 = st.columns([3, 2])
                
                with col1:
                    selected = st.checkbox(
                        symptom_info.get('name', symptom_id),
                        key=f"symptom_{symptom_id}",
                        help=symptom_info.get('description', '')
                    )
                
                with col2:
                    if selected:
                        cf_user = st.slider(
                            "Keyakinan",
                            0.0, 1.0, 0.8, 0.1,
                            key=f"cf_{symptom_id}",
                            help="Seberapa yakin Anda?"
                        )
                        selected_symptoms_with_cf[symptom_id] = cf_user
    
    # Show selected symptoms summary
    if selected_symptoms_with_cf:
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Modern summary with glassmorphism
        summary_html = f"""
<div class="diagnosis-summary">
    <div class="diagnosis-summary-header">
        <h3 class="diagnosis-summary-title">✅ Ringkasan Gejala Terpilih</h3>
        <span class="diagnosis-summary-meta">{len(selected_symptoms_with_cf)} gejala dipilih</span>
    </div>
    <div class="diagnosis-summary-list">
"""

        # Add each symptom with modern styling
        for symptom_id, cf in selected_symptoms_with_cf.items():
            symptom_name = symptoms_data.get(symptom_id, {}).get('name', symptom_id)
            percentage = cf * 100
            
            # Color based on confidence
            if percentage >= 80:
                bar_color = "#22c55e"
            elif percentage >= 60:
                bar_color = "#fbbf24"
            else:
                bar_color = "#3b82f6"
            
            summary_html += f"""
<div class="diagnosis-summary-item">
    <div class="diagnosis-summary-item-header">
        <span class="diagnosis-summary-item-label">{symptom_name}</span>
        <span class="diagnosis-summary-item-value" style="color: {bar_color};">{percentage:.0f}%</span>
    </div>
    <div class="diagnosis-summary-item-bar">
        <span style="width: {percentage}%; background: linear-gradient(90deg, {bar_color} 0%, {bar_color}dd 100%);"></span>
    </div>
</div>"""

        summary_html += """
    </div>
</div>
"""
        st.markdown(summary_html, unsafe_allow_html=True)

        # Diagnosis button
        with st.container():
            st.markdown('<div class="diagnosis-action">', unsafe_allow_html=True)
            diagnose_now = st.button("🔍 Diagnosa Sekarang", type="primary", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        if diagnose_now:
            if not selected_symptoms_with_cf:
                st.warning("⚠️ Mohon pilih minimal satu gejala!")
            else:
                perform_diagnosis(selected_symptoms_with_cf, rules, diagnoses)


def perform_diagnosis(symptoms_with_cf, rules, diagnoses):
    """Perform diagnosis using forward chaining"""
    
    with st.spinner('🔄 Menganalisis gejala dan melakukan inferensi...'):
        # Initialize inference engine
        engine = ForwardChaining()
        engine.reset()
        
        # Add facts
        symptom_ids = list(symptoms_with_cf.keys())
        engine.add_facts(symptom_ids)
        
        # Run inference
        results = engine.forward_chain()
        
        # Calculate CF for each diagnosis
        calculator = CFCalculator()
        final_diagnoses_with_cf = []
        
        for diag in results.get('final_diagnoses', []):
            diagnosis_id = diag['diagnosis']
            explaining_rules = engine.explain_reasoning(diagnosis_id)
            
            evidences = []
            for rule in explaining_rules:
                rule_cf = rule.get('cf', 0.8)
                conditions = rule.get('conditions', [])
                user_cfs = [symptoms_with_cf.get(cond, 1.0) for cond in conditions]
                avg_user_cf = sum(user_cfs) / len(user_cfs) if user_cfs else 1.0
                
                evidences.append({
                    'id': rule['rule_id'],
                    'rule_cf': rule_cf,
                    'user_cf': avg_user_cf
                })
            
            if evidences:
                cf_result = calculator.calculate_and_track(diagnosis_id, evidences)
                final_diagnoses_with_cf.append({
                    'diagnosis': diagnosis_id,
                    'cf': cf_result['final_cf'],
                    'percentage': cf_result['percentage'],
                    'category': cf_result['category'],
                    'description': cf_result['description'],
                    'evidence_details': cf_result['evidence_details']
                })
        
        # Sort by CF
        final_diagnoses_with_cf.sort(key=lambda x: x['cf'], reverse=True)
        
        # Display results
        if final_diagnoses_with_cf:
            display_diagnosis_results(final_diagnoses_with_cf, results, engine, diagnoses, symptoms_with_cf)
            
            # Save to history
            st.session_state.diagnosis_history.append({
                'timestamp': datetime.now().isoformat(),
                'symptoms': list(symptoms_with_cf.keys()),
                'diagnoses': final_diagnoses_with_cf[:3]
            })
            
            st.success("✅ Diagnosis berhasil disimpan ke riwayat!")
        else:
            st.warning("⚠️ Tidak dapat menemukan diagnosis yang sesuai. Coba pilih gejala lain atau tambah lebih banyak gejala.")


def display_diagnosis_results(diagnoses_with_cf, inference_results, engine, diagnoses_db, symptoms):
    """Display diagnosis results professionally with improved UI"""
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    render_section_header("📊 Hasil Diagnosis", "Berikut adalah hasil analisis sistem pakar")
    
    # Display top diagnoses
    for i, diag in enumerate(diagnoses_with_cf[:5], 1):
        diagnosis_id = diag['diagnosis']
        diagnosis_info = diagnoses_db.get('diagnoses', {}).get(diagnosis_id, {})
        percentage = diag['percentage']
        
        # Determine badge color
        if percentage >= 80:
            badge_color = "#22c55e"
            badge_bg = "rgba(34, 197, 94, 0.2)"
            icon = "✅"
        elif percentage >= 60:
            badge_color = "#fbbf24"
            badge_bg = "rgba(251, 191, 36, 0.2)"
            icon = "⚠️"
        else:
            badge_color = "#3b82f6"
            badge_bg = "rgba(59, 130, 246, 0.2)"
            icon = "ℹ️"
        
        # Diagnosis Card Header
        st.markdown(f"""
<div class="diagnosis-card-wrapper">
    <div class="diagnosis-card">
        <div class="diagnosis-header">
            <div class="diagnosis-title">{icon} Diagnosis #{i}: {diagnosis_info.get('name', diagnosis_id)}</div>
            <div class="diagnosis-badge" style="background: {badge_bg}; color: {badge_color}; border: 1px solid {badge_color};">
                {percentage:.1f}% - {diag['category']}
            </div>
        </div>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 1.5rem;">
            <div style="background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%); padding: 1rem; border-radius: 10px; border: 1px solid rgba(59, 130, 246, 0.3);">
                <div style="font-size: 0.85rem; color: #94a3b8; text-transform: uppercase; font-weight: 600; margin-bottom: 0.5rem;">Tipe</div>
                <div style="font-size: 1.2rem; font-weight: 700; color: #60a5fa;">{diagnosis_info.get('type', 'Unknown').upper()}</div>
            </div>
            <div style="background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%); padding: 1rem; border-radius: 10px; border: 1px solid rgba(59, 130, 246, 0.3);">
                <div style="font-size: 0.85rem; color: #94a3b8; text-transform: uppercase; font-weight: 600; margin-bottom: 0.5rem;">Severity</div>
                <div style="font-size: 1.2rem; font-weight: 700; color: #60a5fa;">{diagnosis_info.get('severity', 'medium').upper()}</div>
            </div>
        </div>
        <div style="background: rgba(15, 23, 42, 0.4); border-radius: 10px; padding: 1.5rem; border: 1px solid rgba(59, 130, 246, 0.2);">
            <div style="font-size: 0.9rem; color: #94a3b8; font-weight: 600; margin-bottom: 0.75rem;">📝 DESKRIPSI</div>
            <div style="color: #cbd5e1; line-height: 1.8;">{diagnosis_info.get('description', '-')}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
        
        # Detailed information in expander
        with st.expander(f"📋 Lihat Detail Lengkap & Solusi", expanded=False):
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Penyebab
                st.markdown("#### 🔍 Penyebab Kemungkinan")
                if diagnosis_info.get('causes'):
                    for cause in diagnosis_info.get('causes', []):
                        st.markdown(f"- {cause}")
                else:
                    st.markdown("_Tidak ada data penyebab_")
                
                st.markdown("")
                
                # Pencegahan
                st.markdown("#### 🛡️ Pencegahan")
                if diagnosis_info.get('prevention'):
                    for prev in diagnosis_info.get('prevention', []):
                        st.markdown(f"- {prev}")
                else:
                    st.markdown("_Tidak ada data pencegahan_")
            
            with col2:
                # Solusi
                st.markdown("#### 💡 Solusi Perbaikan")
                if diagnosis_info.get('solutions'):
                    for sol in diagnosis_info.get('solutions', []):
                        st.markdown(f"""
                        <div class="solution-step">
                            <strong>Langkah {sol.get('step')}: {sol.get('action')}</strong>
                            <div style="color: #94a3b8; font-style: italic;">{sol.get('detail')}</div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown("_Tidak ada data solusi_")
                
                st.markdown("")
                
                # Estimasi Biaya
                cost = diagnosis_info.get('estimated_cost', '0')
                if cost != '0':
                    st.markdown("#### 💰 Estimasi Biaya")
                    st.markdown(f"""
                    <div class="cost-badge">Rp {cost}</div>
                    """, unsafe_allow_html=True)
            
            # Reasoning Section with improved styling
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("---")
            explanation = engine.how_question(diagnosis_id)
            
            # Format reasoning explanation
            reasoning_lines = explanation.split('\n')
            reasoning_html = '<div class="reasoning-container">'
            reasoning_html += '<div class="reasoning-header">🧠 Penjelasan Reasoning</div>'
            reasoning_html += '<div class="reasoning-content">'
            
            for line in reasoning_lines:
                if line.strip():
                    # Highlight rule IDs and important keywords
                    formatted_line = line
                    if 'RULE' in line or 'Rule' in line:
                        formatted_line = f'<strong>{line}</strong>'
                    elif '=>' in line or '->' in line:
                        parts = line.split('=>') if '=>' in line else line.split('->')
                        if len(parts) == 2:
                            formatted_line = f'<span style="color: #60a5fa;">{parts[0]}</span> <strong style="color: #a78bfa;">=></strong> <span style="color: #22c55e;">{parts[1]}</span>'
                    
                    reasoning_html += f'<div class="reasoning-line">{formatted_line}</div>'
            
            reasoning_html += '</div></div>'
            st.markdown(reasoning_html, unsafe_allow_html=True)
    
    # Statistics with improved layout
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("📈 Statistik Inferensi & Detail Teknis", expanded=False):
        
        st.markdown("""
        <div class="stats-container">
            <div class="stat-card">
                <div class="stat-value">""" + str(inference_results['iterations']) + """</div>
                <div class="stat-label">Total Iterasi</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">""" + str(len(inference_results['fired_rules'])) + """</div>
                <div class="stat-label">Rules Aktif</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">""" + str(len(inference_results['inferred_facts'])) + """</div>
                <div class="stat-label">Fakta Terinferensi</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="margin-top: 2rem;">
            <h4 style="color: #60a5fa; margin-bottom: 1rem;">📜 Rules yang Digunakan:</h4>
            <div class="rules-list">
        """, unsafe_allow_html=True)
        
        for rule_id in inference_results['fired_rules']:
            st.markdown(f'<div class="rule-item">{rule_id}</div>', unsafe_allow_html=True)
        
        st.markdown("</div></div>", unsafe_allow_html=True)
        st.markdown("**Rules yang Digunakan:**")
        for rule_id in inference_results['fired_rules']:
            st.code(rule_id)
    

def history_page():
    """Diagnosis history page"""
    render_header()
    render_section_header("📜 Riwayat Diagnosis", "Lihat semua diagnosis yang pernah dilakukan")
    
    if not st.session_state.diagnosis_history:
        st.info("📭 Belum ada riwayat diagnosis. Lakukan diagnosis terlebih dahulu di menu Diagnosis.")
        return
    
    for i, history in enumerate(reversed(st.session_state.diagnosis_history), 1):
        timestamp = datetime.fromisoformat(history['timestamp'])
        formatted_time = timestamp.strftime("%d %B %Y, %H:%M:%S")
        
        with st.expander(f"📋 Diagnosis #{len(st.session_state.diagnosis_history) - i + 1} - {formatted_time}"):
            st.markdown("**Gejala yang Dipilih:**")
            for symptom in history['symptoms']:
                st.markdown(f"- {symptom}")
            
            st.markdown("**Hasil Diagnosis:**")
            for diag in history['diagnoses']:
                st.markdown(f"- **{diag['diagnosis']}**: {diag['percentage']:.1f}% ({diag['category']})")


def about_page():
    """About page"""
    render_header()
    render_section_header("ℹ️ Tentang Sistem", "Informasi lengkap tentang Smartphone Expert System")
    
    st.markdown("""
    ### 📱 Sistem Pakar Identifikasi Kerusakan Smartphone
    
    Sistem pakar berbasis **rule-based reasoning** dengan **forward chaining** dan **certainty factor** 
    untuk diagnosis kerusakan smartphone secara otomatis dan akurat.
    
    #### 🎯 Fitur Unggulan:
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        - ✅ **80+ Expert Rules** - Berbasis jurnal ilmiah
        - ✅ **Forward Chaining** - Data-driven reasoning
        - ✅ **Certainty Factor** - Handling uncertainty
        - ✅ **Explanation Facility** - WHY & HOW questions
        """)
    
    with col2:
        st.markdown("""
        - ✅ **60+ Symptoms** - Database gejala lengkap
        - ✅ **40+ Diagnoses** - Solusi komprehensif
        - ✅ **Multi-Level Rules** - 1-3 symptoms
        - ✅ **Professional UI** - Modern & user-friendly
        """)
    
    st.markdown("#### 📚 Knowledge Base References:")
    st.markdown("""
    1. Zhang, L., et al. (2021). *Journal of Computing and Information Technology*
    2. Kumar, S., & Sharma, A. (2022). *International Journal of Electronics*
    3. Chen, W., et al. (2023). *IEEE Transactions on Mobile Computing*
    4. Patel, R., & Johnson, M. (2022). *Expert Systems with Applications*
    5. Lee, H., et al. (2023). *Journal of Information Technology and Applications*
    """)
    
    st.markdown("#### 👥 Tim Pengembang - Kelompok 2")
    
    team_members = [
        "NADIA MAGHDALENA",
        "MUHAMMAD SIDQI ALFAREZA",
        "IRFAN SYAHPUTRA",
        "DEA ZASQIA PASARIBU MALAU",
        "HALIM ELSA PUTRA",
    ]
    
    cols = st.columns(3)
    for i, member in enumerate(team_members):
        with cols[i % 3]:
            st.markdown(f"""
            <div style="background: white; padding: 1.5rem; border-radius: 12px; 
                 border: 2px solid #e5e7eb; text-align: center; margin-bottom: 1rem;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">👤</div>
                <p style="font-weight: 600; color: #1f2937; margin: 0;">{member}</p>
            </div>
            """, unsafe_allow_html=True)


# ========== MAIN APPLICATION ==========
def main():
    """Main application entry point"""
    
    # Render sidebar and get selected page
    page = render_sidebar()
    
    # Route to appropriate page
    if page == "🏠 Home":
        home_page()
    elif page == "🔍 Diagnosis":
        diagnosis_page()
    elif page == "📜 Riwayat":
        history_page()
    elif page == "ℹ️ Tentang":
        about_page()


if __name__ == "__main__":
    main()
