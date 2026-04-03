"""
Authentication Module

Handles user login, registration, logout, and password reset.
Seeds extra accounts on first run.
"""

import streamlit as st
import json
import os
from datetime import datetime

USERS_FILE = "data/users.json"


def ensure_users_file():
    if not os.path.exists(USERS_FILE):
        os.makedirs("data", exist_ok=True)
        default_users = {
            "user1": {"password": "123", "role": "User", "email": "user1@example.com", "created_at": datetime.now().isoformat()},
            "user2": {"password": "123", "role": "User", "email": "user2@example.com", "created_at": datetime.now().isoformat()},
            "doctor1": {"password": "123", "role": "Doctor", "email": "doctor1@mediscan.ai", "created_at": datetime.now().isoformat()},
            "doctor3": {"password": "123", "role": "Doctor", "email": "doctor3@mediscan.ai", "created_at": datetime.now().isoformat()},
        }
        with open(USERS_FILE, "w") as f:
            json.dump(default_users, f, indent=4)


def load_users():
    ensure_users_file()
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        st.error("Error reading users file.")
        return {}


def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)


def register_user(username, password, email, role="User", display_name="", specialization="", city="", area="", hospital="", bio=""):
    users = load_users()
    if username in users:
        return False, "Username already exists."
    if len(username) < 3:
        return False, "Username too short (min 3)."
    if len(password) < 4:
        return False, "Password too short (min 4)."
    if "@" not in email or "." not in email:
        return False, "Invalid email address."

    users[username] = {
        "password": password,
        "role": role,
        "email": email,
        "created_at": datetime.now().isoformat()
    }
    save_users(users)

    if role == "Doctor":
        from database import register_doctor_profile
        register_doctor_profile(username, display_name=display_name or f"Dr. {username.title()}", specialization=specialization, city=city, area=area, hospital=hospital, bio=bio)

    return True, "Registration successful! You can now log in."


def toggle_theme():
    st.session_state["theme"] = "light" if st.session_state.get("theme", "dark") == "dark" else "dark"

def login():
    ensure_users_file()

    col_empty, col_toggle = st.columns([8, 1])
    with col_toggle:
        theme_label = "☀️ Light Mode" if st.session_state.get("theme", "dark") == "dark" else "🌙 Dark Mode"
        st.button(theme_label, on_click=toggle_theme, key="login_theme")

    # CSS specifically for the split view login page
    st.markdown("""
    <style>
    .split-left-panel {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
        border-radius: 20px;
        color: white;
        padding: 4rem 3rem;
        height: 100%;
        min-height: 500px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 10px 40px rgba(0,74,153,0.3);
    }
    .brand-title { font-size: 2.5rem; font-weight: 800; letter-spacing: -0.03em; margin-bottom: 2rem; color: white !important; }
    .brand-subtitle { font-size: 1.25rem; font-weight: 300; opacity: 0.9; line-height: 1.5; color: white !important; }
    .trust-badges { margin-top: 4rem; opacity: 0.7; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em; }
    .right-panel-header { margin-bottom: 2rem; }
    .right-panel-header h2 { font-size: 1.8rem; color: var(--text-primary); font-weight: 800; }
    .right-panel-header p { color: var(--text-secondary); margin-top: 0.5rem; }
    </style>
    """, unsafe_allow_html=True)

    # Empty columns for outer margin, making it look centered
    st.markdown("<br><br>", unsafe_allow_html=True)
    _, col_main, _ = st.columns([1, 8, 1])

    with col_main:
        # The main Split Card
        col_left, col_right = st.columns([1, 1], gap="large")

        with col_left:
            st.markdown("""
            <div class="split-left-panel">
                <div>
                    <div class="brand-title">🏥 MediScan AI</div>
                    <div class="brand-subtitle">
                        Empowering healthcare professionals and patients with enterprise-grade clinical AI diagnostics.
                    </div>
                </div>
                <div class="trust-badges">
                    Trusted securely by 50+ Top Tier Hospitals
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_right:
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Use tabs for Login vs Register, similar to standard flow but styled
            tab1, tab2 = st.tabs(["🔒 Secure Log In", "Create an Account"])

            with tab1:
                st.markdown("""
                <div class="right-panel-header">
                    <h2>Welcome Back</h2>
                    <p>Please enter your details to access your portal.</p>
                </div>
                """, unsafe_allow_html=True)

                role_selection = st.radio("Log in as:", ["Patient", "Doctor"], horizontal=True, label_visibility="collapsed")
                
                with st.form("login_form"):
                    username = st.text_input("Username", placeholder="e.g. user1 or doctor1")
                    password = st.text_input("Password", type="password", placeholder="••••••••")
                    submit = st.form_submit_button("Log In →")

                    if submit:
                        if not username or not password:
                            st.error("Please fill in all fields.")
                        else:
                            users = load_users()
                            if username in users and users[username]["password"] == password:
                                user_role = users[username].get("role", "User")
                                expected_role = "User" if role_selection == "Patient" else "Doctor"
                                
                                if user_role != expected_role:
                                    st.warning(f"This account is registered as a {user_role}, not a {expected_role}.")
                                else:
                                    st.session_state["logged_in"] = True
                                    st.session_state["username"]  = username
                                    st.session_state["role"]      = user_role
                                    st.session_state["email"]     = users[username].get("email", "")
                                    st.rerun()
                            else:
                                st.error("Incorrect username or password.")
                
                st.markdown("""
                <div style="margin-top:1.5rem;font-size:0.85rem;color:var(--text-muted);text-align:center;">
                    <p><strong>Demo Accounts:</strong> <code>user1/123</code> (Patient) | <code>doctor1/123</code> (Doctor)</p>
                </div>
                """, unsafe_allow_html=True)

            with tab2:
                st.markdown("""
                <div class="right-panel-header">
                    <h2>Register Account</h2>
                    <p>Join the MediScan platform.</p>
                </div>
                """, unsafe_allow_html=True)
                
                with st.form("register_form"):
                    reg_role = st.radio("I am a:", ["Patient", "Doctor"], horizontal=True)
                    new_user = st.text_input("Choose Username")
                    new_email= st.text_input("Email Address")
                    new_pw   = st.text_input("Choose Password", type="password")
                    
                    d_name = d_spec = d_city = d_hosp = ""
                    if reg_role == "Doctor":
                        st.markdown("**Doctor Details**")
                        d_name = st.text_input("Full Name with Title")
                        d_spec = st.text_input("Specialization")
                        d_city = st.text_input("Practice City")
                        d_hosp = st.text_input("Primary Hospital/Clinic")

                    btn = st.form_submit_button("Register Account →")
                    if btn:
                        mapped_role = "User" if reg_role == "Patient" else "Doctor"
                        success, message = register_user(
                            new_user, new_pw, new_email, mapped_role,
                            display_name=d_name, specialization=d_spec, city=d_city, hospital=d_hosp
                        )
                        if success: st.success(message)
                        else: st.error(message)

def logout():
    st.session_state["logged_in"] = False
    st.session_state["username"]  = ""
    st.session_state["role"]      = ""
    st.session_state["email"]     = ""
    st.rerun()

def get_current_user():
    if st.session_state.get("logged_in", False):
        users = load_users()
        return users.get(st.session_state["username"])
    return None
