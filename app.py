import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import qrcode
from io import BytesIO
import base64
from datetime import datetime, timedelta
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Page Configuration
st.set_page_config(
    page_title="URAMix - Waste to Wealth",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Green Eco Theme
st.markdown("""
<style>
    .main {
        background-color: #f0f8f0;
    }
    .stButton>button {
        background-color: #28a745;
        color: white;
        border-radius: 10px;
        padding: 10px 24px;
        border: none;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #218838;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .problem-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #28a745;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        animation: slideIn 0.5s ease-out;
    }
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    .product-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        text-align: center;
        transition: transform 0.3s;
    }
    .product-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    .hero-text {
        font-size: 3em;
        font-weight: bold;
        color: #28a745;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .sub-hero {
        font-size: 1.5em;
        color: #555;
        text-align: center;
        margin-bottom: 30px;
    }
    .dustbin-container {
        background: linear-gradient(to bottom, #e8f5e9 0%, #c8e6c9 100%);
        border-radius: 15px;
        padding: 30px;
        margin: 20px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .dustbin-fill {
        background: linear-gradient(to top, #4caf50 0%, #81c784 100%);
        border-radius: 10px;
        transition: height 0.5s ease;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
def init_session_state():
    if 'users' not in st.session_state:
        st.session_state.users = {}
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'current_user' not in st.session_state:
        st.session_state.current_user = None
    if 'is_admin' not in st.session_state:
        st.session_state.is_admin = False
    if 'total_credits_issued' not in st.session_state:
        st.session_state.total_credits_issued = 0
    if 'daily_credits' not in st.session_state:
        st.session_state.daily_credits = {}
    if 'qr_codes' not in st.session_state:
        st.session_state.qr_codes = {}
    if 'feedbacks' not in st.session_state:
        st.session_state.feedbacks = []
    if 'total_manure' not in st.session_state:
        st.session_state.total_manure = 1000  # Initial stock in kg
    if 'manure_price' not in st.session_state:
        st.session_state.manure_price = 50  # Price per kg
    if 'manure_sales' not in st.session_state:
        st.session_state.manure_sales = []
    if 'dustbin_fill_level' not in st.session_state:
        st.session_state.dustbin_fill_level = 0

init_session_state()

# Authentication Functions
def signup_user(email, password):
    if email in st.session_state.users:
        return False, "Email already exists!"
    st.session_state.users[email] = {
        'password': password,
        'credits': 0,
        'waste_submissions': [],
        'manure_purchased': 0,
        'referral_used': False
    }
    return True, "Signup successful! Please login."

def login_user(email, password):
    if email == "admin" and password == "12345":
        st.session_state.logged_in = True
        st.session_state.is_admin = True
        st.session_state.current_user = "admin"
        return True, "Admin login successful!"
    
    if email in st.session_state.users:
        if st.session_state.users[email]['password'] == password:
            st.session_state.logged_in = True
            st.session_state.is_admin = False
            st.session_state.current_user = email
            return True, "Login successful!"
        return False, "Invalid password!"
    return False, "User not found!"

def logout():
    st.session_state.logged_in = False
    st.session_state.is_admin = False
    st.session_state.current_user = None

# QR Code Generation
def generate_qr_code(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return img_str

# Credit Calculation
def calculate_credits(waste_type, quantity):
    if waste_type == "Organic Waste":
        base_credits = 50  # Higher for organic
    else:
        base_credits = 30  # Lower for inorganic
    
    # Credits don't depend directly on quantity, but we add a small bonus
    quantity_bonus = min(quantity * 2, 20)  # Max 20 bonus credits
    total_credits = base_credits + quantity_bonus
    return int(total_credits)

# Email Feedback Function
def send_feedback_email(user_email, feedback_text):
    try:
        # Demo SMTP configuration (replace with actual credentials)
        sender_email = "your_email@gmail.com"
        sender_password = "your_app_password"
        receiver_email = "admin@uramix.com"
        
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = f"URAMix Feedback from {user_email}"
        
        body = f"User: {user_email}\n\nFeedback:\n{feedback_text}"
        msg.attach(MIMEText(body, 'plain'))
        
        # Uncomment to actually send email
        # server = smtplib.SMTP('smtp.gmail.com', 587)
        # server.starttls()
        # server.login(sender_email, sender_password)
        # server.send_message(msg)
        # server.quit()
        
        return True
    except Exception as e:
        return False

# Login/Signup Page
def auth_page():
    st.markdown('<p class="hero-text">♻️ URAMix</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-hero">Waste to Wealth | Clean India Mission</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        tab1, tab2 = st.tabs(["Login", "Signup"])
        
        with tab1:
            st.subheader("🔐 Login")
            email = st.text_input("Email / Username", key="login_email")
            password = st.text_input("Password", type="password", key="login_pass")
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("Login", use_container_width=True):
                    success, message = login_user(email, password)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
            
            with col_b:
                if st.button("🔍 Sign in with Google (Demo)", use_container_width=True):
                    st.info("Google Sign-In Demo Mode")
        
        with tab2:
            st.subheader("📝 Signup")
            new_email = st.text_input("Email", key="signup_email")
            new_password = st.text_input("Password", type="password", key="signup_pass")
            confirm_password = st.text_input("Confirm Password", type="password", key="confirm_pass")
            
            if st.button("Create Account", use_container_width=True):
                if new_password != confirm_password:
                    st.error("Passwords don't match!")
                elif len(new_password) < 4:
                    st.error("Password too short!")
                else:
                    success, message = signup_user(new_email, new_password)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)

# Home Page
def home_page():
    # Hero Section
    st.markdown('<p class="hero-text">🌍 Welcome to URAMix</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-hero">Transform Waste into Wealth | Clean India Initiative</p>', unsafe_allow_html=True)
    
    # Hero Images
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://via.placeholder.com/400x300/28a745/ffffff?text=Smart+Dustbin", use_container_width=True)
    with col2:
        st.image("https://via.placeholder.com/400x300/8bc34a/ffffff?text=Natural+Manure", use_container_width=True)
    
    # Dynamic Eco Quote
    user = st.session_state.users.get(st.session_state.current_user, {})
    reduction_percent = min(user.get('credits', 0) * 0.1, 100)
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 30px; border-radius: 15px; color: white; text-align: center; margin: 30px 0;'>
        <h2>🌱 You helped reduce landfill emissions by {reduction_percent:.1f}% today!</h2>
        <p style='font-size: 1.2em;'>Your eco credits increased! Keep going! 🌍</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Problem Statements
    st.markdown("### 🚨 Real-World Problems We're Solving")
    
    problems = [
        {"icon": "🗑️", "title": "Overflowing Bins", "desc": "People dump waste early because bins fill before collection"},
        {"icon": "⏰", "title": "Irregular Collection", "desc": "Unpredictable garbage collection schedules"},
        {"icon": "💰", "title": "Costly Manure", "desc": "Natural manure is expensive and unaffordable for farmers"},
        {"icon": "🌾", "title": "Farmer Crisis", "desc": "Small farmers can't compete with big manure corporations"}
    ]
    
    cols = st.columns(2)
    for idx, problem in enumerate(problems):
        with cols[idx % 2]:
            st.markdown(f"""
            <div class='problem-card'>
                <h3>{problem['icon']} {problem['title']}</h3>
                <p>{problem['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Mission Statement
    st.markdown("### ✨ Our Mission")
    missions = [
        "🇮🇳 Make India Clean",
        "♻️ Reduce Landfills",
        "🔄 Encourage Waste Segregation",
        "🌿 Convert Waste to Affordable Manure",
        "💳 Reward Users with Credits & Money"
    ]
    
    for mission in missions:
        st.markdown(f"**{mission}**")

# Dashboard Page
def dashboard_page():
    user = st.session_state.users[st.session_state.current_user]
    
    st.title("📊 Your Dashboard")
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class='metric-card'>
            <h2>{user['credits']}</h2>
            <p>Total Credits</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        rupees = user['credits'] * 0.05
        st.markdown(f"""
        <div class='metric-card'>
            <h2>₹{rupees:.2f}</h2>
            <p>Wallet Balance</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='metric-card'>
            <h2>{len(user['waste_submissions'])}</h2>
            <p>Waste Submissions</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class='metric-card'>
            <h2>{user['manure_purchased']}</h2>
            <p>URAM Count</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Withdrawal Section
    st.subheader("💰 Withdraw Credits")
    
    if user['credits'] >= 500:
        withdraw_amount = st.number_input("Credits to Withdraw", min_value=500, max_value=user['credits'], step=100)
        rupees_withdraw = withdraw_amount * 0.05
        st.info(f"You will receive: ₹{rupees_withdraw:.2f}")
        
        if st.button("Withdraw"):
            user['credits'] -= withdraw_amount
            st.success(f"✅ Successfully withdrawn ₹{rupees_withdraw:.2f}!")
            st.rerun()
    else:
        st.warning(f"⚠️ You need at least 500 credits to withdraw. Current: {user['credits']} credits")
    
    st.markdown("---")
    
    # Recent Activity
    st.subheader("📜 Recent Waste Submissions")
    if user['waste_submissions']:
        df = pd.DataFrame(user['waste_submissions'])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No submissions yet. Start submitting waste to earn credits!")

# Waste Submission Page
def waste_submission_page():
    st.title("♻️ Submit Waste")
    
    # Animated Dustbin Fill Simulator
    st.markdown("### 🗑️ Dustbin Fill Level Simulator")
    st.markdown('<div class="dustbin-container">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fill_level = st.slider(
            "Adjust Dustbin Fill Level (%)", 
            min_value=0, 
            max_value=100, 
            value=st.session_state.dustbin_fill_level,
            key="dustbin_slider"
        )
        st.session_state.dustbin_fill_level = fill_level
        
        # Visual dustbin representation
        dustbin_height = 300
        fill_height = int(dustbin_height * fill_level / 100)
        
        st.markdown(f"""
        <div style='background: #e0e0e0; width: 200px; height: {dustbin_height}px; 
                    border-radius: 10px; margin: 20px auto; position: relative; 
                    border: 3px solid #666; overflow: hidden;'>
            <div style='position: absolute; bottom: 0; width: 100%; height: {fill_height}px;
                        background: linear-gradient(to top, #4caf50 0%, #81c784 100%);
                        border-radius: 0 0 8px 8px; transition: height 0.5s ease;'>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if fill_level >= 80:
            st.error("🚨 Dustbin is nearly full! Please request collection.")
        elif fill_level >= 50:
            st.warning("⚠️ Dustbin is half full.")
        else:
            st.success("✅ Dustbin has space available.")
    
    with col2:
        st.metric("Fill Status", f"{fill_level}%")
        st.metric("Remaining Space", f"{100-fill_level}%")
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Waste Submission Form
    st.subheader("📦 Submit Your Waste")
    
    waste_type = st.selectbox("Select Waste Type", ["Organic Waste", "Inorganic Waste"])
    
    st.info(f"""
    **Credit Information:**
    - Organic Waste: Higher credits (50+ credits)
    - Inorganic Waste: Standard credits (30+ credits)
    - Referral Bonus: +20 credits (one-time)
    """)
    
    if st.button("Submit Waste Request"):
        # Generate unique QR code
        qr_data = f"{st.session_state.current_user}_{waste_type}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        qr_img = generate_qr_code(qr_data)
        
        st.session_state.qr_codes[qr_data] = {
            'user': st.session_state.current_user,
            'waste_type': waste_type,
            'verified': False,
            'quantity': 0
        }
        
        st.success("✅ Waste submission request created! Show this QR code to the collection staff.")
        st.image(f"data:image/png;base64,{qr_img}", width=300)
        st.code(qr_data)
    
    # Referral Section
    st.markdown("---")
    st.subheader("🎁 Referral Bonus")
    user = st.session_state.users[st.session_state.current_user]
    
    if not user['referral_used']:
        referral_code = st.text_input("Enter Referral Code (if any)")
        if st.button("Apply Referral"):
            if referral_code:
                user['credits'] += 20
                user['referral_used'] = True
                st.success("🎉 Referral bonus of 20 credits added!")
                st.rerun()
    else:
        st.info("✅ Referral bonus already claimed!")

# Manure Marketplace Page
def manure_page():
    st.title("🌿 URAM Manure Marketplace")
    
    st.markdown("""
    <div style='background: linear-gradient(135deg, #8bc34a 0%, #689f38 100%); 
                padding: 20px; border-radius: 15px; color: white; margin-bottom: 30px;'>
        <h3>🌾 Premium Natural Manure - Made from YOUR Waste!</h3>
        <p>Affordable, eco-friendly, and supports Indian farmers</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display available stock
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Available Stock", f"{st.session_state.total_manure} kg")
    with col2:
        st.metric("Price per kg", f"₹{st.session_state.manure_price}")
    with col3:
        user = st.session_state.users[st.session_state.current_user]
        st.metric("Your URAM Count", f"{user['manure_purchased']} kg")
    
    st.markdown("---")
    
    # Product Card
    col_left, col_center, col_right = st.columns([1, 2, 1])
    
    with col_center:
        st.markdown("""
        <div class='product-card'>
            <img src='https://via.placeholder.com/300x200/8bc34a/ffffff?text=Natural+Manure' 
                 style='width: 100%; border-radius: 10px;'>
            <h2 style='color: #28a745; margin: 20px 0;'>🌿 URAM Natural Manure</h2>
            <p style='color: #666; font-size: 1.1em;'>Premium quality organic manure</p>
            <h3 style='color: #28a745;'>₹{} per kg</h3>
        </div>
        """.format(st.session_state.manure_price), unsafe_allow_html=True)
        
        if st.session_state.total_manure > 0:
            max_qty = min(st.session_state.total_manure, 100)
            quantity = st.number_input(
                "Quantity (in kg)", 
                min_value=1, 
                max_value=max_qty,
                value=1,
                step=1
            )
            
            total_price = quantity * st.session_state.manure_price
            st.info(f"Total Price: ₹{total_price}")
            
            if st.button("🛒 Buy Now", use_container_width=True):
                if st.session_state.total_manure >= quantity:
                    st.session_state.total_manure -= quantity
                    user['manure_purchased'] += quantity
                    
                    # Record sale
                    st.session_state.manure_sales.append({
                        'date': datetime.now().strftime('%Y-%m-%d'),
                        'user': st.session_state.current_user,
                        'quantity': quantity,
                        'amount': total_price
                    })
                    
                    st.success(f"✅ Successfully purchased {quantity} kg of URAM manure!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("❌ Insufficient stock!")
        else:
            st.warning("⚠️ Out of stock! Check back later.")

# Feedback Page
def feedback_page():
    st.title("💬 Send Feedback")
    
    st.markdown("""
    <div style='background: #e3f2fd; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
        <h4>We value your feedback! 🌟</h4>
        <p>Help us improve URAMix by sharing your thoughts and suggestions.</p>
    </div>
    """, unsafe_allow_html=True)
    
    feedback_text = st.text_area("Your Feedback", height=200, placeholder="Share your experience, suggestions, or report issues...")
    
    if st.button("Submit Feedback", use_container_width=True):
        if feedback_text:
            feedback_entry = {
                'user': st.session_state.current_user,
                'feedback': feedback_text,
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            st.session_state.feedbacks.append(feedback_entry)
            
            # Try to send email
            email_sent = send_feedback_email(st.session_state.current_user, feedback_text)
            
            st.success("✅ Feedback submitted successfully!")
            if email_sent:
                st.info("📧 Email notification sent to admin.")
            else:
                st.info("📧 Email notification pending (configure SMTP settings).")
        else:
            st.error("❌ Please enter feedback before submitting.")

# Admin Dashboard
def admin_dashboard():
    st.title("🔧 Admin Dashboard")
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Users", len(st.session_state.users))
    with col2:
        st.metric("Credits Issued", st.session_state.total_credits_issued)
    with col3:
        st.metric("Manure Stock", f"{st.session_state.total_manure} kg")
    with col4:
        total_sales = sum([sale['amount'] for sale in st.session_state.manure_sales])
        st.metric("Total Sales", f"₹{total_sales}")
    
    st.markdown("---")
    
    # Tabs for different admin functions
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "QR Verification", "Manure Management", "Analytics", "Feedbacks", "Users"
    ])
    
    with tab1:
        st.subheader("📱 QR Code Verification")
        
        qr_code_input = st.text_input("Enter QR Code Data")
        
        if st.button("Verify QR"):
            if qr_code_input in st.session_state.qr_codes:
                qr_info = st.session_state.qr_codes[qr_code_input]
                
                if not qr_info['verified']:
                    st.success(f"✅ Valid QR Code - User: {qr_info['user']}, Type: {qr_info['waste_type']}")
                    
                    quantity = st.number_input("Enter Verified Quantity (kg)", min_value=0.5, value=5.0, step=0.5)
                    
                    if st.button("Confirm & Issue Credits"):
                        # Calculate credits
                        credits = calculate_credits(qr_info['waste_type'], quantity)
                        
                        # Add credits to user
                        user = st.session_state.users[qr_info['user']]
                        user['credits'] += credits
                        user['waste_submissions'].append({
                            'date': datetime.now().strftime('%Y-%m-%d'),
                            'type': qr_info['waste_type'],
                            'quantity': quantity,
                            'credits': credits
                        })
                        
                        # Update QR status
                        qr_info['verified'] = True
                        qr_info['quantity'] = quantity
                        
                        # Update total credits
                        st.session_state.total_credits_issued += credits
                        
                        # Track daily credits
                        today = datetime.now().strftime('%Y-%m-%d')
                        if today not in st.session_state.daily_credits:
                            st.session_state.daily_credits[today] = 0
                        st.session_state.daily_credits[today] += credits
                        
                        st.success(f"✅ {credits} credits issued to {qr_info['user']}!")
                        st.balloons()
                else:
                    st.warning("⚠️ This QR code has already been verified.")
            else:
                st.error("❌ Invalid QR code!")
    
    with tab2:
        st.subheader("🌿 Manure Stock Management")
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            add_stock = st.number_input("Add Stock (kg)", min_value=0, value=100, step=10)
            if st.button("Add Stock"):
                st.session_state.total_manure += add_stock
                st.success(f"✅ Added {add_stock} kg to stock!")
                st.rerun()
        
        with col_b:
            new_price = st.number_input("Set Price per kg (₹)", min_value=10, value=st.session_state.manure_price, step=5)
            if st.button("Update Price"):
                st.session_state.manure_price = new_price
                st.success(f"✅ Price updated to ₹{new_price}/kg!")
                st.rerun()
        
        st.markdown("---")
        st.subheader("📊 Manure Sales History")
        if st.session_state.manure_sales:
            df_sales = pd.DataFrame(st.session_state.manure_sales)
            st.dataframe(df_sales, use_container_width=True)
        else:
            st.info("No sales recorded yet.")
    
    with tab3:
        st.subheader("📈 Analytics")
        
        # Daily Credits Chart
        if st.session_state.daily_credits:
            st.markdown("#### Daily Credits Issued")
            dates = list(st.session_state.daily_credits.keys())
            credits = list(st.session_state.daily_credits.values())
            
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.bar(dates, credits, color='#28a745')
            ax.set_xlabel('Date')
            ax.set_ylabel('Credits')
            ax.set_title('Daily Credits Distribution')
            plt.xticks(rotation=45)
            st.pyplot(fig)
        else:
            st.info("No credit data available yet.")
        
        st.markdown("---")
        
        # Manure Sales Chart
        if st.session_state.manure_sales:
            st.markdown("#### Manure Sales Analytics")
            df_sales = pd.DataFrame(st.session_state.manure_sales)
            sales_by_date = df_sales.groupby('date')['quantity'].sum()
            
            fig2, ax2 = plt.subplots(figsize=(10, 5))
            ax2.plot(sales_by_date.index, sales_by_date.values, marker='o', color='#8bc34a', linewidth=2)
            ax2.set_xlabel('Date')
            ax2.set_ylabel('Quantity (kg)')
            ax2.set_title('Manure Sales Over Time')
            plt.xticks(rotation=45)
            st.pyplot(fig2)
    
    with tab4:
        st.subheader("💬 User Feedbacks")
        
        if st.session_state.feedbacks:
            for feedback in reversed(st.session_state.feedbacks):
                st.markdown(f"""
                <div style='background: white; padding: 15px; border-radius: 10px; 
                            margin: 10px 0; border-left: 4px solid #28a745;'>
                    <strong>👤 {feedback['user']}</strong><br>
                    <small>📅 {feedback['date']}</small><br>
                    <p style='margin-top: 10px;'>{feedback['feedback']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No feedbacks received yet.")
    
    with tab5:
        st.subheader("👥 Registered Users")
        
        if st.session_state.users:
            users_data = []
            for email, data in st.session_state.users.items():
                users_data.append({
                    'Email': email,
                    'Credits': data['credits'],
                    'Submissions': len(data['waste_submissions']),
                    'Manure Purchased': data['manure_purchased']
                })
            
            df_users = pd.DataFrame(users_data)
            st.dataframe(df_users, use_container_width=True)
        else:
            st.info("No users registered yet.")

# Main App
def main():
    # Sidebar
    with st.sidebar:
        st.markdown("### ♻️ URAMix Navigation")
        
        if st.session_state.logged_in:
            if st.session_state.is_admin:
                st.success("🔧 Admin Mode")
                page = st.radio("Go to", ["Admin Dashboard"], label_visibility="collapsed")
            else:
                st.success(f"👤 {st.session_state.current_user}")
                page = st.radio(
                    "Go to",
                    ["Home", "Dashboard", "Submit Waste", "Buy Manure", "Feedback"]
                )
            
            st.markdown("---")
            if st.button("🚪 Logout", use_container_width=True):
                logout()
                st.rerun()
        else:
            st.info("Please login to continue")
            page = "Login"
    
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
                dashboard_page()
            elif page == "Submit Waste":
                waste_submission_page()
            elif page == "Buy Manure":
                manure_page()
            elif page == "Feedback":
                feedback_page()

if __name__ == "__main__":
    main()
