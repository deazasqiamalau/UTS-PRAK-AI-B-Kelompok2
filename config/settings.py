"""
Configuration Settings
Konfigurasi sistem pakar smartphone
"""

import os
from pathlib import Path

# Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Knowledge Base Paths
KNOWLEDGE_BASE_DIR = os.path.join(BASE_DIR, 'knowledge_base')
RULES_FILE = os.path.join(KNOWLEDGE_BASE_DIR, 'rules.json')
SYMPTOMS_FILE = os.path.join(KNOWLEDGE_BASE_DIR, 'symptoms.json')
DIAGNOSES_FILE = os.path.join(KNOWLEDGE_BASE_DIR, 'diagnoses.json')

# Inference Engine Settings
INFERENCE_SETTINGS = {
    'max_iterations': 50,
    'max_depth': 10,
    'min_confidence': 0.5,
    'default_cf': 0.8
}

# Certainty Factor Settings
CF_SETTINGS = {
    'very_certain': 0.9,
    'certain': 0.7,
    'fairly_certain': 0.5,
    'uncertain': 0.3,
    'very_uncertain': 0.1
}

# CF Interpretation Thresholds
CF_INTERPRETATION = {
    'very_high': (0.9, 1.0),
    'high': (0.7, 0.9),
    'medium': (0.5, 0.7),
    'low': (0.3, 0.5),
    'very_low': (0.0, 0.3)
}

# Logging Settings
LOG_DIR = os.path.join(BASE_DIR, 'logs')
LOG_FILE = os.path.join(LOG_DIR, 'system.log')
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Export Settings
EXPORT_DIR = os.path.join(BASE_DIR, 'exports')
PDF_TEMPLATE = 'default'

# UI Settings
UI_SETTINGS = {
    'page_title': 'Smartphone Expert System',
    'page_icon': '📱',
    'layout': 'wide',
    'theme': {
        'primaryColor': '#667eea',
        'backgroundColor': '#ffffff',
        'secondaryBackgroundColor': '#f0f2f6',
        'textColor': '#262730',
        'font': 'sans serif'
    }
}

# Symptom Categories
SYMPTOM_CATEGORIES = {
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

# Diagnosis Types
DIAGNOSIS_TYPES = {
    'hardware': 'Hardware',
    'software': 'Software',
    'hybrid': 'Hardware & Software'
}

# Severity Levels
SEVERITY_LEVELS = {
    'critical': {
        'name': 'Kritis',
        'color': '#dc3545',
        'icon': '🚨'
    },
    'high': {
        'name': 'Tinggi',
        'color': '#fd7e14',
        'icon': '⚠️'
    },
    'medium': {
        'name': 'Sedang',
        'color': '#ffc107',
        'icon': '⚡'
    },
    'low': {
        'name': 'Rendah',
        'color': '#28a745',
        'icon': 'ℹ️'
    }
}

# Repair Difficulty
REPAIR_DIFFICULTY = {
    'very_low': {
        'name': 'Sangat Mudah',
        'description': 'Bisa dilakukan sendiri tanpa tools khusus',
        'icon': '😊'
    },
    'low': {
        'name': 'Mudah',
        'description': 'Perlu sedikit pengetahuan teknis',
        'icon': '🙂'
    },
    'medium': {
        'name': 'Sedang',
        'description': 'Memerlukan teknisi atau tools khusus',
        'icon': '😐'
    },
    'high': {
        'name': 'Sulit',
        'description': 'Harus dilakukan oleh teknisi profesional',
        'icon': '😰'
    },
    'very_high': {
        'name': 'Sangat Sulit',
        'description': 'Hanya bisa dilakukan di service center resmi',
        'icon': '😱'
    }
}

# System Messages
MESSAGES = {
    'welcome': """
    Selamat datang di Sistem Pakar Identifikasi Kerusakan Smartphone!
    
    Sistem ini akan membantu Anda mendiagnosis masalah pada smartphone
    berdasarkan gejala yang dialami. Pilih menu Diagnosis untuk memulai.
    """,
    
    'no_diagnosis': """
    Tidak dapat menemukan diagnosis yang sesuai dengan gejala yang dipilih.
    Cobalah:
    - Pilih lebih banyak gejala yang relevan
    - Periksa kembali gejala yang dipilih
    - Konsultasikan dengan teknisi profesional
    """,
    
    'critical_warning': """
    ⚠️ PERINGATAN PENTING ⚠️
    
    Diagnosis menunjukkan masalah KRITIS yang memerlukan perhatian SEGERA!
    Mohon JANGAN gunakan smartphone dan segera bawa ke teknisi profesional.
    """,
    
    'data_backup': """
    💾 Rekomendasi: Backup Data Anda
    
    Sebelum melakukan perbaikan, sangat disarankan untuk melakukan backup
    semua data penting (foto, kontak, dokumen, dll) untuk mencegah kehilangan data.
    """
}

# Validation Rules
VALIDATION = {
    'min_symptoms': 1,
    'max_symptoms': 15,
    'min_cf_user': 0.0,
    'max_cf_user': 1.0,
    'min_cf_rule': 0.0,
    'max_cf_rule': 1.0
}

# Cache Settings
CACHE_SETTINGS = {
    'enable': True,
    'ttl': 3600,  # Time to live in seconds (1 hour)
    'max_entries': 100
}

# API Settings (untuk future development)
API_SETTINGS = {
    'enable': False,
    'host': '0.0.0.0',
    'port': 8000,
    'debug': False
}

# Database Settings (untuk future development)
DATABASE_SETTINGS = {
    'type': 'json',  # json, sqlite, postgresql
    'backup_enabled': True,
    'backup_interval': 86400  # 24 hours
}

# Email Settings (untuk notifications - future)
EMAIL_SETTINGS = {
    'enable': False,
    'smtp_server': '',
    'smtp_port': 587,
    'sender_email': '',
    'sender_password': ''
}

# Analytics Settings
ANALYTICS = {
    'enable': True,
    'track_usage': True,
    'track_diagnosis': True,
    'track_errors': True
}

# Feature Flags
FEATURES = {
    'backward_chaining': True,
    'forward_chaining': True,
    'certainty_factor': True,
    'explanation_facility': True,
    'knowledge_acquisition': True,
    'export_pdf': True,
    'history': True,
    'statistics': True
}

# Development Settings
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
TESTING = os.getenv('TESTING', 'False').lower() == 'true'

# Version Info
VERSION = '1.0.0'
RELEASE_DATE = '2025-09-20'
AUTHORS = [
    'NADIA MAGHDALENA',
    'MUHAMMAD SIDQI ALFAREZA',
    'IRFAN SYAHPUTRA',
    'DEA ZASQIA PASARIBU MALAU',
    'HALIM ELSA PUTRA',
    'KHAIRUL BARRI FAIZ'
]

# Help & Support
SUPPORT = {
    'email': 'kelompok2.inf313@university.ac.id',
    'github': 'https://github.com/username/smartphone-expert-system',
    'documentation': 'https://github.com/username/smartphone-expert-system/wiki'
}


def get_config(key: str, default=None):
    """
    Get configuration value by key
    
    Args:
        key: Configuration key
        default: Default value if key not found
        
    Returns:
        Configuration value
    """
    return globals().get(key, default)


def validate_paths():
    """Validate and create necessary directories"""
    dirs = [
        KNOWLEDGE_BASE_DIR,
        LOG_DIR,
        EXPORT_DIR
    ]
    
    for dir_path in dirs:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(f"Created directory: {dir_path}")


# Auto-validate paths on import
if not TESTING:
    validate_paths()


# Example usage
if __name__ == "__main__":
    print("=" * 70)
    print("SYSTEM CONFIGURATION")
    print("=" * 70)
    
    print(f"\nVersion: {VERSION}")
    print(f"Release Date: {RELEASE_DATE}")
    print(f"Debug Mode: {DEBUG}")
    
    print("\nPaths:")
    print(f"  Base Dir: {BASE_DIR}")
    print(f"  Knowledge Base: {KNOWLEDGE_BASE_DIR}")
    print(f"  Logs: {LOG_DIR}")
    print(f"  Exports: {EXPORT_DIR}")
    
    print("\nInference Settings:")
    for key, value in INFERENCE_SETTINGS.items():
        print(f"  {key}: {value}")
    
    print("\nEnabled Features:")
    for feature, enabled in FEATURES.items():
        status = "✅" if enabled else "❌"
        print(f"  {status} {feature}")
    
    print("\n" + "=" * 70)