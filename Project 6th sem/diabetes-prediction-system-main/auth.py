"""
Authentication module for the Diabetes Prediction System
"""
import streamlit as st
import hashlib
import json
import os

# Default credentials (in production, these should be stored securely)
DEFAULT_USERS = {
    "admin": {
        "password": "admin123",  # In production, use hashed passwords
        "role": "admin"
    },
    "user": {
        "password": "user123",
        "role": "user"
    }
}

def hash_password(password):
    """Hash a password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    """Load users from file or use defaults"""
    users_file = "users.json"
    if os.path.exists(users_file):
        try:
            with open(users_file, 'r') as f:
                return json.load(f)
        except:
            return DEFAULT_USERS.copy()
    return DEFAULT_USERS.copy()

def save_users(users):
    """Save users to file"""
    users_file = "users.json"
    with open(users_file, 'w') as f:
        json.dump(users, f, indent=2)

def verify_login(username, password):
    """Verify user credentials"""
    users = load_users()
    if username in users:
        # For simplicity, using plain text comparison
        # In production, compare hashed passwords
        if users[username]["password"] == password:
            return True, users[username].get("role", "user")
    return False, None

def is_logged_in():
    """Check if user is logged in"""
    return "logged_in" in st.session_state and st.session_state.logged_in

def is_admin():
    """Check if current user is admin"""
    return is_logged_in() and st.session_state.get("role") == "admin"

def login(username, password):
    """Login user"""
    success, role = verify_login(username, password)
    if success:
        st.session_state.logged_in = True
        st.session_state.username = username
        st.session_state.role = role
        return True
    return False

def logout():
    """Logout user"""
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None
    if "predictions_history" in st.session_state:
        del st.session_state.predictions_history

def get_current_user():
    """Get current logged in user"""
    if is_logged_in():
        return st.session_state.get("username")
    return None

def get_user_role():
    """Get current user role"""
    if is_logged_in():
        return st.session_state.get("role", "user")
    return None

def signup(username, password, confirm_password):
    """Register a new user"""
    if password != confirm_password:
        return False, "Passwords do not match"
    
    if len(username) < 3:
        return False, "Username must be at least 3 characters long"
    
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    
    users = load_users()
    
    if username in users:
        return False, "Username already exists"
    
    # Add new user
    users[username] = {
        "password": password,  # In production, hash the password
        "role": "user"  # New users are regular users by default
    }
    
    save_users(users)
    return True, "Account created successfully!"

