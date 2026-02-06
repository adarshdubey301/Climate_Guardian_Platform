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
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
import io
import qrcode
import base64

# Database file path
USER_DB_FILE = "users_database.csv"
ACTIVITY_DB_FILE = "user_activities.csv"
CERTIFICATES_DB_FILE = "certificates_database.csv"

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

def log_activity(username, action, points):
    """Log user activity to persistent CSV storage"""
    if not os.path.exists(ACTIVITY_DB_FILE):
        df = pd.DataFrame(columns=['timestamp', 'username', 'action', 'points'])
        df.to_csv(ACTIVITY_DB_FILE, index=False)
    
    new_row = pd.DataFrame({
        'timestamp': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        'username': [username],
        'action': [action],
        'points': [points]
    })
    # Append to CSV
    new_row.to_csv(ACTIVITY_DB_FILE, mode='a', header=False, index=False)

def get_all_activities():
    """Load all activities for global dashboard"""
    if os.path.exists(ACTIVITY_DB_FILE):
        return pd.read_csv(ACTIVITY_DB_FILE)
    return pd.DataFrame(columns=['timestamp', 'username', 'action', 'points'])

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
                user_info = get_user_info(username)
                st.session_state['user_info'] = user_info
                
                # Load persistent eco_score from database
                if user_info and 'eco_score' in user_info:
                    st.session_state['eco_score'] = int(user_info['eco_score'])
                
                # Set query params for persistence on refresh
                st.query_params["user"] = username
                st.query_params["logged_in"] = "true"
                
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

# ==========================================
# LEADERBOARD FUNCTIONS
# ==========================================

def get_leaderboard_data():
    """Get sorted leaderboard data with rankings"""
    try:
        df = load_users()
        # Sort by eco_score in descending order
        df_sorted = df.sort_values('eco_score', ascending=False).reset_index(drop=True)
        # Add rank column
        df_sorted['rank'] = df_sorted.index + 1
        return df_sorted
    except FileNotFoundError:
        return pd.DataFrame(columns=['rank', 'username', 'full_name', 'eco_score'])
    except Exception as e:
        print(f"Error loading leaderboard: {e}")
        return pd.DataFrame(columns=['rank', 'username', 'full_name', 'eco_score'])

def get_user_rank(username):
    """Get user's current global rank"""
    leaderboard = get_leaderboard_data()
    if not leaderboard.empty:
        user_row = leaderboard[leaderboard['username'] == username]
        if not user_row.empty:
            return int(user_row.iloc[0]['rank'])
    return None

def get_top_users(n=10):
    """Get top N users by eco score"""
    leaderboard = get_leaderboard_data()
    return leaderboard.head(n)

def get_user_percentile(username):
    """Get user's percentile ranking"""
    leaderboard = get_leaderboard_data()
    total_users = len(leaderboard)
    
    if total_users == 0:
        return 0
    
    user_rank = get_user_rank(username)
    if user_rank:
        percentile = ((total_users - user_rank + 1) / total_users) * 100
        return round(percentile, 1)
    return 0

# ==========================================
# CERTIFICATE FUNCTIONS
# ==========================================

def load_certificates():
    """Load certificates database"""
    if os.path.exists(CERTIFICATES_DB_FILE):
        return pd.read_csv(CERTIFICATES_DB_FILE)
    else:
        df = pd.DataFrame(columns=['username', 'eco_score', 'rank', 'issued_date', 'certificate_id', 'qr_code_id'])
        df.to_csv(CERTIFICATES_DB_FILE, index=False)
        return df

def save_certificates(df):
    """Save certificates to database"""
    df.to_csv(CERTIFICATES_DB_FILE, index=False)

def generate_certificate_pdf(username, eco_score, rank, total_users):
    """Generate certificate PDF with ReportLab"""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape(letter))
    w, h = landscape(letter)

    # Get full name from database
    user_info = get_user_info(username)
    full_name = user_info.get('full_name', username) if user_info else username

    # 🌿 Background
    c.setFillColor(colors.HexColor("#e9f7ef"))
    c.rect(0, 0, w, h, fill=1, stroke=0)

    # 🎀 Curved ribbon (top-left)
    c.setFillColor(colors.HexColor("#2e7d32"))
    path = c.beginPath()
    path.moveTo(0, h)
    path.curveTo(300, h-30, 400, h-120, 450, h-180)
    path.lineTo(450, h)
    path.close()
    c.drawPath(path, fill=1, stroke=0)

    # 🌱 Abstract leaf shapes (right side)
    c.setFillColor(colors.HexColor("#43a047"))
    leaf = c.beginPath()
    leaf.moveTo(w-200, 100)
    leaf.curveTo(w-50, 250, w-50, 450, w-220, 580)
    leaf.curveTo(w-160, 420, w-180, 260, w-200, 100)
    leaf.close()
    c.drawPath(leaf, fill=1, stroke=0)

    c.setFillColor(colors.HexColor("#66bb6a"))
    leaf2 = c.beginPath()
    leaf2.moveTo(w-260, 120)
    leaf2.curveTo(w-140, 280, w-160, 450, w-300, 600)
    leaf2.close()
    c.drawPath(leaf2, fill=1, stroke=0)

    # 🏅 Golden Award Seal
    cx, cy = w/2 + 220, h/2 + 50
    c.setFillColor(colors.HexColor("#f9a825"))
    c.circle(cx, cy, 45, fill=1, stroke=0)

    c.setFillColor(colors.HexColor("#ffd54f"))
    c.circle(cx, cy, 38, fill=1, stroke=0)

    c.setFillColor(colors.darkgreen)
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(cx, cy+5, "BEST")
    c.drawCentredString(cx, cy-10, "AWARD")

    # 📜 Certificate Title
    c.setFillColor(colors.HexColor("#1b5e20"))
    c.setFont("Helvetica-Bold", 36)
    c.drawCentredString(w/2 - 100, h - 1.7*inch, "CERTIFICATE")

    c.setFont("Helvetica", 16)
    c.drawCentredString(w/2 - 100, h - 2.3*inch, "OF APPRECIATION")

    # 👤 Name (Full Name instead of username)
    c.setFont("Helvetica-Bold", 30)
    c.drawCentredString(w/2 - 100, h - 3.5*inch, full_name)

    # 📝 Content
    c.setFont("Helvetica", 14)
    c.drawCentredString(
        w/2 - 100,
        h - 4.2*inch,
        "For outstanding contribution towards climate sustainability"
    )

    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(
        w/2 - 100,
        h - 4.9*inch,
        f"ECO SCORE: {eco_score}"
    )

    c.setFont("Helvetica", 13)
    c.drawCentredString(
        w/2 - 100,
        h - 5.4*inch,
        f"Rank #{rank} among {total_users} Climate Guardians"
    )

    # ✍ Signatures (moved text above signature line)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(2.75*inch, 1.5*inch, "Director")
    c.line(1.5*inch, 1.2*inch, 4*inch, 1.2*inch)

    c.drawCentredString(w-2.75*inch, 1.5*inch, "ClimateGuardian AI")
    c.line(w-4*inch, 1.2*inch, w-1.5*inch, 1.2*inch)

    # 📅 Date
    c.setFont("Helvetica-Oblique", 11)
    c.drawCentredString(
        w/2,
        0.7*inch,
        f"Issued on {datetime.now().strftime('%d %B %Y')}"
    )

    c.save()
    buffer.seek(0)
    return buffer

def generate_qr_code(certificate_id, username):
    """Generate QR code for certificate download"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr_data = f"certificate_{certificate_id}_{username}"
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    return img

def issue_certificate(username):
    """Issue certificate to user (only if eco_score >= 500)"""
    users_df = load_users()
    user_row = users_df[users_df['username'] == username]
    
    if user_row.empty:
        return False, "User not found"
    
    eco_score = int(user_row.iloc[0]['eco_score'])
    
    if eco_score < 500:
        return False, f"User must have at least 500 eco-points. Current score: {eco_score}"
    
    # Check if certificate already issued
    certs_df = load_certificates()
    if not certs_df.empty and (certs_df['username'] == username).any():
        return False, "Certificate already issued to this user"
    
    # Generate certificate ID
    certificate_id = f"CERT_{username}_{int(datetime.now().timestamp())}"
    leaderboard = get_leaderboard_data()
    rank = get_user_rank(username) or len(leaderboard)
    total_users = len(leaderboard)
    
    # Create certificate record
    new_cert = pd.DataFrame({
        'username': [username],
        'eco_score': [eco_score],
        'rank': [rank],
        'issued_date': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        'certificate_id': [certificate_id],
        'qr_code_id': [f"QR_{certificate_id}"]
    })
    
    certs_df = pd.concat([certs_df, new_cert], ignore_index=True)
    save_certificates(certs_df)
    
    # Log activity
    log_activity(username, "Certificate Issued", 50)
    
    return True, certificate_id

def check_certificate_eligibility(username):
    """Check if user is eligible for certificate"""
    users_df = load_users()
    user_row = users_df[users_df['username'] == username]
    
    if user_row.empty:
        return False, 0
    
    eco_score = int(user_row.iloc[0]['eco_score'])
    return eco_score >= 500, eco_score

def get_certificate_info(username):
    """Get certificate information for user"""
    certs_df = load_certificates()
    cert_row = certs_df[certs_df['username'] == username]
    
    if cert_row.empty:
        return None
    
    return cert_row.iloc[0].to_dict()

def get_all_certificates():
    """Get all issued certificates"""
    return load_certificates()

def logout():
    """Logout user"""
    st.session_state['logged_in'] = False
    st.session_state['username'] = None
    st.session_state['user_info'] = None
    # Reset eco score on logout
    if 'eco_score' in st.session_state:
        st.session_state['eco_score'] = 0
    # Clear persistence
    st.query_params.clear()
    st.rerun()
