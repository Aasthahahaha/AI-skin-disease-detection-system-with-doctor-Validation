"""
AI-Assisted Skin Disease Detection System
Main Application Controller
Supports Dynamic Theme Switching (Dark Glassmorphism <-> Light Corporate)
"""

import streamlit as st
from auth import login, logout
from user_portal import user_dashboard
from doctor_portal import doctor_dashboard


# ══════════════════════════════════════════════════════════════════════════════
# THEME 1: DARK GLASSMORPHISM (Original Premium Theme)
# ══════════════════════════════════════════════════════════════════════════════
def get_dark_css():
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    :root {
        --bg-base:       #050c1a;
        --bg-surface:    #0a1628;
        --bg-elevated:   #0f2040;
        --glass-bg:      rgba(255,255,255,0.04);
        --glass-border:  rgba(255,255,255,0.10);
        --glass-hover:   rgba(255,255,255,0.07);
        --glass-blur:    blur(20px);
        --primary:       #4f9cf9;
        --primary-dark:  #2563eb;
        --primary-light: rgba(79,156,249,0.25);
        --primary-glow:  rgba(79,156,249,0.25);
        --cyan:          #06b6d4;
        --purple:        #7c3aed;
        --purple-light:  rgba(124,58,237,0.20);
        --success:       #10b981;
        --success-light: rgba(16,185,129,0.15);
        --success-dark:  #059669;
        --warning:       #f59e0b;
        --warning-light: rgba(245,158,11,0.15);
        --warning-dark:  #d97706;
        --error:         #ef4444;
        --error-light:   rgba(239,68,68,0.15);
        --error-dark:    #dc2626;
        --info:          #3b82f6;
        --info-light:    rgba(59,130,246,0.15);
        --text-primary:   #f1f5f9;
        --text-secondary: #94a3b8;
        --text-muted:     #475569;
        --r-sm: 8px; --r-md: 12px; --r-lg: 16px; --r-xl: 20px;
        --shadow-glow:  0 0 30px rgba(79,156,249,0.12);
        --shadow-card:  0 4px 24px rgba(0,0,0,0.4);
    }

    * { margin:0; padding:0; box-sizing:border-box; }
    #MainMenu, footer, header, .stDeployButton { display:none !important; }

    .stApp {
        background: var(--bg-base) !important;
        background-image:
            radial-gradient(ellipse at 20% 0%, rgba(79,156,249,0.08) 0%, transparent 50%),
            radial-gradient(ellipse at 80% 100%, rgba(124,58,237,0.06) 0%, transparent 50%) !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: var(--text-primary);
    }
    .main .block-container { padding: 1.5rem 2rem 3rem; max-width: 100%; }

    h1,h2,h3,h4,h5,h6 { font-family: 'Inter', sans-serif; font-weight: 700; color: var(--text-primary); }
    h1 { font-size: 2rem; } h2 { font-size: 1.5rem; font-weight: 600; }
    p  { color: var(--text-secondary); line-height: 1.6; font-size: 0.95rem; margin: 0; }
    hr { border: none; border-top: 1px solid var(--glass-border); margin: 1.5rem 0; }

    .stMarkdown, .element-container { color: var(--text-primary) !important; }

    .stTextInput > label, .stSelectbox > label, .stTextArea > label,
    .stDateInput > label, .stTimeInput > label, .stRadio > label {
        color: var(--text-primary) !important; font-weight: 500;
    }

    .stTextInput > div > div > input, .stTextArea > div > div > textarea, .stDateInput > div > div > input {
        background: var(--glass-bg) !important; border: 1px solid var(--glass-border) !important;
        border-radius: var(--r-md) !important; color: var(--text-primary) !important; padding: 0.65rem 0.9rem;
    }
    .stTextInput > div > div > input:focus { border-color: var(--primary) !important; box-shadow: 0 0 0 3px var(--primary-glow) !important; }

    .stSelectbox > div > div { background: var(--glass-bg) !important; border: 1px solid var(--glass-border) !important; color: white !important; }
    .stSelectbox > div > div > div { color: white !important; }
    /* Fix selectbox dropdown options for dark theme */
    div[role="listbox"] { background: var(--bg-elevated) !important; }
    div[role="option"] { color: var(--text-primary) !important; }
    div[role="option"]:hover { background: var(--primary-dark) !important; }

    .stButton > button, .stFormSubmitButton > button {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%) !important;
        color: white !important; border: none !important; border-radius: var(--r-md) !important;
        padding: 0.65rem 1.5rem !important; font-weight: 600 !important; width: 100% !important;
    }
    .stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 8px 24px rgba(79,156,249,0.4) !important; filter: brightness(1.1) !important; }
    .stButton > button[kind="secondary"] { background: var(--glass-bg) !important; border: 1px solid var(--glass-border) !important; color: var(--text-secondary) !important; }

    /* Custom Radio styling for Dark Mode (Segmented Controls) */
    .stRadio > label { display: none !important; }
    .stRadio > div { gap: 0.5rem; display: flex; flex-direction: row; }
    .stRadio [role="radiogroup"] { 
        display: inline-flex; gap: 0; background: rgba(0,0,0,0.2); padding: 4px; border-radius: var(--r-md); border: 1px solid var(--glass-border); width: 100%;
    }
    .stRadio [role="radio"] { 
        background: transparent !important; border: none !important; color: var(--text-secondary);
        padding: 0.6rem 1.2rem; border-radius: var(--r-sm); font-weight: 600; cursor: pointer;
        flex: 1; justify-content: center; text-align: center; display: flex; align-items: center;
        transition: all 0.2s ease;
    }
    .stRadio [role="radio"] div:first-child { display: none !important; }
    .stRadio [role="radio"] p { margin: 0; font-weight: 600; font-size: 0.95rem; }

    .stRadio [role="radio"][aria-checked="true"] { 
        background: rgba(79,156,249,0.2) !important; color: white !important; 
        box-shadow: inset 0 0 0 1px var(--primary);
    }
    .stRadio [role="radio"][aria-checked="true"] p { color: white !important; }
    
    /* FIX POPOVER CONTRAST (SELECTBOX DROPDOWN) */
    [data-baseweb="popover"], [data-baseweb="popover"] > div, [data-baseweb="menu"] {
        background-color: var(--bg-surface) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: var(--r-md) !important;
    }
    [data-baseweb="menu"] ul, [data-baseweb="menu"] li {
        background-color: transparent !important;
        color: white !important;
    }
    [data-baseweb="menu"] li:hover { background-color: var(--primary-dark) !important; }
    .stTabs [data-baseweb="tab-list"] { background: var(--glass-bg) !important; border: 1px solid var(--glass-border); padding: 0.3rem; border-radius: var(--r-lg); }
    .stTabs [data-baseweb="tab"] { color: var(--text-secondary) !important; border-radius: var(--r-md) !important; }
    .stTabs [aria-selected="true"] { background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%) !important; color: white !important; }

    [data-testid="stSidebar"] { background: var(--bg-surface) !important; border-right: 1px solid var(--glass-border) !important; }

    .dashboard-header { background: linear-gradient(135deg, rgba(37,99,235,0.6) 0%, rgba(124,58,237,0.4) 100%); backdrop-filter: var(--glass-blur); border: 1px solid rgba(79,156,249,0.3); border-radius: var(--r-xl); padding: 2rem 2.5rem; margin-bottom: 1.5rem; }
    .dashboard-header h1 { color: #ffffff !important; }
    .dashboard-header p { color: #f1f5f9 !important; }
    
    .medical-card { background: var(--glass-bg); backdrop-filter: var(--glass-blur); border: 1px solid var(--glass-border); border-radius: var(--r-lg); padding: 1.5rem; margin-bottom: 1.25rem; }
    .medical-card-header { border-bottom: 1px solid var(--glass-border); margin-bottom: 1rem; padding-bottom: 0.75rem; }
    .medical-card-title { font-size: 1.1rem; }

    .stat-card { background: var(--glass-bg); border: 1px solid var(--glass-border); border-radius: var(--r-lg); padding: 1.25rem; position: relative; }
    .stat-card-blue { border-left: 3px solid var(--primary); }
    .stat-card-yellow { border-left: 3px solid var(--warning); }
    .stat-card-green { border-left: 3px solid var(--success); }
    .stat-card-purple { border-left: 3px solid var(--purple); }
    .stat-card-icon { position:absolute; top:1rem; right:1rem; font-size:2rem; opacity:0.12; }
    .stat-card-label { font-size:0.75rem; font-weight:600; text-transform:uppercase; color:var(--text-secondary); margin-bottom:0.4rem; }
    .stat-card-value { font-size:2.25rem; font-weight:800; }
    
    .case-card, .doctor-card { background: var(--glass-bg); border: 1px solid var(--glass-border); border-radius: var(--r-lg); padding: 1.25rem; margin-bottom: 1rem; }
    .dtag { background: rgba(255,255,255,0.05); border: 1px solid var(--glass-border); color: var(--text-secondary); border-radius: 50px; padding: 0.2rem 0.65rem; font-size: 0.72rem; }

    .badge-success { background: var(--success-light); color: var(--success); border: 1px solid rgba(16,185,129,0.3); }
    .badge-warning { background: var(--warning-light); color: var(--warning); border: 1px solid rgba(245,158,11,0.3); }
    .badge-error { background: var(--error-light); color: var(--error); border: 1px solid rgba(239,68,68,0.3); }

    .info-box { padding: 0.85rem 1rem; border-radius: var(--r-md); border-left: 4px solid; margin: 0.75rem 0; }
    .info-box-primary { background: var(--info-light); border-left-color: var(--primary); }
    .info-box-success { background: var(--success-light); border-left-color: var(--success); }
    .info-box-warning { background: var(--warning-light); border-left-color: var(--warning); }

    .sidebar-profile { text-align:center; padding: 1rem 0; border-bottom: 1px solid var(--glass-border); margin-bottom: 1rem; }
    .sidebar-avatar { font-size:3.5rem; margin-bottom:0.5rem; }
    .sidebar-name { font-size:1.1rem; font-weight:700; color:var(--text-primary); }
    .sidebar-stats { display:flex; justify-content:space-around; padding:1rem 0; }
    .sidebar-stat-num { display:block; font-size:1.5rem; font-weight:800; color:var(--text-primary); }
    .sidebar-stat-label { display:block; font-size:0.7rem; color:var(--text-secondary); text-transform:uppercase; font-weight: 600; }

    /* AUTH.PY LEFT PANEL COMPATIBILITY */
    .split-left-panel {
        background: linear-gradient(135deg, var(--primary) 0%, var(--purple) 100%);
        border-radius: 20px; color: white; padding: 4rem 3rem; height: 100%; min-height: 500px;
        display: flex; flex-direction: column; justify-content: space-between;
    }
    .brand-title { font-size: 2.5rem; font-weight: 800; color: white !important; }
    .brand-subtitle { font-size: 1.25rem; opacity: 0.9; color: white !important; }
    .right-panel-header h2 { color: var(--text-primary); font-weight: 800; }
    </style>
    """


# ══════════════════════════════════════════════════════════════════════════════
# THEME 2: LIGHT CORPORATE (Stitch UI Inspired)
# ══════════════════════════════════════════════════════════════════════════════
def get_light_css():
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    :root {
        --bg-base:       #F3F6F9;
        --bg-surface:    #FFFFFF;
        --bg-elevated:   #FFFFFF;
        --primary:       #004A99; 
        --primary-dark:  #003370;
        --primary-light: #E6F0FA;
        --primary-glow:  rgba(0, 74, 153, 0.15);
        --cyan:          #005B99; 
        --glass-border:  #E1E4E8;
        --glass-bg:      #FFFFFF;
        --success:       #059669; --success-light: #D1FAE5; --success-dark:  #047857;
        --warning:       #D97706; --warning-light: #FEF3C7; --warning-dark:  #B45309;
        --error:         #DC2626; --error-light:   #FEE2E2; --error-dark:    #B91C1C;
        --info:          #2563EB; --info-light:    #DBEAFE; --info-dark:     #1D4ED8;
        --text-primary:   #111827; 
        --text-secondary: #4B5563; 
        --text-muted:     #6B7280;
        --r-sm: 6px; --r-md: 8px; --r-lg: 12px; --r-xl: 16px;
        --shadow-glow:  0 4px 14px rgba(0,74,153,0.08);
        --shadow-card:  0 4px 12px rgba(0,0,0,0.03), 0 1px 3px rgba(0,0,0,0.05);
    }

    * { margin:0; padding:0; box-sizing:border-box; }
    #MainMenu, footer, header, .stDeployButton { display:none !important; }

    .stApp {
        background: var(--bg-base) !important;
        background-image: radial-gradient(circle at 50% 0%, #FFFFFF 0%, #F3F6F9 70%) !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: var(--text-primary);
    }
    .main .block-container { padding: 1.5rem 2rem 3rem; max-width: 100%; }

    h1,h2,h3,h4,h5,h6 { font-family: 'Inter', sans-serif; font-weight: 700; color: var(--text-primary); letter-spacing: -0.01em; }
    h1 { font-size: 2rem; color: var(--primary); }
    h2 { font-size: 1.5rem; font-weight: 600; }
    p  { color: var(--text-secondary); line-height: 1.6; font-size: 0.95rem; margin: 0; }
    hr { border: none; border-top: 1px solid var(--glass-border); margin: 1.5rem 0; }

    .stMarkdown, .element-container { color: var(--text-primary) !important; }

    .stTextInput > label, .stSelectbox > label, .stTextArea > label,
    .stDateInput > label, .stTimeInput > label, .stRadio > label {
        color: var(--text-primary) !important; font-weight: 600; font-size: 0.9rem;
    }

    .stTextInput > div > div > input, .stTextArea > div > div > textarea, .stDateInput > div > div > input {
        background: #FFFFFF !important; border: 1px solid #CBD5E1 !important;
        border-radius: var(--r-md) !important; color: var(--text-primary) !important; padding: 0.75rem 1rem;
    }
    .stTextInput > div > div > input:focus { border-color: var(--primary) !important; box-shadow: 0 0 0 3px var(--primary-light) !important; }

    .stSelectbox > div > div { background: #FFFFFF !important; border: 1px solid #CBD5E1 !important; color: var(--text-primary) !important; }
    .stSelectbox > div > div > div { color: var(--text-primary) !important; }
    /* Fix selectbox dropdown options for light theme */
    div[role="listbox"] { background: #FFFFFF !important; }
    div[role="option"] { color: var(--text-primary) !important; }
    div[role="option"]:hover { background: var(--primary-light) !important; }

    .stButton > button, .stFormSubmitButton > button {
        background: var(--primary) !important; color: white !important; border: none !important;
        border-radius: var(--r-md) !important; padding: 0.75rem 1.5rem !important; font-weight: 600 !important; width: 100% !important;
    }
    .stButton > button:hover { background: var(--primary-dark) !important; box-shadow: 0 4px 10px rgba(0,74,153,0.25) !important; }
    .stButton > button[kind="secondary"] { background: #FFFFFF !important; border: 1px solid var(--glass-border) !important; color: var(--text-primary) !important; box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important; }

    /* PROFESSIONAL RADIO BUTTONS (SEGMENTED CONTROLS) */
    .stRadio > label { display: none !important; } /* Hide label if we use our own */
    .stRadio [role="radiogroup"] { 
        display: inline-flex; gap: 0; background: #F1F5F9; padding: 4px; border-radius: var(--r-md); border: 1px solid #E2E8F0; width: 100%;
    }
    .stRadio [role="radio"] {
        background: transparent !important; border: none !important; color: var(--text-secondary);
        padding: 0.6rem 1.2rem; border-radius: var(--r-sm); font-weight: 600; cursor: pointer;
        flex: 1; justify-content: center; text-align: center; display: flex; align-items: center;
        transition: all 0.2s ease;
    }
    /* Hide the native radio circles */
    .stRadio [role="radio"] div:first-child { display: none !important; }
    .stRadio [role="radio"] p { margin: 0; font-weight: 600; font-size: 0.95rem; }
    
    .stRadio [role="radio"][aria-checked="true"] {
        background: #FFFFFF !important; color: var(--primary) !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.12) !important;
    }
    .stRadio [role="radio"][aria-checked="true"] p { color: var(--primary) !important; }

    /* FIX INVISIBLE DROPDOWN MENUS (POPOVER) */
    [data-baseweb="popover"], [data-baseweb="popover"] > div, [data-baseweb="menu"] {
        background-color: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: var(--r-md) !important;
    }
    [data-baseweb="menu"] ul, [data-baseweb="menu"] li {
        background-color: #FFFFFF !important;
        color: var(--text-primary) !important;
    }
    [data-baseweb="menu"] li:hover { background-color: var(--primary-light) !important; }
    .stTabs [data-baseweb="tab-list"] { background: #F4F5F7 !important; border-radius: var(--r-md); padding: 0.3rem; border: none; }
    .stTabs [data-baseweb="tab"] { color: var(--text-secondary) !important; border-radius: var(--r-sm) !important; font-weight: 600 !important; }
    .stTabs [aria-selected="true"] { background: #FFFFFF !important; color: var(--primary) !important; box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important; }

    [data-testid="stSidebar"] { background: #FFFFFF !important; border-right: 1px solid var(--glass-border) !important; box-shadow: 1px 0 10px rgba(0,0,0,0.02); }

    .dashboard-header { background: #FFFFFF; border: 1px solid var(--glass-border); border-radius: var(--r-xl); padding: 2rem 2.5rem; margin-bottom: 1.5rem; box-shadow: var(--shadow-card); }
    .dashboard-header h1 { color: var(--primary) !important; }
    .dashboard-header p { color: var(--text-secondary) !important; }

    .medical-card { background: #FFFFFF; border: 1px solid var(--glass-border); border-radius: var(--r-lg); padding: 1.5rem; margin-bottom: 1.25rem; box-shadow: var(--shadow-card); }
    .medical-card-header { border-bottom: 1px solid #F3F4F6; margin-bottom: 1rem; padding-bottom: 0.75rem; }
    
    .stat-card { background: #FFFFFF; border: 1px solid var(--glass-border); border-radius: var(--r-lg); padding: 1.25rem; position: relative; box-shadow: var(--shadow-card); }
    .stat-card-blue { border-left: 4px solid var(--info); }
    .stat-card-yellow { border-left: 4px solid var(--warning); }
    .stat-card-green { border-left: 4px solid var(--success); }
    .stat-card-purple { border-left: 4px solid #8B5CF6; }
    .stat-card-icon { position:absolute; top:1rem; right:1.2rem; font-size:1.8rem; opacity:0.8; }
    .stat-card-label { font-size:0.75rem; font-weight:700; text-transform:uppercase; color:var(--text-secondary); margin-bottom:0.4rem; }
    .stat-card-value { font-size:2.25rem; font-weight:800; color: var(--text-primary); }
    
    .case-card, .doctor-card { background: #FFFFFF; border: 1px solid var(--glass-border); border-radius: var(--r-md); padding: 1.25rem; margin-bottom: 1rem; box-shadow: var(--shadow-card); }
    .dtag { background: #F3F4F6; color: var(--text-secondary); border-radius: 50px; padding: 0.2rem 0.65rem; font-size: 0.72rem; font-weight: 500; border: 1px solid #E5E7EB; }

    .badge-success { background: var(--success-light); color: var(--success-dark); }
    .badge-warning { background: var(--warning-light); color: var(--warning-dark); }
    .badge-error { background: var(--error-light); color: var(--error-dark); }

    .info-box { padding: 0.85rem 1rem; border-radius: var(--r-md); border-left: 4px solid; margin: 0.75rem 0; background: #F9FAFB; border-color: #CBD5E1; }
    .info-box p { color: var(--text-primary) !important; }
    .info-box-primary { background: var(--info-light); border-left-color: var(--info); }
    .info-box-success { background: var(--success-light); border-left-color: var(--success); }
    .info-box-warning { background: var(--warning-light); border-left-color: var(--warning); }

    .sidebar-profile { text-align:center; padding: 1rem 0; border-bottom: 1px solid #F3F4F6; margin-bottom: 1rem; }
    .sidebar-avatar { font-size:3.5rem; margin-bottom:0.5rem; }
    .sidebar-name { font-size:1.1rem; font-weight:700; color:var(--text-primary); }
    .sidebar-stats { display:flex; justify-content:space-around; padding:1rem 0; }
    .sidebar-stat-num { display:block; font-size:1.5rem; font-weight:800; color:var(--text-primary); }
    .sidebar-stat-label { display:block; font-size:0.7rem; color:var(--text-secondary); text-transform:uppercase; font-weight: 600; }

    /* AUTH.PY LEFT PANEL COMPATIBILITY */
    .split-left-panel {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
        border-radius: 20px; color: white; padding: 4rem 3rem; height: 100%; min-height: 500px;
        display: flex; flex-direction: column; justify-content: space-between;
    }
    .brand-title { font-size: 2.5rem; font-weight: 800; color: white !important; }
    .brand-subtitle { font-size: 1.25rem; opacity: 0.9; color: white !important; }
    .right-panel-header h2 { color: var(--text-primary); font-weight: 800; }
    </style>
    """


def inject_medical_saas_css():
    theme = st.session_state.get("theme", "dark")
    if theme == "dark":
        st.markdown(get_dark_css(), unsafe_allow_html=True)
    else:
        st.markdown(get_light_css(), unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    st.set_page_config(
        page_title="MediScan AI — Portal",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="auto"
    )

    # Session state init
    for key, default in [("logged_in", False), ("username", ""), ("role", ""), ("email", ""), ("theme", "dark")]:
        if key not in st.session_state:
            st.session_state[key] = default

    inject_medical_saas_css()

    if not st.session_state["logged_in"]:
        login()
    else:
        role = st.session_state["role"]
        if role == "User":
            user_dashboard(st.session_state["username"])
        elif role == "Doctor":
            doctor_dashboard()
        else:
            st.error("Invalid role. Please login again.")
            logout()


if __name__ == "__main__":
    main()