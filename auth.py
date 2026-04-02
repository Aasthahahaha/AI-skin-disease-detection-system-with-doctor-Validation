"""
Authentication Module

Handles user login, registration, logout, and password reset functionality.
Manages session state and user credentials stored in JSON format.
"""

import streamlit as st
import json
import os
from datetime import datetime

# File paths for data storage
USERS_FILE = "data/users.json"

def ensure_users_file():
    """
    Create users.json file if it doesn't exist.
    Initializes with default test accounts.
    """
    if not os.path.exists(USERS_FILE):
        # Create data directory if it doesn't exist
        os.makedirs("data", exist_ok=True)
        
        # Initialize with default users
        default_users = {
            "user1": {
                "password": "123",
                "role": "User",
                "email": "user1@example.com",
                "created_at": datetime.now().isoformat()
            },
            "doctor1": {
                "password": "123",
                "role": "Doctor",
                "email": "doctor1@example.com",
                "created_at": datetime.now().isoformat()
            },
            "user2": {
                "password": "123",
                "role": "User",
                "email": "user2@example.com",
                "created_at": datetime.now().isoformat()
            },
            "doctor2": {
                "password": "123",
                "role": "Doctor",
                "email": "doctor2@example.com",
                "created_at": datetime.now().isoformat()
            }
        }
        
        with open(USERS_FILE, "w") as f:
            json.dump(default_users, f, indent=4)

def load_users():
    """
    Load all users from the JSON file.
    
    Returns:
        dict: Dictionary containing user credentials and information
    """
    ensure_users_file()  # Ensure file exists
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        st.error("Error reading users file. Please contact administrator.")
        return {}

def save_users(users):
    """
    Save users dictionary to JSON file.
    
    Args:
        users (dict): Dictionary of users to save
    """
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def register_user(username, password, email, role="User"):
    """
    Register a new user.
    
    Args:
        username (str): Unique username
        password (str): User password
        email (str): User email address
        role (str): User role (User or Doctor)
    
    Returns:
        tuple: (success: bool, message: str)
    """
    users = load_users()
    
    # Check if username already exists
    if username in users:
        return False, "Username already exists. Please choose a different username."
    
    # Validate username
    if len(username) < 3:
        return False, "Username must be at least 3 characters long."
    
    # Validate password
    if len(password) < 4:
        return False, "Password must be at least 4 characters long."
    
    # Validate email format
    if "@" not in email or "." not in email:
        return False, "Please enter a valid email address."
    
    # Add new user
    users[username] = {
        "password": password,
        "role": role,
        "email": email,
        "created_at": datetime.now().isoformat()
    }
    
    save_users(users)
    return True, "Registration successful! You can now login."

def reset_password(username, new_password):
    """
    Reset user's password.
    
    Args:
        username (str): Username to reset password for
        new_password (str): New password
    
    Returns:
        tuple: (success: bool, message: str)
    """
    users = load_users()
    
    # Check if username exists
    if username not in users:
        return False, "Username not found."
    
    # Validate new password
    if len(new_password) < 4:
        return False, "Password must be at least 4 characters long."
    
    # Update password
    users[username]["password"] = new_password
    save_users(users)
    
    return True, "Password reset successfully! You can now login with your new password."

def login():
    """
    Display login form and handle authentication.
    
    This function creates a clean login interface with:
    - Username and password fields only
    - Automatic role detection from users.json
    - New user registration option
    - Password reset option
    """
    
    # Ensure users file exists
    ensure_users_file()
    
    st.title("🏥 Skin Disease Detection System")
    st.markdown("### AI-Powered Skin Disease Detection")
    st.markdown("---")
    
    # Create tabs for login, registration, and password reset
    tab1, tab2, tab3 = st.tabs(["🔐 Login", "📝 Register", "🔑 Forgot Password"])
    
    with tab1:
        st.subheader("Login to Your Account")
        
        # Login form - Only username and password (no role dropdown)
        with st.form("login_form"):
            username = st.text_input("Username", 
                                    placeholder="Enter your username")
            password = st.text_input("Password", 
                                   type="password",
                                   placeholder="Enter your password")
            
            submit_button = st.form_submit_button("Login")
            
            if submit_button:
                if not username or not password:
                    st.error("Please enter both username and password.")
                else:
                    users = load_users()
                    if username in users:
                        user_data = users[username]
                        if user_data["password"] == password:
                            # Successful login - get role from JSON
                            user_role = user_data.get("role", "User")
                            
                            # Store in session state
                            st.session_state["logged_in"] = True
                            st.session_state["username"] = username
                            st.session_state["role"] = user_role
                            st.session_state["email"] = user_data.get("email", "")
                            
                            st.success(f"Welcome back, {username}! ({user_role})")
                            st.rerun()
                        else:
                            st.error("Invalid password. Please try again.")
                    else:
                        st.error("Username not found. Please check your username or register.")
    
    with tab2:
        st.subheader("Create New Account")
        st.info("Register as a User to upload skin images and get AI predictions.")
        
        with st.form("register_form"):
            new_username = st.text_input("Choose Username", 
                                        placeholder="At least 3 characters")
            new_email = st.text_input("Email Address", 
                                      placeholder="your@email.com")
            new_password = st.text_input("Choose Password", 
                                        type="password",
                                        placeholder="At least 4 characters")
            confirm_password = st.text_input("Confirm Password", 
                                            type="password",
                                            placeholder="Confirm your password")
            new_role = st.selectbox("Register as", ["User", "Doctor"],
                                   help="Doctors can review and approve cases")
            
            register_submit = st.form_submit_button("Register")
            
            if register_submit:
                if not new_username or not new_password or not new_email:
                    st.error("Please fill in all fields.")
                elif new_password != confirm_password:
                    st.error("Passwords do not match.")
                else:
                    success, message = register_user(new_username, new_password, new_email, new_role)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
    
    with tab3:
        st.subheader("Forgot Password")
        st.warning("Enter your username and new password to reset it.")
        st.info("Note: For security, you must know your username. Contact admin if you don't remember it.")
        
        with st.form("reset_password_form"):
            reset_username = st.text_input("Username", 
                                          placeholder="Enter your username")
            reset_email = st.text_input("Registered Email", 
                                       placeholder="Enter your registered email")
            new_password = st.text_input("New Password", 
                                         type="password",
                                         placeholder="At least 4 characters")
            confirm_new_password = st.text_input("Confirm New Password", 
                                                 type="password",
                                                 placeholder="Confirm new password")
            
            reset_submit = st.form_submit_button("Reset Password")
            
            if reset_submit:
                if not reset_username or not reset_email or not new_password:
                    st.error("Please fill in all fields.")
                else:
                    users = load_users()
                    
                    # Verify username exists
                    if reset_username not in users:
                        st.error("Username not found. Please check and try again.")
                    # Verify email matches
                    elif users[reset_username].get("email", "") != reset_email:
                        st.error("Email doesn't match our records. Please try again.")
                    # Verify passwords match
                    elif new_password != confirm_new_password:
                        st.error("New passwords do not match.")
                    else:
                        success, message = reset_password(reset_username, new_password)
                        if success:
                            st.success(message)
                            st.balloons()
                        else:
                            st.error(message)
    
    
def logout():
    """
    Log out the current user by clearing session state.
    """
    # Clear all session state variables
    st.session_state["logged_in"] = False
    st.session_state["username"] = ""
    st.session_state["role"] = ""
    st.session_state["email"] = ""
    
    st.success("You have been logged out successfully.")
    st.rerun()

def get_current_user():
    """
    Get information about the currently logged-in user.
    
    Returns:
        dict or None: User data if logged in, None otherwise
    """
    if st.session_state.get("logged_in", False):
        username = st.session_state.get("username", "")
        users = load_users()
        if username in users:
            return users[username]
    return None

