"""
AI-Assisted Skin Disease Detection System
Main Application Controller - Professional Medical SaaS Design

Pure HTML/CSS implementation with minimal Streamlit
"""

import streamlit as st
from auth import login, logout
from user_portal import user_dashboard
from doctor_portal import doctor_dashboard


def inject_medical_saas_css():
    """
    Complete CSS framework for professional medical SaaS dashboard
    """
    st.markdown("""
    <style>
    /* ==================== GOOGLE FONTS ==================== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* ==================== CSS VARIABLES ==================== */
    :root {
        /* Primary Colors */
        --primary: #2F80ED;
        --primary-dark: #1E5FBF;
        --primary-light: #E3F2FD;
        --primary-gradient: linear-gradient(135deg, #2F80ED 0%, #1E5FBF 100%);
        
        /* Neutral Colors */
        --background: #F7F9FC;
        --card-bg: #FFFFFF;
        --text-primary: #1F2937;
        --text-secondary: #6B7280;
        --text-light: #9CA3AF;
        --border: #E5E7EB;
        
        /* Status Colors */
        --success: #10B981;
        --success-light: #D1FAE5;
        --success-dark: #065F46;
        --warning: #F59E0B;
        --warning-light: #FEF3C7;
        --warning-dark: #92400E;
        --error: #EF4444;
        --error-light: #FEE2E2;
        --error-dark: #991B1B;
        --info: #3B82F6;
        --info-light: #DBEAFE;
        --info-dark: #1E40AF;
        
        /* Shadows */
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        
        /* Spacing */
        --spacing-xs: 0.25rem;
        --spacing-sm: 0.5rem;
        --spacing-md: 1rem;
        --spacing-lg: 1.5rem;
        --spacing-xl: 2rem;
        --spacing-2xl: 3rem;
        
        /* Border Radius */
        --radius-sm: 6px;
        --radius-md: 8px;
        --radius-lg: 12px;
        --radius-xl: 16px;
        --radius-2xl: 20px;
    }
    
    /* ==================== GLOBAL RESET ==================== */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* ==================== HIDE STREAMLIT BRANDING ==================== */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* ==================== BASE STYLES ==================== */
    .stApp {
        background-color: var(--background);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    .main .block-container {
        padding: 2rem;
        max-width: 100%;
    }
    
    /* ==================== TYPOGRAPHY ==================== */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        color: var(--text-primary);
        letter-spacing: -0.02em;
        line-height: 1.2;
    }
    
    h1 { font-size: 2rem; font-weight: 700; }
    h2 { font-size: 1.5rem; font-weight: 600; }
    h3 { font-size: 1.25rem; font-weight: 600; }
    h4 { font-size: 1.125rem; font-weight: 600; }
    
    p {
        color: var(--text-secondary);
        line-height: 1.6;
        font-size: 1rem;
    }
    
    /* ==================== MEDICAL CARD SYSTEM ==================== */
    .medical-card {
        background: var(--card-bg);
        border-radius: var(--radius-lg);
        padding: var(--spacing-xl);
        box-shadow: var(--shadow);
        border: 1px solid var(--border);
        margin-bottom: var(--spacing-lg);
        transition: all 0.3s ease;
        animation: fadeIn 0.5s ease-out;
    }
    
    .medical-card:hover {
        box-shadow: var(--shadow-md);
        transform: translateY(-2px);
    }
    
    .medical-card-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: var(--spacing-md);
        padding-bottom: var(--spacing-md);
        border-bottom: 2px solid var(--primary-light);
    }
    
    .medical-card-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--text-primary);
        margin: 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .medical-card-body {
        padding: var(--spacing-md) 0;
    }
    
    .medical-card-footer {
        margin-top: var(--spacing-md);
        padding-top: var(--spacing-md);
        border-top: 1px solid var(--border);
    }
    
    /* ==================== LOGIN PAGE ==================== */
    .login-page {
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, var(--primary-light) 0%, var(--background) 100%);
        padding: 2rem;
    }
    
    .login-container {
        max-width: 480px;
        width: 100%;
        background: var(--card-bg);
        border-radius: var(--radius-xl);
        padding: 3rem;
        box-shadow: var(--shadow-xl);
        border: 1px solid var(--border);
        animation: slideUp 0.5s ease-out;
    }
    
    .login-header {
        text-align: center;
        margin-bottom: 2.5rem;
    }
    
    .login-logo {
        width: 80px;
        height: 80px;
        background: var(--primary-gradient);
        border-radius: var(--radius-2xl);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.5rem;
        margin: 0 auto 1.5rem;
        box-shadow: 0 8px 16px rgba(47, 128, 237, 0.25);
    }
    
    .login-title {
        font-size: 2rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }
    
    .login-subtitle {
        color: var(--text-secondary);
        font-size: 0.9375rem;
        line-height: 1.5;
    }
    
    .login-footer {
        margin-top: 2rem;
        padding-top: 2rem;
        border-top: 1px solid var(--border);
        text-align: center;
    }
    
    .login-footer p {
        font-size: 0.875rem;
        color: var(--text-secondary);
        margin: 0.5rem 0;
    }
    
    .security-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.875rem;
        color: var(--success);
        font-weight: 500;
    }
    
    /* ==================== DASHBOARD HEADER ==================== */
    .dashboard-header {
        background: var(--primary-gradient);
        padding: 2rem;
        border-radius: var(--radius-lg);
        margin-bottom: 2rem;
        box-shadow: var(--shadow-md);
        animation: fadeIn 0.5s ease-out;
    }
    
    .dashboard-header h1 {
        color: white;
        margin: 0;
        font-size: 2rem;
        font-weight: 700;
    }
    
    .dashboard-header p {
        color: rgba(255, 255, 255, 0.9);
        margin: 0.5rem 0 0 0;
        font-size: 1.125rem;
    }
    
    /* ==================== STAT CARDS ==================== */
    .stat-card {
        background: var(--card-bg);
        border-radius: var(--radius-lg);
        padding: 1.5rem;
        box-shadow: var(--shadow);
        border: 1px solid var(--border);
        border-left: 4px solid var(--primary);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .stat-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-lg);
    }
    
    .stat-card-label {
        font-size: 0.875rem;
        font-weight: 600;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }
    
    .stat-card-value {
        font-size: 2.25rem;
        font-weight: 700;
        color: var(--text-primary);
        line-height: 1;
        margin-bottom: 0.5rem;
    }
    
    .stat-card-change {
        font-size: 0.875rem;
        color: var(--text-secondary);
    }
    
    .stat-card-icon {
        position: absolute;
        top: 1rem;
        right: 1rem;
        font-size: 2.5rem;
        opacity: 0.08;
    }
    
    /* Stat card color variants */
    .stat-card-blue {
        background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
        border-left-color: var(--primary);
    }
    
    .stat-card-blue .stat-card-value {
        color: var(--info-dark);
    }
    
    .stat-card-yellow {
        background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%);
        border-left-color: var(--warning);
    }
    
    .stat-card-yellow .stat-card-value {
        color: var(--warning-dark);
    }
    
    .stat-card-green {
        background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%);
        border-left-color: var(--success);
    }
    
    .stat-card-green .stat-card-value {
        color: var(--success-dark);
    }
    
    .stat-card-purple {
        background: linear-gradient(135deg, #F5F3FF 0%, #EDE9FE 100%);
        border-left-color: #8B5CF6;
    }
    
    .stat-card-purple .stat-card-value {
        color: #5B21B6;
    }
    
    .stat-card-orange {
        background: linear-gradient(135deg, #FFF7ED 0%, #FFEDD5 100%);
        border-left-color: #F97316;
    }
    
    .stat-card-orange .stat-card-value {
        color: #9A3412;
    }
    
    /* ==================== BADGE SYSTEM ==================== */
    .badge {
        display: inline-flex;
        align-items: center;
        padding: 0.375rem 0.75rem;
        border-radius: var(--radius-sm);
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        gap: 0.25rem;
    }
    
    .badge-success {
        background: var(--success-light);
        color: var(--success-dark);
    }
    
    .badge-warning {
        background: var(--warning-light);
        color: var(--warning-dark);
    }
    
    .badge-error {
        background: var(--error-light);
        color: var(--error-dark);
    }
    
    .badge-info {
        background: var(--info-light);
        color: var(--info-dark);
    }
    
    .badge-primary {
        background: var(--primary);
        color: white;
    }
    
    /* ==================== UPLOAD ZONE ==================== */
    .upload-zone {
        background: var(--card-bg);
        border: 2px dashed var(--border);
        border-radius: var(--radius-lg);
        padding: 3rem 2rem;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .upload-zone:hover {
        border-color: var(--primary);
        background: var(--primary-light);
    }
    
    .upload-zone-icon {
        font-size: 3rem;
        color: var(--text-light);
        margin-bottom: 1rem;
    }
    
    .upload-zone-title {
        font-size: 1.125rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }
    
    .upload-zone-subtitle {
        font-size: 0.875rem;
        color: var(--text-secondary);
    }
    
    /* ==================== RESULT HIGHLIGHT BOX ==================== */
    .result-highlight {
        background: linear-gradient(135deg, var(--primary-light) 0%, #FFFFFF 100%);
        border: 2px solid var(--primary);
        border-radius: var(--radius-lg);
        padding: 2rem;
        box-shadow: var(--shadow-md);
        text-align: center;
        margin: 1.5rem 0;
        animation: scaleIn 0.5s ease-out;
    }
    
    .result-title {
        font-size: 0.875rem;
        font-weight: 600;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.75rem;
    }
    
    .result-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--primary-dark);
        margin-bottom: 1rem;
        line-height: 1.2;
    }
    
    .result-confidence {
        display: inline-block;
        background: var(--success);
        color: white;
        padding: 0.5rem 1.5rem;
        border-radius: 20px;
        font-size: 1rem;
        font-weight: 600;
        box-shadow: var(--shadow);
    }
    
    /* ==================== INFO BOX ==================== */
    .info-box {
        background: var(--card-bg);
        padding: 1rem;
        border-radius: var(--radius-md);
        border-left: 4px solid;
        margin: 1rem 0;
    }
    
    .info-box-primary {
        background: var(--info-light);
        border-left-color: var(--info);
    }
    
    .info-box-primary p {
        color: var(--info-dark);
        margin: 0;
    }
    
    .info-box-success {
        background: var(--success-light);
        border-left-color: var(--success);
    }
    
    .info-box-success p {
        color: var(--success-dark);
        margin: 0;
    }
    
    .info-box-warning {
        background: var(--warning-light);
        border-left-color: var(--warning);
    }
    
    .info-box-warning p {
        color: var(--warning-dark);
        margin: 0;
    }
    
    /* ==================== CASE CARD ==================== */
    .case-card {
        background: var(--card-bg);
        border-radius: var(--radius-lg);
        padding: 1.5rem;
        box-shadow: var(--shadow);
        border: 1px solid var(--border);
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
    }
    
    .case-card:hover {
        box-shadow: var(--shadow-md);
    }
    
    .case-card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }
    
    .case-card-title {
        font-size: 1rem;
        font-weight: 600;
        color: var(--text-primary);
        margin: 0;
    }
    
    .case-card-date {
        font-size: 0.875rem;
        color: var(--text-secondary);
    }
    
    .case-card-content {
        padding: 1rem 0;
    }
    
    .case-card-image {
        width: 100%;
        border-radius: var(--radius-md);
        margin-bottom: 1rem;
        box-shadow: var(--shadow-sm);
    }
    
    /* ==================== BUTTONS ==================== */
    .stButton > button {
        background: var(--primary-gradient);
        color: white;
        border: none;
        border-radius: var(--radius-md);
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: var(--shadow);
        width: 100%;
        cursor: pointer;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Secondary button */
    .stButton > button[kind="secondary"] {
        background: white;
        color: var(--primary);
        border: 2px solid var(--primary);
    }
    
    .stButton > button[kind="secondary"]:hover {
        background: var(--primary-light);
    }
    
    /* ==================== FORM INPUTS ==================== */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stTextArea > div > div > textarea,
    .stDateInput > div > div > input,
    .stTimeInput > div > div > input {
        border-radius: var(--radius-md);
        border: 2px solid var(--border);
        padding: 0.75rem;
        font-size: 1rem;
        transition: all 0.3s ease;
        background: var(--card-bg);
        font-family: 'Inter', sans-serif;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary);
        box-shadow: 0 0 0 3px var(--primary-light);
        outline: none;
    }
    
    .stTextInput > label,
    .stSelectbox > label,
    .stTextArea > label,
    .stDateInput > label,
    .stTimeInput > label {
        font-weight: 600;
        color: var(--text-primary);
        font-size: 0.9375rem;
        margin-bottom: 0.5rem;
    }
    
    /* ==================== FILE UPLOADER ==================== */
    .stFileUploader {
        background: var(--card-bg);
        border: 2px dashed var(--border);
        border-radius: var(--radius-lg);
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .stFileUploader:hover {
        border-color: var(--primary);
        background: var(--primary-light);
    }
    
    .stFileUploader label {
        font-weight: 600;
        color: var(--text-primary);
    }
    
    /* ==================== ALERTS ==================== */
    .stSuccess, .stInfo, .stWarning, .stError {
        border-radius: var(--radius-md);
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid;
        font-weight: 500;
    }
    
    .stSuccess {
        background: var(--success-light);
        border-left-color: var(--success);
        color: var(--success-dark);
    }
    
    .stInfo {
        background: var(--info-light);
        border-left-color: var(--info);
        color: var(--info-dark);
    }
    
    .stWarning {
        background: var(--warning-light);
        border-left-color: var(--warning);
        color: var(--warning-dark);
    }
    
    .stError {
        background: var(--error-light);
        border-left-color: var(--error);
        color: var(--error-dark);
    }
    
    /* ==================== TABS ==================== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: transparent;
        border-bottom: 2px solid var(--border);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border: none;
        border-radius: var(--radius-md) var(--radius-md) 0 0;
        color: var(--text-secondary);
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: var(--primary-light);
        color: var(--primary);
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--card-bg);
        color: var(--primary);
        border-bottom: 3px solid var(--primary);
    }
    
    /* ==================== METRICS ==================== */
    .stMetric {
        background: var(--card-bg);
        padding: 1.25rem;
        border-radius: var(--radius-lg);
        border: 1px solid var(--border);
        box-shadow: var(--shadow);
        transition: all 0.3s ease;
    }
    
    .stMetric:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-md);
    }
    
    .stMetric label {
        font-size: 0.875rem;
        color: var(--text-secondary);
        font-weight: 500;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary);
    }
    
    /* ==================== SIDEBAR ==================== */
    [data-testid="stSidebar"] {
        background: var(--card-bg);
        border-right: 1px solid var(--border);
        padding: 2rem 1rem;
    }
    
    [data-testid="stSidebar"] h2 {
        color: var(--text-primary);
        font-weight: 700;
        font-size: 1.25rem;
        margin-bottom: 1.5rem;
    }
    
    /* ==================== EXPANDER ==================== */
    .streamlit-expanderHeader {
        background: var(--card-bg);
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
        padding: 0.75rem 1rem;
        font-weight: 600;
        color: var(--text-primary);
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: var(--primary-light);
        border-color: var(--primary);
    }
    
    /* ==================== IMAGE ==================== */
    .stImage {
        border-radius: var(--radius-md);
        overflow: hidden;
        box-shadow: var(--shadow);
    }
    
    /* ==================== DATAFRAME ==================== */
    .stDataFrame {
        border-radius: var(--radius-md);
        overflow: hidden;
        box-shadow: var(--shadow);
    }
    
    /* ==================== DIVIDER ==================== */
    hr {
        border: none;
        border-top: 2px solid var(--border);
        margin: 2rem 0;
    }
    
    /* ==================== ANIMATIONS ==================== */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes scaleIn {
        from {
            opacity: 0;
            transform: scale(0.95);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    /* ==================== UTILITY CLASSES ==================== */
    .text-center { text-align: center; }
    .text-left { text-align: left; }
    .text-right { text-align: right; }
    
    .mb-1 { margin-bottom: var(--spacing-sm); }
    .mb-2 { margin-bottom: var(--spacing-md); }
    .mb-3 { margin-bottom: var(--spacing-lg); }
    .mb-4 { margin-bottom: var(--spacing-xl); }
    
    .mt-1 { margin-top: var(--spacing-sm); }
    .mt-2 { margin-top: var(--spacing-md); }
    .mt-3 { margin-top: var(--spacing-lg); }
    .mt-4 { margin-top: var(--spacing-xl); }
    
    .p-2 { padding: var(--spacing-md); }
    .p-3 { padding: var(--spacing-lg); }
    .p-4 { padding: var(--spacing-xl); }
    
    /* ==================== RESPONSIVE ==================== */
    @media (max-width: 768px) {
        .login-container {
            margin: 1rem;
            padding: 2rem 1.5rem;
        }
        
        h1 { font-size: 1.5rem; }
        h2 { font-size: 1.25rem; }
        
        .medical-card {
            padding: 1rem;
        }
        
        .stat-card-value {
            font-size: 1.75rem;
        }
    }
    
    </style>
    """, unsafe_allow_html=True)


def main():
    """
    Main application controller
    """
    
    # Initialize session state
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    
    if "username" not in st.session_state:
        st.session_state["username"] = ""
    
    if "role" not in st.session_state:
        st.session_state["role"] = ""
    
    # Page configuration
    st.set_page_config(
        page_title="MediScan AI - Professional Healthcare Platform",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="auto"
    )
    
    # Inject comprehensive CSS
    inject_medical_saas_css()
    
    # Route to appropriate view
    if not st.session_state["logged_in"]:
        show_login_page()
    else:
        if st.session_state["role"] == "User":
            user_dashboard(st.session_state["username"])
        elif st.session_state["role"] == "Doctor":
            doctor_dashboard()
        else:
            st.error("Invalid role detected. Please login again.")
            logout()


def show_login_page():
    """
    Display professional medical SaaS login page with pure HTML/CSS
    """
    
    # Create centered layout
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Login container HTML
        st.markdown("""
        <div class="login-container">
            <div class="login-header">
                <div class="login-logo">🏥</div>
                <h1 class="login-title">MediScan AI</h1>
                <p class="login-subtitle">
                    Advanced Skin Disease Detection Platform<br>
                    Powered by Artificial Intelligence
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Call Streamlit login function (backend)
        login()
        
        # Login footer
        st.markdown("""
            <div class="login-footer">
                <p class="security-badge">
                    🔒 HIPAA Compliant & Secure
                </p>
                <p>
                    AI-Powered Medical Analysis • Real-time Doctor Verification
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()