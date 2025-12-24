import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import random
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io
import base64

# ============================================
# PAGE CONFIGURATION
# ============================================
st.set_page_config(
    page_title="URAMix - Waste to Value",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CUSTOM CSS - GREEN & WHITE ECO THEME
# ============================================
st.markdown("""
<style>
    .main {
        background-color: #f5fdf5;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #4CAF50 0%, #2e7d32 100%);
        color: white;
        border-radius: 12px;
        padding: 12px 28px;
        border: none;
        font-weight: 600;
        transition: all 0.3s;
        box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(76, 175, 80, 0.4);
    }
    
    .hero-section {
        background: linear-gradient(135deg, #2e7d32 0%, #66bb6a 100%);
        padding: 40px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.2);
    }
    
    .tagline {
        font-size: 32px;
        font-weight: bold;
        color: #2e7d32;
        text-align: center;
        margin: 20px 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        animation: fadeIn 1.5s;
    }
    
    .problem-card {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
        color: white;
        padding: 25px;
        border-radius: 15px;
        margin: 15px 0;
        box-shadow: 0 6px 15px rgba(0,0,0,0.2);
        animation: slideIn 0.8s ease-out;
        transition: transform 0.3s;
    }
    
    .problem-card:hover {
        transform: scale(1.02);
    }
    
    .eco-quote {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        padding: 25px;
        border-left: 6px solid #4CAF50;
        border-radius: 10px;
        margin: 20px 0;
        font-size: 20px;
        color: #1b5e20;
        font-weight: 600;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    
    .metric-card {
        background: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        text-align: center;
        transition: transform 0.3s;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    }
    
    .product-card {
        background: white;
        border: 2px solid #e0e0e0;
        border-radius: 15px;
        padding: 20px;
        margin: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transition: all 0.3s;
    }
    
    .product-card:hover {
        border-color: #4CAF50;
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(76, 175, 80, 0.3);
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
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
    
    .wallet-display {
        background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
        padding: 20px;
        border-radius: 15px;
        color: #1b5e20;
        font-weight: bold;
        text-align: center;
        box-shadow: 0 4px 12px rgba(255, 215, 0, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# SESSION STATE INITIALIZATION
# ============================================
def init_session_state():
    """Initialize all session state variables"""
    if 'users' not in st.session_state:
        st.session_state.users = {}
    
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if 'current_user' not in st.session_state:
        st.session_state.current_user = None
    
    if 'is_admin' not in st.session_state:
        st.session_state.is_admin = False
    
    if 'waste_bookings' not in st.session_state:
        st.session_state.waste_bookings = []
    
    if 'qr_codes' not in st.session_state:
        st.session_state.qr_codes = {}
    
    if 'manure_stock' not in st.session_state:
        st.session_state.manure_stock = 500  # URAM Count
    
    if 'manure_price' not in st.session_state:
        st.session_state.manure_price = 12  # ₹ per kg
    
    if 'manure_sales' not in st.session_state:
        st.session_state.manure_sales = []
    
    if 'feedback_list' not in st.session_state:
        st.session_state.feedback_list = []
    
    if 'daily_credits_data' not in st.session_state:
        st.session_state.daily_credits_data = []

init_session_state()

# ============================================
# HELPER FUNCTIONS
# ============================================

def calculate_credits(waste_type):
    """
    Calculate credits based on waste type (NOT quantity)
    Organic → Higher credits
    Inorganic → Lower credits
    """
    if waste_type == "Organic":
        return 150  # Higher credits for organic
    else:  # Inorganic
        return 100  # Lower credits for inorganic

def credits_to_rupees(credits):
    """Convert credits to rupees: 1 credit = ₹0.05, 20 credits = ₹1"""
    return round(credits * 0.05, 2)

def rupees_to_credits(rupees):
    """Convert rupees to credits: ₹1 = 20 credits"""
    return int(rupees * 20)

def generate_qr_code(booking_id, waste_type, credits):
    """Generate QR code for booking"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    qr_data = f"URAMIX|{booking_id}|{waste_type}|{credits}"
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="#2e7d32", back_color="white")
    return img

def send_feedback_email(user_email, feedback_text):
    """
    Mock function to send feedback via email
    In production, use actual SMTP:
    
    import smtplib
    from email.mime.text import MIMEText
    
    sender = "uramix@gmail.com"
    recipient = "admin@uramix.com"
    msg = MIMEText(feedback_text)
    msg['Subject'] = f'Feedback from {user_email}'
    msg['From'] = sender
    msg['To'] = recipient
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender, 'app_password')
        smtp.send_message(msg)
    """
    # Store feedback in session state
    st.session_state.feedback_list.append({
        'email': user_email,
        'feedback': feedback_text,
        'timestamp': datetime.datetime.now()
    })
    return True

# ============================================
# AUTHENTICATION FUNCTIONS
# ============================================

def signup_user(email, password):
    """Create new user account with referral bonus"""
    if email in st.session_state.users:
        return False, "Email already exists"
    
    st.session_state.users[email] = {
        'password': password,
        'credits': 20,  # Referral bonus
        'bookings': [],
        'uram_count': 0,  # Manure purchased count
        'transactions': []
    }
    return True, "Account created successfully!"

def login_user(email, password):
    """Login user or admin"""
    # Admin login
    if email == "admin" and password == "12345":
        st.session_state.logged_in = True
        st.session_state.is_admin = True
        st.session_state.current_user = "admin"
        return True, "Admin login successful"
    
    # User login
    if email in st.session_state.users:
        if st.session_state.users[email]['password'] == password:
            st.session_state.logged_in = True
            st.session_state.is_admin = False
            st.session_state.current_user = email
            return True, "Login successful"
        else:
            return False, "Incorrect password"
    
    return False, "Email not found"

def logout_user():
    """Logout current user"""
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.session_state.is_admin = False

# ============================================
# LOGIN & SIGNUP PAGE
# ============================================

def login_signup_page():
    """Authentication page"""
    
    # Hero header
    st.markdown("""
    <div class='hero-section'>
        <h1 style='font-size: 48px; margin: 0;'>🌱 URAMix</h1>
        <p style='font-size: 28px; margin: 10px 0;'>♻️ WASTE TO VALUE ♻️</p>
        <p style='font-size: 18px; opacity: 0.9;'>Transforming India's Waste Crisis into Opportunity</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        tab1, tab2 = st.tabs(["🔑 Login", "✨ Sign Up"])
        
        with tab1:
            st.subheader("Welcome Back!")
            
            email = st.text_input("Email Address", key="login_email", placeholder="Enter your email")
            password = st.text_input("Password", type="password", key="login_pass", placeholder="Enter password")
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                if st.button("🚀 Login", use_container_width=True):
                    if email and password:
                        success, message = login_user(email, password)
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
                    else:
                        st.warning("Please fill all fields")
            
            with col_b:
                if st.button("🔐 Google Sign-In (Demo)", use_container_width=True):
                    demo_email = "demo@google.com"
                    if demo_email not in st.session_state.users:
                        signup_user(demo_email, "demo123")
                    login_user(demo_email, "demo123")
                    st.success("Google Sign-In successful!")
                    st.rerun()
        
        with tab2:
            st.subheader("Join the Green Revolution!")
            
            new_email = st.text_input("Email Address", key="signup_email", placeholder="your@email.com")
            new_pass = st.text_input("Password", type="password", key="signup_pass", placeholder="Create password")
            confirm_pass = st.text_input("Confirm Password", type="password", placeholder="Re-enter password")
            
            if st.button("🌟 Create Account", use_container_width=True):
                if not new_email or not new_pass:
                    st.warning("Please fill all fields")
                elif new_pass != confirm_pass:
                    st.error("Passwords don't match")
                elif len(new_pass) < 6:
                    st.error("Password must be at least 6 characters")
                else:
                    success, message = signup_user(new_email, new_pass)
                    if success:
                        st.success(f"{message} You got 20 referral credits! 🎉")
                        st.balloons()
                    else:
                        st.error(message)

# ============================================
# HOME PAGE
# ============================================

def home_page():
    """Main home page with problem statement and metrics"""
    
    # Logo and tagline
    st.markdown("<h1 style='text-align: center; color: #2e7d32; font-size: 48px;'>🌱 URAMix</h1>", unsafe_allow_html=True)
    st.markdown("<p class='tagline'>♻️ WASTE TO VALUE ♻️</p>", unsafe_allow_html=True)
    
    # Get user data
    user_data = st.session_state.users.get(st.session_state.current_user, {})
    credits = user_data.get('credits', 0)
    
    # Dynamic eco quote
    reduction_percentage = round(credits * 0.08, 2)
    st.markdown(f"""
    <div class='eco-quote'>
        🌍 You helped reduce landfill emissions by {reduction_percentage}% today!<br>
        Your eco-credits increased! Keep making a difference! 🌱
    </div>
    """, unsafe_allow_html=True)
    
    # Hero images section
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        st.markdown("### 🗑️ Waste Collection")
        st.image("https://via.placeholder.com/250x200/4CAF50/FFFFFF?text=Dustbin", use_container_width=True)
        st.write("Submit your segregated waste")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        st.markdown("### ⭐ Earn Credits")
        st.image("https://via.placeholder.com/250x200/FFC107/FFFFFF?text=Credits", use_container_width=True)
        st.write("Get rewarded for segregation")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        st.markdown("### 🌾 Buy Manure")
        st.image("https://via.placeholder.com/250x200/8BC34A/FFFFFF?text=Manure", use_container_width=True)
        st.write("Affordable natural fertilizer")
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Problem statement cards (animated)
    st.markdown("## 💡 Problems We Solve")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='problem-card'>
            <h3>🚮 Waste Management Crisis</h3>
            <ul style='font-size: 16px; line-height: 1.8;'>
                <li>People dump waste early - bins fill before collection</li>
                <li>Irregular garbage collection schedules</li>
                <li>No incentive for proper waste segregation</li>
                <li>Landfills overflowing across Indian cities</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='problem-card'>
            <h3>🌾 Farming Challenges</h3>
            <ul style='font-size: 16px; line-height: 1.8;'>
                <li>Natural manure is expensive and unaffordable</li>
                <li>Small farmers can't compete with big companies</li>
                <li>Chemical fertilizers harm soil health</li>
                <li>Lack of affordable organic alternatives</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # User dashboard metrics
    st.markdown("## 📊 Your Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("⭐ Your Credits", user_data.get('credits', 0))
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        rupees = credits_to_rupees(user_data.get('credits', 0))
        st.metric("💰 Wallet Value", f"₹{rupees}")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("📦 Waste Submitted", len(user_data.get('bookings', [])))
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col4:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("🌾 URAM Count", user_data.get('uram_count', 0))
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Platform impact
    st.markdown("---")
    st.markdown("## 🌍 Platform Impact")
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_users = len(st.session_state.users)
    total_bookings = len(st.session_state.waste_bookings)
    total_credits = sum([u.get('credits', 0) for u in st.session_state.users.values()])
    
    col1.metric("👥 Total Users", total_users)
    col2.metric("♻️ Waste Collections", total_bookings)
    col3.metric("⭐ Credits Issued", total_credits)
    col4.metric("🌾 Manure Stock", f"{st.session_state.manure_stock} kg")

# ============================================
# WASTE SUBMISSION PAGE
# ============================================

def waste_submission_page():
    """User waste submission page"""
    
    st.title("♻️ Submit Your Waste")
    
    user_data = st.session_state.users[st.session_state.current_user]
    
    # Wallet display
    st.markdown(f"""
    <div class='wallet-display'>
        <h3>💳 Your Wallet</h3>
        <p style='font-size: 24px; margin: 10px 0;'>
            ⭐ {user_data['credits']} Credits = ₹{credits_to_rupees(user_data['credits'])}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Waste submission form
    st.subheader("📝 Book Waste Collection")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        waste_type = st.selectbox(
            "🗑️ Select Waste Type",
            ["Organic", "Inorganic"],
            help="Choose the type of waste you want to submit"
        )
        
        # Show credits info
        credits_earned = calculate_credits(waste_type)
        
        st.info(f"""
        **Credit Information:**
        
        🌿 **Organic Waste:** 150 credits
        
        ♻️ **Inorganic Waste:** 100 credits
        
        **You will earn:** ⭐ {credits_earned} credits
        """)
    
    with col2:
        address = st.text_area(
            "📍 Pickup Address",
            placeholder="Enter your complete address for waste pickup...",
            height=150
        )
        
        phone = st.text_input("📞 Contact Number", placeholder="Your phone number")
    
    if st.button("📤 Submit Booking Request", use_container_width=True, type="primary"):
        if address and phone:
            booking_id = f"URX{len(st.session_state.waste_bookings) + 1001}"
            
            booking = {
                'booking_id': booking_id,
                'user': st.session_state.current_user,
                'waste_type': waste_type,
                'credits_earned': credits_earned,
                'address': address,
                'phone': phone,
                'status': 'Pending',
                'timestamp': datetime.datetime.now(),
                'quantity_verified': None
            }
            
            st.session_state.waste_bookings.append(booking)
            user_data['bookings'].append(booking_id)
            
            st.success(f"✅ Booking successful! Your Booking ID: **{booking_id}**")
            st.info("Admin will verify your waste and generate QR code. You can then scan it to claim credits!")
            st.balloons()
        else:
            st.error("⚠️ Please provide address and phone number")
    
    # Show user bookings
    st.markdown("---")
    st.subheader("📋 Your Bookings")
    
    user_bookings = [b for b in st.session_state.waste_bookings if b['user'] == st.session_state.current_user]
    
    if user_bookings:
        for booking in reversed(user_bookings):
            status_emoji = "⏳" if booking['status'] == "Pending" else "✅" if booking['status'] == "Approved" else "🎉"
            
            with st.expander(f"{status_emoji} {booking['booking_id']} - {booking['waste_type']} - {booking['status']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Waste Type:** {booking['waste_type']}")
                    st.write(f"**Credits:** ⭐ {booking['credits_earned']}")
                    st.write(f"**Status:** {booking['status']}")
                    st.write(f"**Date:** {booking['timestamp'].strftime('%d %b %Y, %I:%M %p')}")
                
                with col2:
                    if booking['status'] == 'Approved' and booking['booking_id'] in st.session_state.qr_codes:
                        st.write("**QR Code Generated! Scan below:**")
                        qr_img = st.session_state.qr_codes[booking['booking_id']]
                        st.image(qr_img, width=200)
                        
                        if st.button(f"📱 Scan & Claim Credits", key=f"claim_{booking['booking_id']}"):
                            user_data['credits'] += booking['credits_earned']
                            booking['status'] = 'Completed'
                            
                            # Add to daily credits
                            st.session_state.daily_credits_data.append({
                                'date': datetime.datetime.now().strftime('%Y-%m-%d'),
                                'credits': booking['credits_earned']
                            })
                            
                            st.success(f"🎉 {booking['credits_earned']} credits added to your wallet!")
                            st.rerun()
                    else:
                        st.info("⏳ Waiting for admin verification")
    else:
        st.info("📭 No bookings yet. Submit your first waste collection request!")

# ============================================
# WALLET & WITHDRAWAL PAGE
# ============================================

def wallet_page():
    """Wallet and withdrawal management"""
    
    st.title("💰 Wallet & Withdrawals")
    
    user_data = st.session_state.users[st.session_state.current_user]
    credits = user_data['credits']
    rupees = credits_to_rupees(credits)
    
    # Wallet overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='metric-card' style='background: linear-gradient(135deg, #4CAF50 0%, #2e7d32 100%); color: white;'>
            <h2 style='color: white;'>⭐ Credits</h2>
            <h1 style='color: white; margin: 10px 0;'>{}</h1>
        </div>
        """.format(credits), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='metric-card' style='background: linear-gradient(135deg, #FFC107 0%, #FFA000 100%); color: white;'>
            <h2 style='color: white;'>💵 Rupees</h2>
            <h1 style='color: white; margin: 10px 0;'>₹{}</h1>
        </div>
        """.format(rupees), unsafe_allow_html=True)
    
    with col3:
        withdrawal_status = "✅ Available" if credits >= 500 else "🔒 Locked"
        st.markdown("""
        <div class='metric-card'>
            <h2>🎯 Status</h2>
            <h1 style='margin: 10px 0;'>{}</h1>
        </div>
        """.format(withdrawal_status), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Conversion info
    st.info("""
    💡 **Credit System:**
    - 1 credit = ₹0.05
    - 20 credits = ₹1
    - Minimum withdrawal: 500 credits (₹25)
    """)
    
    # Withdrawal section
    st.subheader("💸 Withdraw Money")
    
    if credits >= 500:
        st.success("✅ You can withdraw money now!")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            credits_to_withdraw = st.number_input(
                "Credits to Withdraw",
                min_value=500,
                max_value=credits,
                step=100,
                value=500
            )
            
            withdrawal_amount = credits_to_rupees(credits_to_withdraw)
            
            st.write(f"**You will receive:** ₹{withdrawal_amount}")
            
            bank_name = st.text_input("Bank Name", placeholder="e.g., SBI, HDFC")
            account_number = st.text_input("Account Number", placeholder="Enter account number")
            
            if st.button("💰 Withdraw to Bank", use_container_width=True, type="primary"):
                if bank_name and account_number:
                    user_data['credits'] -= credits_to_withdraw
                    
                    transaction = {
                        'type': 'Withdrawal',
                        'credits': credits_to_withdraw,
                        'amount': withdrawal_amount,
                        'bank': bank_name,
                        'timestamp': datetime.datetime.now()
                    }
                    user_data['transactions'].append(transaction)
                    
                    st.success(f"✅ ₹{withdrawal_amount} withdrawn successfully!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("Please provide bank details")
        
        with col2:
            # Progress bar
            st.write("**Withdrawal Progress:**")
            progress = min(credits / 500, 1.0)
            st.progress(progress)
            st.write(f"{int(progress * 100)}% eligible")
    else:
        remaining = 500 - credits
        st.warning(f"⚠️ You need {remaining} more credits to withdraw")
        
        progress = credits / 500
        st.progress(progress)
        st.write(f"Progress: {int(progress * 100)}%")
    
    # Transaction history
    st.markdown("---")
    st.subheader("📜 Transaction History")
    
    if user_data.get('transactions'):
        for trans in reversed(user_data['transactions']):
            with st.expander(f"💳 {trans['type']} - {trans['timestamp'].strftime('%d %b %Y')}"):
                st.write(f"**Credits:** {trans['credits']}")
                st.write(f"**Amount:** ₹{trans['amount']}")
                if 'bank' in trans:
                    st.write(f"**Bank:** {trans['bank']}")
    else:
        st.info("No transactions yet")

# ============================================
# MANURE MARKETPLACE 
# ============================================

def manure_marketplace():
    """Manure marketplace"""
    
    st.title("🌾 Natural Manure Store")
    
    user_data = st.session_state.users[st.session_state.current_user]
    
    # User wallet display
    rupees = credits_to_rupees(user_data['credits'])
    
    st.markdown(f"""
    <div class='wallet-display'>
        <h3>💰 Your Wallet: ₹{rupees} ({user_data['credits']} credits)</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Product showcase (Flipkart style)
    st.subheader("🛒 Available Products")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    # Product 1: Organic Manure
    with col1:
        st.markdown("""
        <div class='product-card'>
            <div style='text-align: center;'>
                <h3 style='color: #2e7d32;'>🌿 Organic Manure</h3>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.image("https://via.placeholder.com/300x200/8BC34A/FFFFFF?text=Organic+Manure", use_container_width=True)
        st.write("**Premium Quality Organic Fertilizer**")
        st.write(f"💰 **Price:** ₹{st.session_state.manure_price}/kg")
        st.write(f"📦 **Available:** {st.session_state.manure_stock} kg")
        
        qty1 = st.number_input("Quantity (kg)", min_value=1, max_value=50, value=10, key="qty1")
        total1 = qty1 * st.session_state.manure_price
        
        st.write(f"**Total:** ₹{total1}")
        
        if st.button("🛍️ Buy Now", key="buy1", use_container_width=True):
            if rupees >= total1:
                if st.session_state.manure_stock >= qty1:
                    # Deduct money (convert rupees to credits)
                    credits_to_deduct = rupees_to_credits(total1)
                    user_data['credits'] -= credits_to_deduct
                    user_data['uram_count'] += qty1
                    
                    # Update stock
                    st.session_state.manure_stock -= qty1
                    
                    # Record sale
                    st.session_state.manure_sales.append({
                        'user': st.session_state.current_user,
                        'quantity': qty1,
                        'amount': total1,
                        'timestamp': datetime.datetime.now()
                    })
                    
                    st.success(f"✅ Purchased {qty1} kg manure! URAM Count: {user_data['uram_count']}")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("Insufficient stock")
            else:
                st.error("Insufficient balance. Earn more credits!")
    
    # Product 2: Premium Compost
    with col2:
        st.markdown("""
        <div class='product-card'>
            <div style='text-align: center;'>
                <h3 style='color: #2e7d32;'>🌾 Premium Compost</h3>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.image("https://via.placeholder.com/300x200/689F38/FFFFFF?text=Premium+Compost", use_container_width=True)
        st.write("**High-Grade Composted Fertilizer**")
        premium_price = st.session_state.manure_price + 3
        st.write(f"💰 **Price:** ₹{premium_price}/kg")
        st.write(f"📦 **Available:** {int(st.session_state.manure_stock * 0.6)} kg")
        
        qty2 = st.number_input("Quantity (kg)", min_value=1, max_value=50, value=5, key="qty2")
        total2 = qty2 * premium_price
        
        st.write(f"**Total:** ₹{total2}")
        
        if st.button("🛍️ Buy Now", key="buy2", use_container_width=True):
            if rupees >= total2:
                credits_to_deduct = rupees_to_credits(total2)
                user_data['credits'] -= credits_to_deduct
                user_data['uram_count'] += qty2
                
                st.session_state.manure_sales.append({
                    'user': st.session_state.current_user,
                    'quantity': qty2,
                    'amount': total2,
                    'timestamp': datetime.datetime.now()
                })
                
                st.success(f"✅ Purchased {qty2} kg compost! URAM Count: {user_data['uram_count']}")
                st.balloons()
                st.rerun()
            else:
                st.error("Insufficient balance")
    
    # Product 3: Vermicompost
    with col3:
        st.markdown("""
        <div class='product-card'>
            <div style='text-align: center;'>
                <h3 style='color: #2e7d32;'>🪱 Vermicompost</h3>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.image("https://via.placeholder.com/300x200/558B2F/FFFFFF?text=Vermicompost", use_container_width=True)
        st.write("**Earthworm-Processed Organic Manure**")
        vermi_price = st.session_state.manure_price + 5
        st.write(f"💰 **Price:** ₹{vermi_price}/kg")
        st.write(f"📦 **Available:** {int(st.session_state.manure_stock * 0.4)} kg")
        
        qty3 = st.number_input("Quantity (kg)", min_value=1, max_value=50, value=8, key="qty3")
        total3 = qty3 * vermi_price
        
        st.write(f"**Total:** ₹{total3}")
        
        if st.button("🛍️ Buy Now", key="buy3", use_container_width=True):
            if rupees >= total3:
                credits_to_deduct = rupees_to_credits(total3)
                user_data['credits'] -= credits_to_deduct
                user_data['uram_count'] += qty3
                
                st.session_state.manure_sales.append({
                    'user': st.session_state.current_user,
                    'quantity': qty3,
                    'amount': total3,
                    'timestamp': datetime.datetime.now()
                })
                
                st.success(f"✅ Purchased {qty3} kg vermicompost! URAM Count: {user_data['uram_count']}")
                st.balloons()
                st.rerun()
            else:
                st.error("Insufficient balance")
    
    # User's URAM Count
    st.markdown("---")
    st.subheader("📊 Your URAM Count")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🌾 Total Manure Purchased", f"{user_data['uram_count']} kg")
    
    with col2:
        st.metric("💰 Wallet Balance", f"₹{rupees}")
    
    with col3:
        st.metric("⭐ Available Credits", user_data['credits'])

# ============================================
# FEEDBACK PAGE
# ============================================

def feedback_page():
    """User feedback submission"""
    
    st.title("📝 Feedback & Support")
    
    st.write("Help us improve URAMix! Share your thoughts and suggestions.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        feedback_text = st.text_area(
            "Your Feedback",
            placeholder="Tell us about your experience, suggestions, or report issues...",
            height=200
        )
        
        rating = st.slider("Rate your experience", 1, 5, 5, help="1 = Poor, 5 = Excellent")
        
        if st.button("📤 Submit Feedback", use_container_width=True, type="primary"):
            if feedback_text:
                success = send_feedback_email(st.session_state.current_user, feedback_text)
                
                if success:
                    st.success("✅ Thank you for your feedback! Admin will review it soon.")
                    st.balloons()
                else:
                    st.error("Failed to send feedback. Please try again.")
            else:
                st.error("Please enter your feedback")
    
    with col2:
        st.info("""
        **Contact Information:**
        
        📧 **Email:** 
        support@uramix.com
        
        📞 **Phone:** 
        +91-8438386610
        
        ⏰ **Hours:** 
        24/7 Support
        
        📍 **Address:** 
        Clean India Initiative
        New Delhi, India
        """)

# ============================================
# ADMIN DASHBOARD
# ============================================

def admin_dashboard():
    """Complete admin dashboard"""
    
    st.title("👨‍💼 Admin Dashboard")
    
    # Overview metrics
    st.subheader("📊 Platform Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_users = len(st.session_state.users)
    total_bookings = len(st.session_state.waste_bookings)
    pending_bookings = len([b for b in st.session_state.waste_bookings if b['status'] == 'Pending'])
    total_credits = sum([u.get('credits', 0) for u in st.session_state.users.values()])
    
    col1.metric("👥 Total Users", total_users)
    col2.metric("📦 Total Bookings", total_bookings)
    col3.metric("⏳ Pending", pending_bookings)
    col4.metric("⭐ Credits Issued", total_credits)
    
    st.markdown("---")
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🗑️ Manage Bookings", "📈 Analytics", "🌾 Manure Management", "💬 Feedback"])
    
    with tab1:
        st.subheader("Waste Collection Bookings")
        
        # Pending bookings
        st.markdown("### ⏳ Pending Verification")
        
        pending = [b for b in st.session_state.waste_bookings if b['status'] == 'Pending']
        
        if pending:
            for booking in pending:
                with st.expander(f"📋 {booking['booking_id']} - {booking['waste_type']} ({booking['user']})"):
                    col1, col2 = st.columns([1, 1])
                    
                    with col1:
                        st.write(f"**User:** {booking['user']}")
                        st.write(f"**Waste Type:** {booking['waste_type']}")
                        st.write(f"**Credits to Award:** ⭐ {booking['credits_earned']}")
                        st.write(f"**Phone:** {booking['phone']}")
                        st.write(f"**Address:** {booking['address']}")
                        st.write(f"**Requested:** {booking['timestamp'].strftime('%d %b %Y, %I:%M %p')}")
                    
                    with col2:
                        quantity_verified = st.number_input(
                            "Verified Quantity (kg)",
                            min_value=1,
                            max_value=100,
                            value=10,
                            key=f"qty_{booking['booking_id']}"
                        )
                        
                        st.info(f"**Credits:** {booking['credits_earned']}")
                        
                        if st.button(f"✅ Approve & Generate QR", key=f"approve_{booking['booking_id']}"):
                            # Update booking
                            booking['status'] = 'Approved'
                            booking['quantity_verified'] = quantity_verified
                            
                            # Generate QR code
                            qr_img = generate_qr_code(
                                booking['booking_id'],
                                booking['waste_type'],
                                booking['credits_earned']
                            )
                            st.session_state.qr_codes[booking['booking_id']] = qr_img
                            
                            st.success(f"✅ Booking {booking['booking_id']} approved!")
                            st.rerun()
        else:
            st.info("No pending bookings")
        
        # Approved bookings
        st.markdown("---")
        st.markdown("### ✅ Approved Bookings")
        
        approved = [b for b in st.session_state.waste_bookings if b['status'] == 'Approved']
        
        if approved:
            for booking in approved:
                with st.expander(f"✅ {booking['booking_id']} - {booking['waste_type']}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**User:** {booking['user']}")
                        st.write(f"**Verified Qty:** {booking['quantity_verified']} kg")
                        st.write(f"**Credits:** {booking['credits_earned']}")
                    
                    with col2:
                        if booking['booking_id'] in st.session_state.qr_codes:
                            st.write("**QR Code:**")
                            st.image(st.session_state.qr_codes[booking['booking_id']], width=150)
        else:
            st.info("No approved bookings yet")
    
    with tab2:
        st.subheader("📈 Platform Analytics")
        
        # Credits chart
        if st.session_state.daily_credits_data:
            st.markdown("### Daily Credits Distribution")
            
            df = pd.DataFrame(st.session_state.daily_credits_data)
            df_grouped = df.groupby('date')['credits'].sum().reset_index()
            
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.bar(df_grouped['date'], df_grouped['credits'], color='#4CAF50', alpha=0.8)
            ax.set_xlabel('Date', fontsize=12)
            ax.set_ylabel('Credits Issued', fontsize=12)
            ax.set_title('Daily Credits Distribution', fontsize=14, fontweight='bold')
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.info("No credit data available yet")
        
        # Waste type distribution
        st.markdown("---")
        st.markdown("### Waste Type Distribution")
        
        organic_count = len([b for b in st.session_state.waste_bookings if b['waste_type'] == 'Organic'])
        inorganic_count = len([b for b in st.session_state.waste_bookings if b['waste_type'] == 'Inorganic'])
        
        if organic_count + inorganic_count > 0:
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.pie(
                [organic_count, inorganic_count],
                labels=['Organic', 'Inorganic'],
                colors=['#8BC34A', '#FFC107'],
                autopct='%1.1f%%',
                startangle=90,
                textprops={'fontsize': 12, 'fontweight': 'bold'}
            )
            ax.set_title('Waste Segregation Analysis', fontsize=14, fontweight='bold')
            st.pyplot(fig)
        else:
            st.info("No waste data available")
        
        # Manure sales chart
        if st.session_state.manure_sales:
            st.markdown("---")
            st.markdown("### Manure Sales Analytics")
            
            sales_df = pd.DataFrame(st.session_state.manure_sales)
            
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(range(len(sales_df)), sales_df['quantity'].cumsum(), marker='o', color='#8BC34A', linewidth=2)
            ax.set_xlabel('Transaction', fontsize=12)
            ax.set_ylabel('Cumulative Quantity (kg)', fontsize=12)
            ax.set_title('Manure Sales Trend', fontsize=14, fontweight='bold')
            ax.grid(alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)
    
    with tab3:
        st.subheader("🌾 Manure Stock Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📦 Stock Control")
            
            st.metric("Current Stock (URAM Count)", f"{st.session_state.manure_stock} kg")
            
            add_stock = st.number_input("Add Stock (kg)", min_value=0, max_value=2000, value=100)
            
            if st.button("➕ Add Stock", use_container_width=True):
                st.session_state.manure_stock += add_stock
                st.success(f"✅ Added {add_stock} kg to stock!")
                st.rerun()
        
        with col2:
            st.markdown("### 💰 Pricing Control")
            
            st.metric("Current Price", f"₹{st.session_state.manure_price}/kg")
            
            new_price = st.number_input(
                "Update Price (₹/kg)",
                min_value=5,
                max_value=50,
                value=st.session_state.manure_price
            )
            
            if st.button("💰 Update Price", use_container_width=True):
                st.session_state.manure_price = new_price
                st.success(f"✅ Price updated to ₹{new_price}/kg!")
                st.rerun()
        
        # Sales summary
        st.markdown("---")
        st.markdown("### 📊 Sales Summary")
        
        if st.session_state.manure_sales:
            total_sold = sum([s['quantity'] for s in st.session_state.manure_sales])
            total_revenue = sum([s['amount'] for s in st.session_state.manure_sales])
            
            col1, col2, col3 = st.columns(3)
            col1.metric("🌾 Total Sold", f"{total_sold} kg")
            col2.metric("💰 Revenue", f"₹{total_revenue}")
            col3.metric("📦 Transactions", len(st.session_state.manure_sales))
        else:
            st.info("No sales data yet")
    
    with tab4:
        st.subheader("💬 User Feedback")
        
        if st.session_state.feedback_list:
            for idx, feedback in enumerate(reversed(st.session_state.feedback_list)):
                with st.expander(f"📧 {feedback['email']} - {feedback['timestamp'].strftime('%d %b %Y, %I:%M %p')}"):
                    st.write(f"**Rating:** {'⭐' * feedback.get('rating', 5)}")
                    st.write(f"**Feedback:**")
                    st.write(feedback['feedback'])
                    
                    if st.button(f"✅ Mark as Reviewed", key=f"review_{idx}"):
                        st.success("Feedback marked as reviewed")
        else:
            st.info("No feedback received yet")

# ============================================
# MAIN APPLICATION
# ============================================

def main():
    """Main application controller"""
    
    # Check if logged in
    if not st.session_state.logged_in:
        login_signup_page()
        return
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🌱 URAMix")
        st.markdown("**Waste to Value**")
        st.markdown("---")
        
        if st.session_state.is_admin:
            st.markdown("**👨‍💼 Admin Panel**")
            page = st.radio(
                "Navigation",
                ["📊 Dashboard"],
                label_visibility="collapsed"
            )
        else:
            user_data = st.session_state.users[st.session_state.current_user]
            
            st.markdown(f"**User:** {st.session_state.current_user}")
            st.markdown("---")
            
            # Quick stats
            st.metric("⭐ Credits", user_data['credits'])
            st.metric("💰 Rupees", f"₹{credits_to_rupees(user_data['credits'])}")
            st.metric("🌾 URAM Count", user_data['uram_count'])
            
            st.markdown("---")
            
            page = st.radio(
                "Navigation",
                [
                    "🏠 Home",
                    "♻️ Submit Waste",
                    "💰 Wallet",
                    "🛒 Manure Store",
                    "📝 Feedback"
                ],
                label_visibility="collapsed"
            )
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            logout_user()
            st.rerun()
        
        # Footer
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; font-size: 11px; color: #666;'>
            <p>🌍 Clean India Initiative</p>
            <p>♻️ Circular Economy</p>
            <p style='margin-top: 10px;'>© 2024 URAMix</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Route to pages
    if st.session_state.is_admin:
        admin_dashboard()
    else:
        if page == "🏠 Home":
            home_page()
        elif page == "♻️ Submit Waste":
            waste_submission_page()
        elif page == "💰 Wallet":
            wallet_page()
        elif page == "🛒 Manure Store":
            manure_marketplace()
        elif page == "📝 Feedback":
            feedback_page()

# Run the application
if __name__ == "__main__":
    main()
