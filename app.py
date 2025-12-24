"""
URAMix - Waste to Wealth Platform
Complete Hackathon-Ready Streamlit Application
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import qrcode
from io import BytesIO
import base64
from datetime import datetime
import json

# ============================================
# PAGE CONFIGURATION
# ============================================
st.set_page_config(
    page_title="URAMix - Waste to Wealth",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CUSTOM CSS STYLING
# ============================================
st.markdown("""
<style>
    /* Main Background */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8f5e9 100%);
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #43a047 0%, #66bb6a 100%);
        color: white;
        border-radius: 25px;
        padding: 12px 30px;
        border: none;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(67, 160, 71, 0.3);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(67, 160, 71, 0.4);
    }
    
    /* Hero Section */
    .hero-title {
        font-size: 3.5em;
        font-weight: 800;
        background: linear-gradient(135deg, #2e7d32 0%, #66bb6a 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 10px;
    }
    
    .hero-subtitle {
        font-size: 1.4em;
        color: #558b2f;
        text-align: center;
        margin-bottom: 40px;
        font-weight: 500;
    }
    
    /* Problem Cards */
    .problem-card {
        background: white;
        padding: 25px;
        border-radius: 15px;
        border-left: 6px solid #43a047;
        margin: 15px 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        animation: slideIn 0.6s ease-out;
        transition: transform 0.3s ease;
    }
    
    .problem-card:hover {
        transform: translateX(10px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.12);
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #43a047 0%, #66bb6a 100%);
        padding: 25px;
        border-radius: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 6px 20px rgba(67, 160, 71, 0.3);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: scale(1.05);
    }
    
    .metric-value {
        font-size: 2.5em;
        font-weight: 700;
        margin: 10px 0;
    }
    
    .metric-label {
        font-size: 1.1em;
        opacity: 0.95;
        font-weight: 500;
    }
    
    /* Eco Quote Box */
    .eco-quote {
        background: linear-gradient(135deg, #1b5e20 0%, #388e3c 100%);
        padding: 35px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin: 30px 0;
        box-shadow: 0 8px 24px rgba(27, 94, 32, 0.3);
    }
    
    /* Dustbin Container */
    .dustbin-container {
        background: white;
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
        margin: 20px 0;
    }
    
    .dustbin-visual {
        background: #f5f5f5;
        border-radius: 15px;
        height: 350px;
        position: relative;
        overflow: hidden;
        border: 4px solid #66bb6a;
        box-shadow: inset 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .dustbin-fill {
        position: absolute;
        bottom: 0;
        width: 100%;
        transition: height 0.8s cubic-bezier(0.4, 0, 0.2, 1);
        border-radius: 0 0 11px 11px;
    }
    
    /* Status Badges */
    .status-pending {
        background: #fff3cd;
        color: #856404;
        padding: 10px 20px;
        border-radius: 20px;
        border: 2px solid #ffc107;
        display: inline-block;
        margin: 5px;
        font-weight: 600;
    }
    
    .status-verified {
        background: #d4edda;
        color: #155724;
        padding: 10px 20px;
        border-radius: 20px;
        border: 2px solid #28a745;
        display: inline-block;
        margin: 5px;
        font-weight: 600;
    }
    
    /* Mission Badges */
    .mission-badge {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        padding: 15px 25px;
        border-radius: 30px;
        display: inline-block;
        margin: 8px;
        font-weight: 600;
        color: #2e7d32;
        border: 2px solid #81c784;
        box-shadow: 0 3px 10px rgba(0,0,0,0.08);
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# SESSION STATE INITIALIZATION
# ============================================
def init_session_state():
    """Initialize all session state variables"""
    
    # User Database
    if 'users' not in st.session_state:
        st.session_state.users = {}
    
    # Authentication
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'current_user' not in st.session_state:
        st.session_state.current_user = None
    if 'is_admin' not in st.session_state:
        st.session_state.is_admin = False
    
    # Waste Submissions (Global)
    if 'waste_submissions' not in st.session_state:
        st.session_state.waste_submissions = []
    
    # QR Codes Database
    if 'qr_codes' not in st.session_state:
        st.session_state.qr_codes = {}
    
    # System Metrics
    if 'total_credits_issued' not in st.session_state:
        st.session_state.total_credits_issued = 0
    if 'daily_waste' not in st.session_state:
        st.session_state.daily_waste = {}
    
    # Manure Management
    if 'manure_stock' not in st.session_state:
        st.session_state.manure_stock = 500.0
    if 'manure_price' not in st.session_state:
        st.session_state.manure_price = 25
    if 'manure_sales' not in st.session_state:
        st.session_state.manure_sales = []

# ============================================
# AUTHENTICATION FUNCTIONS
# ============================================
def create_new_user(email, password):
    """Create a new user account"""
    st.session_state.users[email] = {
        'password': password,
        'credits': 0,
        'organic_bin': 0,
        'inorganic_bin': 0,
        'waste_history': [],
        'manure_purchased': 0.0,
        'referral_used': False,
        'co2_reduced': 0.0,
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

def signup_user(email, password):
    """User signup"""
    if not email or not password:
        return False, "❌ Please fill all fields!"
    
    if email.lower() == "admin":
        return False, "❌ Cannot use 'admin' as email!"
    
    if email in st.session_state.users:
        return False, "❌ Email already registered!"
    
    if len(password) < 6:
        return False, "❌ Password must be at least 6 characters!"
    
    create_new_user(email, password)
    return True, "✅ Account created successfully! Please login."

def login_user(email, password):
    """User/Admin login"""
    if not email or not password:
        return False, "❌ Please fill all fields!"
    
    # Admin Login
    if email.lower() == "admin" and password == "12345":
        st.session_state.logged_in = True
        st.session_state.is_admin = True
        st.session_state.current_user = "admin"
        return True, "✅ Admin login successful!"
    
    # User Login
    if email in st.session_state.users:
        if st.session_state.users[email]['password'] == password:
            st.session_state.logged_in = True
            st.session_state.is_admin = False
            st.session_state.current_user = email
            return True, "✅ Login successful!"
        return False, "❌ Incorrect password!"
    
    return False, "❌ User not found! Please signup."

def logout():
    """Logout current user"""
    st.session_state.logged_in = False
    st.session_state.is_admin = False
    st.session_state.current_user = None

# ============================================
# QR CODE GENERATION
# ============================================
def generate_qr_code(data):
    """Generate QR code and return base64 string"""
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return img_str
    except Exception as e:
        st.error(f"QR Error: {str(e)}")
        return None

# ============================================
# CREDIT CALCULATION
# ============================================
def calculate_credits(waste_type, quantity):
    """Calculate credits and CO2 reduction"""
    if waste_type == "Organic Waste":
        base_credits = 60
        co2_reduction = 0.8
    else:
        base_credits = 35
        co2_reduction = 0.4
    
    quantity_bonus = min(int(quantity * 1.5), 15)
    total_credits = base_credits + quantity_bonus
    
    return total_credits, co2_reduction

def update_manure_stock(organic_quantity):
    """Convert organic waste to manure"""
    manure_generated = organic_quantity * 0.3
    st.session_state.manure_stock += manure_generated
    return manure_generated

# ============================================
# AUTHENTICATION PAGE
# ============================================
def auth_page():
    """Login and Signup Page"""
    st.markdown('<p class="hero-title">♻️ URAMix</p>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">Waste to Wealth | Clean India Mission</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 20px; background: white; border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);'>
            <h3 style='color: #2e7d32;'>🌍 Our Mission</h3>
            <p style='color: #558b2f; font-size: 1.1em;'>
                Make India Clean • Reduce Landfills<br>
                Convert Waste to Value • Reward Citizens<br>
                Affordable Natural Manure for Farmers
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col_left, col_center, col_right = st.columns([1, 2, 1])
    
    with col_center:
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Signup"])
        
        # LOGIN TAB
        with tab1:
            st.markdown("### Login to Your Account")
            
            login_email = st.text_input("Email / Username", key="login_email", placeholder="your.email@example.com")
            login_password = st.text_input("Password", type="password", key="login_pass", placeholder="••••••••")
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                if st.button("Login", use_container_width=True, key="btn_login"):
                    success, message = login_user(login_email, login_password)
                    if success:
                        st.success(message)
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(message)
            
            with col_b:
                if st.button("🔍 Google (Demo)", use_container_width=True, key="btn_google"):
                    st.info("🔄 Google Sign-In - Demo Mode")
        
        # SIGNUP TAB
        with tab2:
            st.markdown("### Create New Account")
            
            signup_email = st.text_input("Email Address", key="signup_email", placeholder="your.email@example.com")
            signup_password = st.text_input("Create Password", type="password", key="signup_pass", placeholder="Min. 6 characters")
            signup_confirm = st.text_input("Confirm Password", type="password", key="confirm_pass", placeholder="Re-enter password")
            
            if st.button("Create Account", use_container_width=True, key="btn_signup"):
                if signup_password != signup_confirm:
                    st.error("❌ Passwords don't match!")
                else:
                    success, message = signup_user(signup_email, signup_password)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)

# ============================================
# HOME PAGE
# ============================================
def home_page():
    """Home Page with Problem Statements"""
    st.markdown('<p class="hero-title">🌍 Welcome to URAMix</p>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">Transform Waste into Wealth | Build a Cleaner India</p>', unsafe_allow_html=True)
    
    # Hero Images
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='text-align: center; padding: 20px; background: white; border-radius: 20px; box-shadow: 0 6px 20px rgba(0,0,0,0.1);'>
            <div style='background: #e8f5e9; padding: 60px; border-radius: 15px; margin-bottom: 15px;'>
                <div style='font-size: 80px;'>🗑️</div>
            </div>
            <h3 style='color: #2e7d32; margin: 15px 0;'>Smart Waste Collection</h3>
            <p style='color: #666;'>Segregate & earn credits</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 20px; background: white; border-radius: 20px; box-shadow: 0 6px 20px rgba(0,0,0,0.1);'>
            <div style='background: #fff3e0; padding: 60px; border-radius: 15px; margin-bottom: 15px;'>
                <div style='font-size: 80px;'>🌿</div>
            </div>
            <h3 style='color: #f57c00; margin: 15px 0;'>Natural Manure</h3>
            <p style='color: #666;'>Affordable & eco-friendly</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Eco Quote
    user = st.session_state.users.get(st.session_state.current_user, {})
    co2_reduced = user.get('co2_reduced', 0)
    credits = user.get('credits', 0)
    
    st.markdown(f"""
    <div class='eco-quote'>
        <h2 style='margin: 0 0 15px 0;'>🌱 Your Impact Today</h2>
        <h1 style='font-size: 3em; margin: 15px 0;'>{co2_reduced:.1f}%</h1>
        <p style='font-size: 1.3em; margin: 0;'>
            You helped reduce landfill emissions!<br>
            <strong>Your eco credits: {credits} points! 🎉</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Problem Statements
    st.markdown("---")
    st.markdown("## 🚨 Real Problems We're Solving")
    
    problems = [
        {
            "icon": "🏙️",
            "title": "India's Landfill Crisis",
            "description": "Landfills contribute to 20-25% of urban methane emissions in India, causing severe environmental damage and health hazards.",
            "color": "#e53935"
        },
        {
            "icon": "🗑️",
            "title": "Overflowing Dustbins",
            "description": "People dump waste irresponsibly because dustbins get full quickly and they cannot wait a full day for collection.",
            "color": "#fb8c00"
        },
        {
            "icon": "⏰",
            "title": "Irregular Garbage Collection",
            "description": "Inconsistent collection schedules lead to waste piling up in streets, creating hygiene issues and pollution.",
            "color": "#fdd835"
        },
        {
            "icon": "💰",
            "title": "Expensive Natural Manure",
            "description": "Natural farming manure is costly and unaffordable for common farmers, forcing them to use chemical fertilizers.",
            "color": "#43a047"
        },
        {
            "icon": "🌾",
            "title": "Farmer vs. Big Corporations",
            "description": "Small farmers cannot compete with expensive manure producers. URAMix provides affordable community-generated manure.",
            "color": "#1e88e5"
        }
    ]
    
    for problem in problems:
        st.markdown(f"""
        <div class='problem-card'>
            <h3 style='color: {problem["color"]}; font-size: 1.8em; margin-bottom: 10px;'>
                {problem["icon"]} {problem["title"]}
            </h3>
            <p style='font-size: 1.1em; color: #555; line-height: 1.6;'>
                {problem["description"]}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Mission
    st.markdown("---")
    st.markdown("### ✨ Our Mission")
    
    st.markdown("""
    <div style='text-align: center; padding: 30px;'>
        <span class='mission-badge'>🇮🇳 Make India Clean</span>
        <span class='mission-badge'>♻️ Reduce Landfills</span>
        <span class='mission-badge'>🔄 Convert Waste to Value</span>
        <span class='mission-badge'>💳 Reward Responsible Citizens</span>
        <span class='mission-badge'>🌿 Affordable Natural Manure</span>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# USER DASHBOARD
# ============================================
def user_dashboard():
    """User Dashboard Page"""
    user = st.session_state.users.get(st.session_state.current_user)
    
    if not user:
        st.error("❌ User data not found!")
        return
    
    st.title("📊 Your Dashboard")
    st.markdown(f"Welcome back, **{st.session_state.current_user}** 👋")
    
    # Top Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-value'>{user['credits']}</div>
            <div class='metric-label'>💳 Credits</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        rupees = user['credits'] / 20.0
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-value'>₹{rupees:.2f}</div>
            <div class='metric-label'>💰 Wallet</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-value'>{len(user['waste_history'])}</div>
            <div class='metric-label'>🗑️ Submissions</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-value'>{user['co2_reduced']:.1f}%</div>
            <div class='metric-label'>🌍 CO₂ Reduced</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Virtual Dustbins
    st.markdown("### 🗑️ Virtual Dustbin Status")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown("#### 🟢 Organic Waste Bin")
        organic_fill = user['organic_bin']
        
        st.markdown(f"""
        <div class='dustbin-container'>
            <div class='dustbin-visual'>
                <div class='dustbin-fill' style='height: {organic_fill}%; background: linear-gradient(to top, #43a047 0%, #81c784 100%);'></div>
            </div>
            <div style='text-align: center; margin-top: 20px;'>
                <h2 style='color: #43a047; margin: 10px 0;'>{organic_fill}%</h2>
                <p style='color: #666; font-size: 1.1em;'>Fill Level</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if organic_fill >= 80:
            st.error("🚨 Bin almost full!")
        elif organic_fill >= 50:
            st.warning("⚠️ Bin half full.")
        else:
            st.success("✅ Space available.")
    
    with col_right:
        st.markdown("#### 🔵 Inorganic Waste Bin")
        inorganic_fill = user['inorganic_bin']
        
        st.markdown(f"""
        <div class='dustbin-container'>
            <div class='dustbin-visual'>
                <div class='dustbin-fill' style='height: {inorganic_fill}%; background: linear-gradient(to top, #1976d2 0%, #64b5f6 100%);'></div>
            </div>
            <div style='text-align: center; margin-top: 20px;'>
                <h2 style='color: #1976d2; margin: 10px 0;'>{inorganic_fill}%</h2>
                <p style='color: #666; font-size: 1.1em;'>Fill Level</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if inorganic_fill >= 80:
            st.error("🚨 Bin almost full!")
        elif inorganic_fill >= 50:
            st.warning("⚠️ Bin half full.")
        else:
            st.success("✅ Space available.")
    
    st.markdown("---")
    
    # Waste Submission
    st.markdown("### ♻️ Submit Waste")
    
    col_a, col_b = st.columns([2, 1])
    
    with col_a:
        waste_type = st.selectbox(
            "Select Waste Type",
            ["Organic Waste", "Inorganic Waste"],
            key="waste_type_select"
        )
        
        st.info("""
        **💡 Credit Information:**
        - **Organic Waste:** 60+ credits
        - **Inorganic Waste:** 35+ credits
        - **Referral Bonus:** +20 credits (one-time)
        """)
    
    with col_b:
        st.markdown("#### 🎁 Referral")
        if not user['referral_used']:
            ref_code = st.text_input("Referral Code", key="ref_code", placeholder="Enter code")
            if st.button("Apply", use_container_width=True, key="btn_ref"):
                if ref_code:
                    user['credits'] += 20
                    user['referral_used'] = True
                    st.success("🎉 +20 credits!")
                    st.rerun()
        else:
            st.success("✅ Applied!")
    
    if st.button("📤 Submit Waste Request", use_container_width=True, type="primary", key="btn_submit_waste"):
        submission_id = f"{st.session_state.current_user}_{waste_type.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        submission = {
            'id': submission_id,
            'user': st.session_state.current_user,
            'waste_type': waste_type,
            'status': 'pending',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'credits': 0,
            'quantity': 0
        }
        
        st.session_state.waste_submissions.append(submission)
        
        if waste_type == "Organic Waste":
            user['organic_bin'] = min(user['organic_bin'] + 15, 100)
        else:
            user['inorganic_bin'] = min(user['inorganic_bin'] + 15, 100)
        
        st.success("✅ Request created!")
        st.info("⏳ Waiting for admin verification")
        st.balloons()
        st.rerun()
    
    # Withdrawal
    st.markdown("---")
    st.markdown("### 💰 Withdraw Credits")
    
    if user['credits'] >= 500:
        col_w1, col_w2 = st.columns(2)
        
        with col_w1:
            max_w = (user['credits'] // 100) * 100
            withdraw = st.number_input(
                "Credits to Withdraw",
                min_value=500,
                max_value=max_w if max_w >= 500 else user['credits'],
                step=100,
                value=500,
                key="withdraw_input"
            )
            
            w_rupees = withdraw / 20.0
            st.info(f"💵 You'll receive: **₹{w_rupees:.2f}**")
        
        with col_w2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("💸 Withdraw Now", use_container_width=True, key="btn_withdraw"):
                if user['credits'] >= withdraw:
                    user['credits'] -= withdraw
                    st.success(f"✅ Withdrawn ₹{w_rupees:.2f}!")
                    st.balloons()
                    st.rerun()
    else:
        remaining = 500 - user['credits']
        st.warning(f"⚠️ Need **{remaining} more credits** (Min: 500)")
    
    # History
    st.markdown("---")
    st.markdown("### 📜 Waste History")
    
    if user['waste_history']:
        df = pd.DataFrame(user['waste_history'])
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No submissions yet.")
    
    # Pending
    pending = [s for s in st.session_state.waste_submissions 
               if s['user'] == st.session_state.current_user and s['status'] == 'pending']
    
    if pending:
        st.markdown("### ⏳ Pending Verifications")
        for sub in pending:
            st.markdown(f"""
            <div class='status-pending'>
                ⏳ {sub['waste_type']} - {sub['timestamp']}
            </div>
            """, unsafe_allow_html=True)

# ============================================
# MANURE STORE
# ============================================
def manure_store():
    """Manure Marketplace"""
    user = st.session_state.users.get(st.session_state.current_user)
    
    if not user:
        st.error("❌ User data not found!")
        return
    
    st.title("🌿 URAMix Manure Store")
    
    st.markdown("""
    <div style='background: linear-gradient(135deg, #f57c00 0%, #ff9800 100%); 
                padding: 30px; border-radius: 20px; color: white; margin-bottom: 30px;'>
        <h2 style='margin: 0 0 10px 0;'>🌾 Premium Natural Manure</h2>
        <p style='font-size: 1.2em; margin: 0;'>
            Made from YOUR waste! Affordable, eco-friendly, supports farmers 🇮🇳
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Stock Info
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📦 Stock", f"{st.session_state.manure_stock:.1f} kg")
    
    with col2:
        st.metric("💵 Price", f"₹{st.session_state.manure_price}/kg")
    
    with col3:
        st.metric("🛒 Your Purchases", f"{user['manure_purchased']:.1f} kg")
    
    st.markdown("---")
    
    # Product Card
    col_left, col_center, col_right = st.columns([1, 2, 1])
    
    with col_center:
        st.markdown(f"""
        <div style='background: white; padding: 30px; border-radius: 20px; 
                    box-shadow: 0 8px 24px rgba(0,0,0,0.12); text-align: center;'>
            <div style='background: #fff3e0; padding: 50px; border-radius: 15px; margin-bottom: 20px;'>
                <div style='font-size: 100px;'>🌿</div>
            </div>
            <h2 style='color: #f57c00; margin: 20px 0;'>URAM Natural Manure</h2>
            <p style='color: #666; font-size: 1.1em;'>
                100% Organic • Community-Generated<br>
                Affordable • Eco-Friendly
            </p>
            <h1 style='color: #43a047; margin: 25px 0;'>₹{st.session_state.manure_price} per kg</h1>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.manure_stock > 0:
            max_qty = min(st.session_state.manure_stock, 50.0)
            quantity = st.number_input(
                "Quantity (kg)",
                min_value=1.0,
                max_value=max_qty,
                value=1.0,
                step=0.5,
                key="manure_qty"
            )
            
            total = quantity * st.session_state.manure_price
            st.info(f"💰 **Total:** ₹{total:.2f}")
            
            if st.button("🛒 Purchase Now", use_container_width=True, type="primary", key="btn_purchase"):
                if st.session_state.manure_stock >= quantity:
                    st.session_state.manure_stock -= quantity
                    user['manure_purchased'] += quantity
                    
                    st.session_state.manure_sales.append({
                        'date': datetime.now().strftime('%Y-%m-%d'),
                        'user': st.session_state.current_user,
                        'quantity': quantity,
                        'amount': total
                    })
                    
                    st.success(f"✅ Purchased {quantity} kg!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("❌ Insufficient stock!")
        else:
            st.error("❌ Out of Stock!")

# ============================================
# ADMIN DASHBOARD
# ============================================
def admin_dashboard():
    """Admin Dashboard"""
    st.title("🔧 Admin Dashboard")
    st.markdown("**Manage URAMix System**")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "📱 QR Verification",
        "🌿 Manure",
        "📊 Analytics",
        "👥 Users"
    ])
    
    # TAB 1: QR VERIFICATION
    with tab1:
        st.markdown("### 📱 Waste Verification")
        
        pending = [s for s in st.session_state.waste_submissions if s['status'] == 'pending']
        
        if pending:
            st.markdown(f"**{len(pending)} Pending**")
            
            for sub in pending:
                with st.expander(f"🗑️ {sub['waste_type']} - {sub['user']} - {sub['timestamp']}"):
                    col_a, col_b = st.columns([2, 1])
                    
                    with col_a:
                        st.write(f"**User:** {sub['user']}")
                        st.write(f"**Type:** {sub['waste_type']}")
                        st.write(f"**Time:** {sub['timestamp']}")
                        
                        qty = st.number_input(
                            "Verified Quantity (kg)",
                            min_value=0.5,
                            value=5.0,
                            step=0.5,
                            key=f"qty_{sub['id']}"
                        )
                        
                        credits, co2 = calculate_credits(sub['waste_type'], qty)
                        st.info(f"💳 Credits: {credits} | 🌍 CO₂: {co2}%")
                    
                    with col_b:
                        if st.button("✅ Verify", key=f"verify_{sub['id']}", use_container_width=True):
                            qr_data = sub['id']
                            qr_img = generate_qr_code(qr_data)
                            
                            if qr_img:
                                st.session_state.qr_codes[qr_data] = {
                                    'submission_id': sub['id'],
                                    'user': sub['user'],
                                    'waste_type': sub['waste_type'],
                                    'credits': credits,
                                    'co2_reduction': co2,
                                    'quantity': qty,
                                    'scanned': False
                                }
                                
                                sub['status'] = 'verified'
                                sub['quantity'] = qty
                                sub['credits'] = credits
                                
                                st.success("✅ QR Generated!")
                                st.image(f"data:image/png;base64,{qr_img}", width=250)
                                st.code(qr_data)
        else:
            st.info("✅ No pending!")
        
        st.markdown("---")
        st.markdown("### 🔍 Scan QR")
        
        qr_input = st.text_input("QR Code Data", key="qr_scan_input")
        
        if st.button("🔓 Process QR", key="btn_process_qr"):
            if qr_input in st.session_state.qr_codes:
                qr_info = st.session_state.qr_codes[qr_input]
                
                if not qr_info['scanned']:
                    user = st.session_state.users.get(qr_info['user'])
                    
                    if user:
                        user['credits'] += qr_info['credits']
                        user['co2_reduced'] += qr_info['co2_reduction']
                        
                        user['waste_history'].append({
                            'Date': datetime.now().strftime('%Y-%m-%d'),
                            'Type': qr_info['waste_type'],
                            'Quantity (kg)': qr_info['quantity'],
                            'Credits': qr_info['credits'],
                            'Status': 'Verified ✅'
                        })
                        
                        if qr_info['waste_type'] == "Organic Waste":
                            user['organic_bin'] = max(0, user['organic_bin'] - 20)
                            manure = update_manure_stock(qr_info['quantity'])
                            st.success(f"🌿 +{manure:.2f} kg manure!")
                        else:
                            user['inorganic_bin'] = max(0, user['inorganic_bin'] - 20)
                        
                        qr_info['scanned'] = True
                        st.session_state.total_credits_issued += qr_info['credits']
                        
                        today = datetime.now().strftime('%Y-%m-%d')
                        if today not in st.session_state.daily_waste:
                            st.session_state.daily_waste[today] = 0
                        st.session_state.daily_waste[today] += qr_info['quantity']
                        
                        st.success(f"""
✅ **QR Processed!**
👤 {qr_info['user']}
💳 {qr_info['credits']} credits
🌍 {qr_info['co2_reduction']}% CO₂
📦 {qr_info['quantity']} kg
                        """)
                        st.balloons()
                    else:
                        st.error("❌ User not found!")
                else:
                    st.warning("⚠️ Already scanned!")
            else:
                st.error("❌ Invalid QR!")
    
    # TAB 2: MANURE MANAGEMENT
    with tab2:
        st.markdown("### 🌿 Manure Management")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Stock", f"{st.session_state.manure_stock:.1f} kg")
        
        with col2:
            st.metric("Price", f"₹{st.session_state.manure_price}/kg")
        
        with col3:
            total_sold = sum([s['quantity'] for s in st.session_state.manure_sales])
            st.metric("Sold", f"{total_sold:.1f} kg")
        
        st.markdown("---")
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.markdown("#### Add Stock")
            add_stock = st.number_input("Stock (kg)", min_value=0.0, value=50.0, step=10.0, key="add_stock_input")
            
            if st.button("➕ Add", key="btn_add_stock"):
                st.session_state.manure_stock += add_stock
                st.success(f"✅ +{add_stock} kg!")
                st.rerun()
        
        with col_b:
            st.markdown("#### Update Price")
            new_price = st.number_input("Price (₹/kg)", min_value=10, value=st.session_state.manure_price, step=5, key="price_input")
            
            if st.button("💰 Update", key="btn_update_price"):
                st.session_state.manure_price = new_price
                st.success(f"✅ ₹{new_price}/kg!")
                st.rerun()
        
        st.markdown("---")
        st.markdown("#### Sales History")
        
        if st.session_state.manure_sales:
            df = pd.DataFrame(st.session_state.manure_sales)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            revenue = sum([s['amount'] for s in st.session_state.manure_sales])
            st.success(f"💰 Revenue: ₹{revenue:.2f}")
        else:
            st.info("No sales yet.")
    
    # TAB 3: ANALYTICS
    with tab3:
        st.markdown("### 📊 Analytics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Users", len(st.session_state.users))
        
        with col2:
            st.metric("Credits", st.session_state.total_credits_issued)
        
        with col3:
            total_waste = sum(st.session_state.daily_waste.values())
            st.metric("Waste (kg)", f"{total_waste:.1f}")
        
        with col4:
            verified = len([s for s in st.session_state.waste_submissions if s['status'] == 'verified'])
            st.metric("Verified", verified)
        
        st.markdown("---")
        
        if st.session_state.daily_waste:
            st.markdown("#### Daily Waste Collection")
            
            dates = list(st.session_state.daily_waste.keys())
            quantities = list(st.session_state.daily_waste.values())
            
            fig1, ax1 = plt.subplots(figsize=(10, 5))
            ax1.bar(dates, quantities, color='#43a047', alpha=0.8, edgecolor='#2e7d32', linewidth=2)
            ax1.set_xlabel('Date', fontsize=12, fontweight='bold')
            ax1.set_ylabel('Waste (kg)', fontsize=12, fontweight='bold')
            ax1.set_title('Daily Waste Collection', fontsize=14, fontweight='bold')
            ax1.grid(axis='y', alpha=0.3)
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig1)
            plt.close()
        
        if st.session_state.manure_sales:
            st.markdown("#### Manure Sales Trend")
            
            df = pd.DataFrame(st.session_state.manure_sales)
            sales = df.groupby('date')['quantity'].sum()
            
            fig2, ax2 = plt.subplots(figsize=(10, 5))
            ax2.plot(sales.index, sales.values, marker='o', color='#f57c00', linewidth=3, markersize=10)
            ax2.set_xlabel('Date', fontsize=12, fontweight='bold')
            ax2.set_ylabel('Quantity (kg)', fontsize=12, fontweight='bold')
            ax2.set_title('Manure Sales', fontsize=14, fontweight='bold')
            ax2.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig2)
            plt.close()
    
    # TAB 4: USERS
    with tab4:
        st.markdown("### 👥 Users")
        
        if st.session_state.users:
            users_data = []
            
            for email, data in st.session_state.users.items():
                users_data.append({
                    'Email': email,
                    'Credits': data['credits'],
                    'Wallet (₹)': f"{data['credits']/20:.2f}",
                    'Submissions': len(data['waste_history']),
                    'Manure (kg)': f"{data['manure_purchased']:.1f}",
                    'CO₂ (%)': f"{data['co2_reduced']:.1f}"
                })
            
            df = pd.DataFrame(users_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            st.markdown("---")
            st.markdown("#### Statistics")
            
            total_credits = sum([u['credits'] for u in st.session_state.users.values()])
            total_co2 = sum([u['co2_reduced'] for u in st.session_state.users.values()])
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Credits", total_credits)
            
            with col2:
                st.metric("Money", f"₹{total_credits/20:.2f}")
            
            with col3:
                st.metric("CO₂ Reduced", f"{total_co2:.1f}%")
        else:
            st.info("No users yet.")

# ============================================
# MAIN APPLICATION
# ============================================
def main():
    """Main Application Router"""
    
    # Initialize Session State
    init_session_state()
    
    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <h1 style='color: #43a047; margin: 0;'>♻️ URAMix</h1>
            <p style='color: #666; margin: 5px 0;'>Waste to Wealth</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        if st.session_state.logged_in:
            if st.session_state.is_admin:
                st.success("🔧 **Admin Mode**")
                page = "Admin"
            else:
                st.success(f"👤 **{st.session_state.current_user}**")
                
                page = st.radio(
                    "Navigation",
                    ["🏠 Home", "📊 Dashboard", "🛒 Manure Store"],
                    label_visibility="collapsed"
                )
                
                page = page.split(" ", 1)[1] if " " in page else page
            
            st.markdown("---")
            
            if st.button("🚪 Logout", use_container_width=True, key="btn_logout"):
                logout()
                st.rerun()
        else:
            st.info("Please login")
            page = "Login"
        
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; font-size: 0.8em; color: #999;'>
            <p>🇮🇳 Clean India Mission</p>
            <p>Hackathon 2024</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Page Routing
    if not st.session_state.logged_in:
        auth_page()
    else:
        if st.session_state.is_admin:
            admin_dashboard()
        else:
            if page == "Home":
                home_page()
            elif page == "Dashboard":
                user_dashboard()
            elif page == "Manure Store":
                manure_store()

# Run Application
if __name__ == "__main__":
    main()
