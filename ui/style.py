"""
Professional UI Styles
Clean, Modern, and Enterprise-grade Design
"""

def get_custom_css():
    """Return professional CSS styling"""
    return """
    <style>
        /* Import Professional Font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        /* ========== GLOBAL RESET ========== */
        * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        /* Hide Streamlit Branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {display: none;}
        
        /* ========== MAIN LAYOUT ========== */
        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }
        
        .main .block-container {
            padding: 2rem 3rem !important;
            max-width: 1400px !important;
            background: white;
            border-radius: 16px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
            margin-top: 2rem;
        }
        
        /* ========== LOGO SECTION ========== */
        .logo-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 1.5rem 0;
            border-bottom: 2px solid #e5e7eb;
            margin-bottom: 2rem;
        }
        
        .logo-container {
            display: flex;
            align-items: center;
            gap: 1.5rem;
        }
        
        .logo-img {
            width: 80px;
            height: 80px;
            object-fit: contain;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }
        
        .logo-text h1 {
            font-size: 1.8rem;
            font-weight: 700;
            color: #1f2937;
            margin-bottom: 0.25rem;
            line-height: 1.2;
        }
        
        .logo-text p {
            font-size: 0.95rem;
            color: #6b7280;
            font-weight: 500;
        }
        
        .header-badge {
            display: inline-block;
            padding: 0.5rem 1rem;
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
            color: white;
            border-radius: 8px;
            font-size: 0.875rem;
            font-weight: 600;
            box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
        }
        
        /* ========== METRICS CARDS ========== */
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }
        
        .metric-card {
            background: white;
            border: 2px solid #e5e7eb;
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .metric-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #3b82f6, #8b5cf6);
            transform: scaleX(0);
            transition: transform 0.3s ease;
        }
        
        .metric-card:hover::before {
            transform: scaleX(1);
        }
        
        .metric-card:hover {
            border-color: #3b82f6;
            box-shadow: 0 8px 24px rgba(59, 130, 246, 0.15);
            transform: translateY(-4px);
        }
        
        .metric-icon {
            font-size: 2.5rem;
            margin-bottom: 0.75rem;
        }
        
        .metric-value {
            font-size: 2.5rem;
            font-weight: 700;
            color: #3b82f6;
            line-height: 1;
            margin-bottom: 0.5rem;
        }
        
        .metric-label {
            font-size: 0.95rem;
            color: #6b7280;
            font-weight: 500;
        }
        
        /* ========== FEATURE BADGES ========== */
        .features-container {
            display: flex;
            flex-wrap: wrap;
            gap: 0.75rem;
            margin: 1.5rem 0;
            padding: 1.5rem;
            background: #f9fafb;
            border-radius: 12px;
            border: 1px solid #e5e7eb;
        }
        
        .feature-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            font-size: 0.875rem;
            font-weight: 500;
            color: #374151;
            transition: all 0.2s ease;
        }
        
        .feature-badge:hover {
            border-color: #3b82f6;
            color: #3b82f6;
            box-shadow: 0 2px 8px rgba(59, 130, 246, 0.1);
        }
        
        .feature-icon {
            font-size: 1.1rem;
        }
        
        /* ========== SECTION HEADERS ========== */
        .section-header {
            font-size: 1.75rem;
            font-weight: 700;
            color: #1f2937;
            margin: 2.5rem 0 1.5rem 0;
            padding-bottom: 0.75rem;
            border-bottom: 3px solid #3b82f6;
            display: inline-block;
        }
        
        .section-subtitle {
            font-size: 1rem;
            color: #6b7280;
            margin-bottom: 1.5rem;
            line-height: 1.6;
        }
        
        /* ========== INFO BOXES ========== */
        .info-box {
            background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
            border-left: 4px solid #3b82f6;
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1.5rem 0;
            box-shadow: 0 2px 8px rgba(59, 130, 246, 0.1);
        }
        
        .info-box h4 {
            color: #1e40af;
            font-weight: 600;
            font-size: 1.1rem;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .info-box ol, .info-box ul {
            margin-left: 1.5rem;
            line-height: 1.8;
            color: #1e3a8a;
        }
        
        .info-box li {
            margin-bottom: 0.5rem;
        }
        
        .success-box {
            background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
            border-left: 4px solid #22c55e;
        }
        
        .success-box h3 {
            color: #166534;
        }
        
        .warning-box {
            background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
            border-left: 4px solid #f59e0b;
        }
        
        .warning-box h3 {
            color: #92400e;
        }
        
        .danger-box {
            background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
            border-left: 4px solid #ef4444;
        }
        
        .danger-box h3 {
            color: #991b1b;
        }
        
        /* ========== BUTTONS ========== */
        .stButton>button {
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
            color: white !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
            padding: 0.875rem 2rem !important;
            border-radius: 10px !important;
            border: none !important;
            box-shadow: 0 4px 14px rgba(59, 130, 246, 0.4) !important;
            transition: all 0.3s ease !important;
            text-transform: none !important;
            letter-spacing: 0.3px !important;
        }
        
        .stButton>button:hover {
            box-shadow: 0 6px 20px rgba(59, 130, 246, 0.5) !important;
            transform: translateY(-2px) !important;
        }
        
        .stButton>button:active {
            transform: translateY(0) !important;
        }
        
        /* ========== EXPANDERS ========== */
        .streamlit-expanderHeader {
            background: white !important;
            border: 2px solid #e5e7eb !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
            color: #374151 !important;
            padding: 1rem 1.5rem !important;
            font-size: 0.95rem !important;
            transition: all 0.2s ease !important;
        }
        
        .streamlit-expanderHeader:hover {
            background: #f9fafb !important;
            border-color: #3b82f6 !important;
            color: #3b82f6 !important;
        }
        
        .streamlit-expanderContent {
            border: 2px solid #e5e7eb !important;
            border-top: none !important;
            border-radius: 0 0 10px 10px !important;
            padding: 1.5rem !important;
            background: #fafafa !important;
        }
        
        /* ========== CHECKBOXES & INPUTS ========== */
        .stCheckbox {
            padding: 0.5rem 0 !important;
        }
        
        .stCheckbox label {
            font-weight: 500 !important;
            color: #374151 !important;
            cursor: pointer !important;
        }
        
        .stCheckbox label:hover {
            color: #3b82f6 !important;
        }
        
        /* ========== SIDEBAR ========== */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1f2937 0%, #111827 100%) !important;
        }
        
        [data-testid="stSidebar"] > div:first-child {
            padding: 1.5rem 1rem !important;
        }
        
        [data-testid="stSidebar"] h3 {
            color: #f9fafb !important;
            font-weight: 600 !important;
            font-size: 0.875rem !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
            margin: 2rem 0 1rem 0 !important;
        }
        
        [data-testid="stSidebar"] .stRadio > label {
            background: rgba(255, 255, 255, 0.05) !important;
            color: #d1d5db !important;
            padding: 0.875rem 1rem !important;
            border-radius: 8px !important;
            margin: 0.4rem 0 !important;
            font-weight: 500 !important;
            transition: all 0.2s ease !important;
            border: 1px solid transparent !important;
        }
        
        [data-testid="stSidebar"] .stRadio > label:hover {
            background: rgba(59, 130, 246, 0.15) !important;
            color: #60a5fa !important;
            border-color: rgba(59, 130, 246, 0.3) !important;
        }
        
        [data-testid="stSidebar"] [data-testid="stMetricValue"] {
            color: #60a5fa !important;
            font-size: 2.5rem !important;
            font-weight: 700 !important;
        }
        
        /* ========== SCROLLBAR ========== */
        ::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f5f9;
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #3b82f6, #8b5cf6);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, #2563eb, #7c3aed);
        }
        
        /* ========== ALERTS ========== */
        .stAlert {
            background: white !important;
            border: 2px solid #e5e7eb !important;
            border-left: 4px solid #3b82f6 !important;
            border-radius: 10px !important;
            padding: 1rem 1.5rem !important;
        }
        
        /* ========== METRICS ========== */
        [data-testid="stMetric"] {
            background: white !important;
            border: 2px solid #e5e7eb !important;
            border-radius: 12px !important;
            padding: 1.25rem !important;
            transition: all 0.2s ease !important;
        }
        
        [data-testid="stMetric"]:hover {
            border-color: #3b82f6 !important;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1) !important;
        }
        
        /* ========== DIVIDER ========== */
        hr {
            border: none;
            border-top: 2px solid #e5e7eb;
            margin: 2rem 0;
        }
        
        /* ========== SPINNER ========== */
        .stSpinner > div {
            border-color: #3b82f6 !important;
            border-right-color: transparent !important;
        }
        
        /* ========== CODE BLOCKS ========== */
        .stCodeBlock {
            background: #1f2937 !important;
            border: 2px solid #374151 !important;
            border-radius: 10px !important;
        }
        
        /* ========== RESPONSIVE ========== */
        @media (max-width: 768px) {
            .main .block-container {
                padding: 1rem !important;
            }
            
            .logo-text h1 {
                font-size: 1.4rem;
            }
            
            .metrics-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
    """