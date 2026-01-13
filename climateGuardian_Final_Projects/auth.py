# ==========================================
# AUTHENTICATION MODULE
# Handles user login, signup, and session management
# ==========================================

import streamlit as st
import pandas as pd
import hashlib
import os
import time
from datetime import datetime

# Database file path
USER_DB_FILE = "users_database.csv"

def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    """Load users from CSV database"""
    if os.path.exists(USER_DB_FILE):
        df = pd.read_csv(USER_DB_FILE)
        # Ensure eco_score is numeric (avoid strings) and fill missing values
        if 'eco_score' in df.columns:
            df['eco_score'] = pd.to_numeric(df['eco_score'], errors='coerce').fillna(0).astype(int)
        else:
            df['eco_score'] = 0
        return df
    else:
        # Create new database with headers
        df = pd.DataFrame(columns=['username', 'email', 'password_hash', 'full_name', 'created_at', 'eco_score'])
        df.to_csv(USER_DB_FILE, index=False)
        return df

def save_users(df):
    """Save users to CSV database"""
    df.to_csv(USER_DB_FILE, index=False)

def user_exists(username, email):
    """Check if user already exists"""
    users_df = load_users()
    return ((users_df['username'] == username) | (users_df['email'] == email)).any()

def create_user(username, email, password, full_name):
    """Create a new user account"""
    users_df = load_users()
    
    new_user = pd.DataFrame({
        'username': [username],
        'email': [email],
        'password_hash': [hash_password(password)],
        'full_name': [full_name],
        'created_at': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        'eco_score': [0]
    })
    
    users_df = pd.concat([users_df, new_user], ignore_index=True)
    save_users(users_df)
    return True

def verify_user(username, password):
    """Verify user credentials"""
    users_df = load_users()
    user_row = users_df[users_df['username'] == username]
    
    if user_row.empty:
        return False
    
    stored_hash = user_row.iloc[0]['password_hash']
    return stored_hash == hash_password(password)

def get_user_info(username):
    """Get user information"""
    users_df = load_users()
    user_row = users_df[users_df['username'] == username]
    
    if not user_row.empty:
        return user_row.iloc[0].to_dict()
    return None

def update_user_score(username, new_score):
    """Update user's eco score"""
    users_df = load_users()
    users_df.loc[users_df['username'] == username, 'eco_score'] = new_score
    save_users(users_df)

def login_page():
    """Display login page"""
    st.markdown("""
        <style>
        .auth-container {
            max-width: 500px;
            margin: 50px auto;
            padding: 40px;
            background: white;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            border-left: 5px solid #4CAF50;
        }
        .auth-title {
            text-align: center;
            color: #2e7d32;
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        .auth-subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
        }
        .auth-icon {
            text-align: center;
            font-size: 5em;
            margin-bottom: 20px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        
        # Icon and Title
        st.markdown('<div class="auth-icon">🌿</div>', unsafe_allow_html=True)
        st.markdown('<h1 class="auth-title">Welcome Back!</h1>', unsafe_allow_html=True)
        st.markdown('<p class="auth-subtitle">Login to ClimateGuardian AI</p>', unsafe_allow_html=True)
        
        # Login Form
        with st.form("login_form"):
            username = st.text_input("👤 Username", placeholder="Enter your username")
            password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
            
            col_btn1, col_btn2 = st.columns(2)
            
            with col_btn1:
                login_button = st.form_submit_button("🚀 Login", use_container_width=True)
            
            with col_btn2:
                if st.form_submit_button("📝 Sign Up", use_container_width=True):
                    st.session_state['show_signup'] = True
                    st.rerun()
        
        if login_button:
            if not username or not password:
                st.error("⚠️ Please fill in all fields!")
            elif verify_user(username, password):
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.session_state['user_info'] = get_user_info(username)
                st.success(f"✅ Welcome back, {username}! 🌍")
                st.balloons()
                st.rerun()
            else:
                st.error("❌ Invalid username or password!")
        
        # Footer
        st.markdown("---")
        st.markdown("""
            <p style='text-align: center; color: #666; font-size: 0.9em;'>
                🌍 Join us in saving the planet! 🌱
            </p>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

def signup_page():
    """Display signup page"""
    st.markdown("""
        <style>
        .auth-container {
            max-width: 500px;
            margin: 50px auto;
            padding: 40px;
            background: white;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            border-left: 5px solid #4CAF50;
        }
        .auth-title {
            text-align: center;
            color: #2e7d32;
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        .auth-subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
        }
        .auth-icon {
            text-align: center;
            font-size: 5em;
            margin-bottom: 20px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        
        # Icon and Title
        st.markdown('<div class="auth-icon">🌱</div>', unsafe_allow_html=True)
        st.markdown('<h1 class="auth-title">Join Us!</h1>', unsafe_allow_html=True)
        st.markdown('<p class="auth-subtitle">Create your ClimateGuardian account</p>', unsafe_allow_html=True)
        
        # Signup Form
        with st.form("signup_form"):
            full_name = st.text_input("👨 Full Name", placeholder="Enter your full name")
            email = st.text_input("📧 Email", placeholder="your.email@example.com")
            username = st.text_input("👤 Username", placeholder="Choose a username")
            password = st.text_input("🔒 Password", type="password", placeholder="Create a strong password")
            confirm_password = st.text_input("🔒 Confirm Password", type="password", placeholder="Re-enter your password")
            
            # Terms checkbox
            terms = st.checkbox("I agree to help save the planet! 🌍")
            
            col_btn1, col_btn2 = st.columns(2)
            
            with col_btn1:
                signup_button = st.form_submit_button("🌟 Create Account", use_container_width=True)
            
            with col_btn2:
                if st.form_submit_button("← Back to Login", use_container_width=True):
                    st.session_state['show_signup'] = False
                    st.rerun()
        
        if signup_button:
            # Validation
            if not all([full_name, email, username, password, confirm_password]):
                st.error("⚠️ Please fill in all fields!")
            elif not terms:
                st.error("⚠️ Please accept the terms to continue!")
            elif password != confirm_password:
                st.error("❌ Passwords don't match!")
            elif len(password) < 6:
                st.error("⚠️ Password must be at least 6 characters!")
            elif user_exists(username, email):
                st.error("❌ Username or email already exists!")
            else:
                # Create account
                if create_user(username, email, password, full_name):
                    st.success("✅ Account created successfully! 🎉")
                    st.balloons()
                    st.info("👉 Please login with your credentials")
                    st.session_state['show_signup'] = False
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error("❌ Error creating account. Please try again.")
        
        # Footer
        st.markdown("---")
        st.markdown("""
            <p style='text-align: center; color: #666; font-size: 0.9em;'>
                Already have an account? Click "Back to Login" above! 🌿
            </p>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

def logout():
    """Logout user"""
    st.session_state['logged_in'] = False
    st.session_state['username'] = None
    st.session_state['user_info'] = None
    st.rerun()
